"""Probabilistic bloom filter with Neon Postgres persistence.

Implements a proper bit-array bloom filter (not just a set of hashes)
with configurable false-positive rate, multiple hash functions, and
async persistence to Neon Postgres for cross-session deduplication.

UDA pattern: bloom filter state is a DataContainer projected from the
ontology's as:BloomFilter class → bloom_filters Postgres table.
"""

from __future__ import annotations

import hashlib
import math
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import psycopg


class BloomFilter:
    """Bit-array bloom filter with tunable false-positive rate.

    Args:
        expected_items: Expected number of items to insert.
        fp_rate: Target false-positive rate (default 0.01 = 1%).
        bit_array: Pre-existing bit array for restore from DB.
        num_hashes: Override computed optimal hash count.
    """

    def __init__(
        self,
        expected_items: int = 100_000,
        fp_rate: float = 0.01,
        *,
        bit_array: bytearray | None = None,
        num_hashes: int | None = None,
    ):
        self.expected_items = expected_items
        self.fp_rate = fp_rate

        # Optimal bit array size: m = -n*ln(p) / (ln2)^2
        self.size = self._optimal_size(expected_items, fp_rate)
        # Optimal hash count: k = (m/n) * ln2
        self.num_hashes = num_hashes or self._optimal_hashes(self.size, expected_items)

        self._bits = bit_array if bit_array is not None else bytearray(self.size // 8 + 1)
        self._count = 0

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        """Compute optimal bit array size for n items at false-positive rate p."""
        m = -n * math.log(p) / (math.log(2) ** 2)
        return int(m) + 1

    @staticmethod
    def _optimal_hashes(m: int, n: int) -> int:
        """Compute optimal number of hash functions."""
        k = (m / n) * math.log(2)
        return max(1, int(k) + 1)

    def _hash_positions(self, item: str) -> list[int]:
        """Generate k bit positions using double hashing (Kirsch-Mitzenmacker).

        Uses SHA-256 to derive two base hashes, then combines them:
            h_i(x) = (h1(x) + i * h2(x)) mod m
        """
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1, h2 = struct.unpack_from("<QQ", digest)
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def add(self, item: str) -> bool:
        """Add item to filter. Returns True if item was new (probably)."""
        positions = self._hash_positions(item)
        was_new = False
        for pos in positions:
            byte_idx = pos // 8
            bit_idx = pos % 8
            if not (self._bits[byte_idx] & (1 << bit_idx)):
                was_new = True
            self._bits[byte_idx] |= 1 << bit_idx
        if was_new:
            self._count += 1
        return was_new

    def __contains__(self, item: str) -> bool:
        """Check if item is probably in the filter (may have false positives)."""
        for pos in self._hash_positions(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            if not (self._bits[byte_idx] & (1 << bit_idx)):
                return False
        return True

    def is_new(self, item: str) -> bool:
        """Check and add: returns True if item was not seen before. Adds it."""
        if item in self:
            return False
        self.add(item)
        return True

    @property
    def estimated_fp_rate(self) -> float:
        """Current estimated false-positive rate based on fill ratio."""
        if self._count == 0:
            return 0.0
        fill = 1 - math.exp(-self.num_hashes * self._count / self.size)
        return fill**self.num_hashes

    def to_bytes(self) -> bytes:
        """Serialize bit array for persistence."""
        return bytes(self._bits)

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        expected_items: int = 100_000,
        fp_rate: float = 0.01,
        num_hashes: int | None = None,
    ) -> BloomFilter:
        """Restore filter from persisted bytes."""
        bf = cls(
            expected_items=expected_items,
            fp_rate=fp_rate,
            bit_array=bytearray(data),
            num_hashes=num_hashes,
        )
        return bf

    def __len__(self) -> int:
        return self._count

    def clear(self) -> None:
        self._bits = bytearray(self.size // 8 + 1)
        self._count = 0


class NeonBloomStore:
    """Async persistence layer for bloom filters in Neon Postgres 18.

    Stores filter state in the bloom_filters table, enabling cross-session
    deduplication for crawlers and pipelines.

    UDA mapping: as:BloomFilter → bloom_filters table
    """

    def __init__(self, conn: psycopg.AsyncConnection):
        self._conn = conn

    async def save(self, name: str, bloom: BloomFilter, *, domain: str = "") -> None:
        """Persist bloom filter state to Neon."""
        await self._conn.execute(
            """INSERT INTO bloom_filters (name, domain, bit_array, expected_items,
                   fp_rate, num_hashes, item_count, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, now())
               ON CONFLICT (name) DO UPDATE SET
                   bit_array = EXCLUDED.bit_array,
                   item_count = EXCLUDED.item_count,
                   updated_at = now()""",
            (
                name,
                domain,
                bloom.to_bytes(),
                bloom.expected_items,
                bloom.fp_rate,
                bloom.num_hashes,
                len(bloom),
            ),
        )
        await self._conn.commit()

    async def load(self, name: str) -> BloomFilter | None:
        """Load bloom filter state from Neon. Returns None if not found."""
        row = await (
            await self._conn.execute(
                """SELECT bit_array, expected_items, fp_rate, num_hashes
                   FROM bloom_filters WHERE name = %s""",
                (name,),
            )
        ).fetchone()
        if row is None:
            return None
        return BloomFilter.from_bytes(
            bytes(row[0]),
            expected_items=row[1],
            fp_rate=row[2],
            num_hashes=row[3],
        )

    async def delete(self, name: str) -> None:
        """Remove a persisted bloom filter."""
        await self._conn.execute("DELETE FROM bloom_filters WHERE name = %s", (name,))
        await self._conn.commit()

    async def list_filters(self) -> list[dict]:
        """List all stored bloom filters with metadata."""
        rows = await (
            await self._conn.execute(
                """SELECT name, domain, expected_items, item_count,
                          fp_rate, updated_at
                   FROM bloom_filters ORDER BY updated_at DESC"""
            )
        ).fetchall()
        return [
            {
                "name": r[0],
                "domain": r[1],
                "expected_items": r[2],
                "item_count": r[3],
                "fp_rate": r[4],
                "updated_at": r[5],
            }
            for r in rows
        ]
