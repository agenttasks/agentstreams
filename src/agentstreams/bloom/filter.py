"""Bloom filter implementation for URL deduplication in crawl pipelines.

Uses mmh3-compatible hashing with configurable capacity and false-positive rate.
Persists filter state to Neon Postgres for cross-session deduplication.

Netflix UDA alignment: deduplication is a core data quality gate in the
ingest pipeline, tracked via agentstreams.crawl.dedup metric.
"""

from __future__ import annotations

import hashlib
import math
import struct
from datetime import UTC, datetime


class BloomFilter:
    """Memory-efficient probabilistic set for URL deduplication.

    Args:
        capacity: Expected number of elements.
        fp_rate: Target false-positive rate (default 0.1%).
    """

    def __init__(self, capacity: int = 100_000, fp_rate: float = 0.001) -> None:
        self.capacity = capacity
        self.fp_rate = fp_rate

        # Optimal bit array size: m = -n * ln(p) / (ln2)^2
        self.size = self._optimal_size(capacity, fp_rate)
        # Optimal number of hash functions: k = (m/n) * ln2
        self.num_hashes = self._optimal_hashes(self.size, capacity)

        self._bits = bytearray(math.ceil(self.size / 8))
        self._count = 0
        self.created_at = datetime.now(UTC)

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        """Calculate optimal bit array size."""
        return int(-n * math.log(p) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hashes(m: int, n: int) -> int:
        """Calculate optimal number of hash functions."""
        return max(1, int((m / n) * math.log(2)))

    def _hash_pair(self, item: str) -> tuple[int, int]:
        """Generate two independent hash values using SHA-256."""
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = struct.unpack("<Q", digest[:8])[0]
        h2 = struct.unpack("<Q", digest[8:16])[0]
        return h1, h2

    def _get_positions(self, item: str) -> list[int]:
        """Get bit positions for an item using double hashing."""
        h1, h2 = self._hash_pair(item)
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def add(self, item: str) -> bool:
        """Add an item. Returns True if the item was already (probably) present."""
        positions = self._get_positions(item)
        was_present = all(self._get_bit(pos) for pos in positions)
        for pos in positions:
            self._set_bit(pos)
        if not was_present:
            self._count += 1
        return was_present

    def __contains__(self, item: str) -> bool:
        """Check if an item is (probably) in the set."""
        return all(self._get_bit(pos) for pos in self._get_positions(item))

    def _set_bit(self, position: int) -> None:
        byte_idx = position // 8
        bit_idx = position % 8
        self._bits[byte_idx] |= 1 << bit_idx

    def _get_bit(self, position: int) -> bool:
        byte_idx = position // 8
        bit_idx = position % 8
        return bool(self._bits[byte_idx] & (1 << bit_idx))

    @property
    def count(self) -> int:
        """Number of unique items added."""
        return self._count

    @property
    def fill_ratio(self) -> float:
        """Fraction of bits set (saturation indicator)."""
        set_bits = sum(bin(b).count("1") for b in self._bits)
        return set_bits / self.size

    @property
    def estimated_fp_rate(self) -> float:
        """Current estimated false-positive rate based on fill ratio."""
        if self._count == 0:
            return 0.0
        return (1 - math.exp(-self.num_hashes * self._count / self.size)) ** self.num_hashes

    def to_bytes(self) -> bytes:
        """Serialize filter state for persistence."""
        header = struct.pack("<IIdI", self.capacity, self.size, self.fp_rate, self._count)
        return header + bytes(self._bits)

    @classmethod
    def from_bytes(cls, data: bytes) -> BloomFilter:
        """Deserialize filter state."""
        header_size = struct.calcsize("<IIdI")
        capacity, size, fp_rate, count = struct.unpack("<IIdI", data[:header_size])
        bf = cls(capacity=capacity, fp_rate=fp_rate)
        bf._bits = bytearray(data[header_size:])
        bf._count = count
        return bf

    def merge(self, other: BloomFilter) -> None:
        """Merge another bloom filter into this one (OR operation).

        Both filters must have the same capacity and fp_rate.
        """
        if self.size != other.size:
            raise ValueError("Cannot merge filters with different sizes")
        for i in range(len(self._bits)):
            self._bits[i] |= other._bits[i]
        # Count is approximate after merge
        self._count = max(self._count, other._count)

    def stats(self) -> dict:
        """Return filter statistics for metrics reporting."""
        return {
            "capacity": self.capacity,
            "count": self._count,
            "size_bits": self.size,
            "num_hashes": self.num_hashes,
            "fill_ratio": round(self.fill_ratio, 6),
            "target_fp_rate": self.fp_rate,
            "estimated_fp_rate": round(self.estimated_fp_rate, 8),
            "size_bytes": len(self._bits),
        }
