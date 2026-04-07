"""Vector embeddings with LanceDB local store and Neon pgvector.

Provides a dual-backend embedding system following the mempalace pattern:
- LanceDB: Local vector store for fast similarity search (no API needed)
- Neon pgvector: Postgres-native embeddings for production persistence

The embedding pipeline:
1. Content arrives from crawlers (src/crawlers.py) or DSPy extraction (src/dspy_prompts.py)
2. Text is chunked and embedded via sentence-level hashing or model embeddings
3. Vectors stored in LanceDB (local) and/or Neon pgvector (remote)
4. Semantic search queries both backends with result fusion

UDA pattern: embeddings are a projection of crawled content. The vector
index is a DataContainer that maps back to crawl_pages via content_hash.

Mempalace integration:
- Wings map to embedding namespaces (ontology, skills, docs)
- Rooms map to metadata filters (topic, language, skill)
- Drawers are individual embedded chunks with source provenance

Uses CLAUDE_CODE_OAUTH_TOKEN for any API calls (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ── Text Chunking ───────────────────────────────────────────


def chunk_text(
    text: str,
    chunk_size: int = 512,
    overlap: int = 64,
) -> list[dict[str, Any]]:
    """Split text into overlapping chunks for embedding.

    Args:
        text: Source text to chunk.
        chunk_size: Target chunk size in characters.
        overlap: Overlap between consecutive chunks.

    Returns:
        List of dicts with 'text', 'start', 'end', 'index' keys.
    """
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        if chunk.strip():
            chunks.append({
                "text": chunk.strip(),
                "start": start,
                "end": end,
                "index": idx,
            })
            idx += 1
        start += chunk_size - overlap
    return chunks


# ── Content-Hash Embeddings (no model needed) ───────────────


def hash_embedding(text: str, dim: int = 384) -> list[float]:
    """Generate a deterministic pseudo-embedding from content hash.

    Uses SHA-512 to derive a fixed-dimension vector without any
    external model. Good for exact and near-exact deduplication.
    Not suitable for semantic similarity.

    Args:
        text: Text to embed.
        dim: Output dimension (default 384 to match MiniLM).

    Returns:
        Normalized float vector of length dim.
    """
    # Generate enough hash bytes for the target dimension (2 bytes per dim)
    hash_bytes = b""
    for i in range(math.ceil(dim * 2 / 64)):
        hash_bytes += hashlib.sha512(f"{text}:{i}".encode()).digest()

    # Unpack as unsigned 16-bit ints, convert to [-1, 1] floats
    raw = struct.unpack(f"<{dim}H", hash_bytes[: dim * 2])
    values = [(v / 32767.5) - 1.0 for v in raw]
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


# ── Embedding Record ────────────────────────────────────────


@dataclass
class EmbeddingRecord:
    """A single embedded chunk with metadata.

    Follows mempalace drawer pattern: each record is a "drawer"
    in a "room" within a "wing" of the memory palace.
    """

    id: str
    text: str
    vector: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)

    # Mempalace taxonomy
    wing: str = ""      # Domain: ontology, skills, docs, code
    room: str = ""      # Topic: tool-use, streaming, agents, mcp
    source_url: str = ""
    content_hash: str = ""


# ── LanceDB Local Vector Store ──────────────────────────────


class LanceStore:
    """Local vector store using LanceDB for fast similarity search.

    LanceDB stores vectors in Lance columnar format on disk,
    enabling millisecond queries without a server.

    Args:
        db_path: Path to LanceDB database directory.
        table_name: Name of the vector table.
        dim: Embedding dimension.
    """

    def __init__(
        self,
        db_path: str | Path = ".lancedb",
        table_name: str = "embeddings",
        dim: int = 384,
    ):
        self.db_path = Path(db_path)
        self.table_name = table_name
        self.dim = dim
        self._db = None
        self._table = None

    def _ensure_db(self):
        """Lazy-initialize LanceDB connection."""
        if self._db is None:
            import lancedb

            self.db_path.mkdir(parents=True, exist_ok=True)
            self._db = lancedb.connect(str(self.db_path))

    def _ensure_table(self):
        """Ensure the vector table exists."""
        self._ensure_db()
        assert self._db is not None
        if self._table is None:
            try:
                self._table = self._db.open_table(self.table_name)
            except Exception:
                # Create with schema on first use
                import pyarrow as pa

                schema = pa.schema([
                    pa.field("id", pa.string()),
                    pa.field("text", pa.string()),
                    pa.field("vector", pa.list_(pa.float32(), self.dim)),
                    pa.field("wing", pa.string()),
                    pa.field("room", pa.string()),
                    pa.field("source_url", pa.string()),
                    pa.field("content_hash", pa.string()),
                    pa.field("metadata", pa.string()),
                ])
                self._table = self._db.create_table(
                    self.table_name,
                    schema=schema,
                )

    def add(self, records: list[EmbeddingRecord]) -> int:
        """Add embedding records to the store. Returns count added."""
        self._ensure_table()
        assert self._table is not None
        rows = [
            {
                "id": r.id,
                "text": r.text,
                "vector": r.vector,
                "wing": r.wing,
                "room": r.room,
                "source_url": r.source_url,
                "content_hash": r.content_hash,
                "metadata": json.dumps(r.metadata),
            }
            for r in records
        ]
        self._table.add(rows)
        return len(rows)

    def search(
        self,
        query_vector: list[float],
        *,
        limit: int = 10,
        wing: str = "",
        room: str = "",
    ) -> list[dict[str, Any]]:
        """Search for similar vectors with optional metadata filters.

        Args:
            query_vector: Query embedding vector.
            limit: Max results to return.
            wing: Filter by wing (mempalace domain).
            room: Filter by room (mempalace topic).

        Returns:
            List of result dicts with text, score, and metadata.
        """
        self._ensure_table()
        assert self._table is not None
        query = self._table.search(query_vector).limit(limit)

        if wing:
            query = query.where(f"wing = '{wing}'")
        if room:
            query = query.where(f"room = '{room}'")

        results = query.to_list()
        return [
            {
                "id": r["id"],
                "text": r["text"],
                "score": 1.0 - r.get("_distance", 0.0),
                "wing": r["wing"],
                "room": r["room"],
                "source_url": r["source_url"],
                "content_hash": r["content_hash"],
                "metadata": json.loads(r.get("metadata", "{}")),
            }
            for r in results
        ]

    def count(self) -> int:
        """Return total number of records in the store."""
        self._ensure_table()
        assert self._table is not None
        return self._table.count_rows()

    def delete(self, ids: list[str]) -> None:
        """Delete records by ID."""
        self._ensure_table()
        assert self._table is not None
        id_list = ", ".join(f"'{i}'" for i in ids)
        self._table.delete(f"id IN ({id_list})")


# ── Neon pgvector Store ─────────────────────────────────────


class NeonVectorStore:
    """Neon Postgres 18 vector store using pgvector extension.

    Stores embeddings in a Postgres table with the vector type,
    enabling SQL-native similarity search alongside relational
    queries on the same database.

    Args:
        dim: Embedding dimension (must match index).
    """

    def __init__(self, dim: int = 384):
        self.dim = dim

    async def ensure_schema(self, conn) -> None:
        """Create pgvector extension and embeddings table if needed."""
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS embeddings (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                embedding vector({self.dim}) NOT NULL,
                wing TEXT NOT NULL DEFAULT '',
                room TEXT NOT NULL DEFAULT '',
                source_url TEXT NOT NULL DEFAULT '',
                content_hash TEXT NOT NULL DEFAULT '',
                metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                created_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_embeddings_vector
            ON embeddings USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """)
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_embeddings_wing
            ON embeddings(wing)
        """)
        await conn.commit()

    async def add(self, conn, records: list[EmbeddingRecord]) -> int:
        """Insert embedding records into Neon pgvector table."""
        count = 0
        for r in records:
            vec_str = "[" + ",".join(str(v) for v in r.vector) + "]"
            await conn.execute(
                """INSERT INTO embeddings (id, text, embedding, wing, room,
                       source_url, content_hash, metadata)
                   VALUES (%s, %s, %s::vector, %s, %s, %s, %s, %s)
                   ON CONFLICT (id) DO UPDATE SET
                       embedding = EXCLUDED.embedding,
                       metadata = EXCLUDED.metadata""",
                (
                    r.id,
                    r.text,
                    vec_str,
                    r.wing,
                    r.room,
                    r.source_url,
                    r.content_hash,
                    json.dumps(r.metadata),
                ),
            )
            count += 1
        await conn.commit()
        return count

    async def search(
        self,
        conn,
        query_vector: list[float],
        *,
        limit: int = 10,
        wing: str = "",
        room: str = "",
    ) -> list[dict[str, Any]]:
        """Search for similar vectors using pgvector cosine distance."""
        vec_str = "[" + ",".join(str(v) for v in query_vector) + "]"
        where_clauses = []
        params: list = [vec_str]

        if wing:
            where_clauses.append("wing = %s")
            params.append(wing)
        if room:
            where_clauses.append("room = %s")
            params.append(room)

        where = ""
        if where_clauses:
            where = "WHERE " + " AND ".join(where_clauses)

        params.append(limit)
        rows = await (
            await conn.execute(
                f"""SELECT id, text, 1 - (embedding <=> %s::vector) AS score,
                           wing, room, source_url, content_hash, metadata
                    FROM embeddings {where}
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s""",
                (*params[:1], *params),
            )
        ).fetchall()

        return [
            {
                "id": r[0],
                "text": r[1],
                "score": float(r[2]),
                "wing": r[3],
                "room": r[4],
                "source_url": r[5],
                "content_hash": r[6],
                "metadata": r[7],
            }
            for r in rows
        ]

    async def count(self, conn) -> int:
        """Return total embedding count."""
        row = await (await conn.execute("SELECT COUNT(*) FROM embeddings")).fetchone()
        return row[0]


# ── Embedding Pipeline ──────────────────────────────────────


class EmbeddingPipeline:
    """End-to-end embedding pipeline: chunk → embed → store.

    Connects crawl output to vector stores following the UDA
    DataContainer pattern. Content flows:
    crawl_pages → chunk → embed → LanceDB + Neon pgvector

    Args:
        lance_store: Local LanceDB store (optional).
        neon_store: Neon pgvector store (optional).
        dim: Embedding dimension.
        chunk_size: Text chunk size for splitting.
    """

    def __init__(
        self,
        *,
        lance_store: LanceStore | None = None,
        neon_store: NeonVectorStore | None = None,
        dim: int = 384,
        chunk_size: int = 512,
    ):
        self.lance_store = lance_store
        self.neon_store = neon_store
        self.dim = dim
        self.chunk_size = chunk_size

    def embed_page(
        self,
        url: str,
        content: str,
        *,
        wing: str = "docs",
        room: str = "",
        content_hash: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> list[EmbeddingRecord]:
        """Chunk and embed a crawled page.

        Returns EmbeddingRecords ready for storage in either backend.
        """
        chunks = chunk_text(content, chunk_size=self.chunk_size)
        records = []

        for chunk in chunks:
            chunk_id = hashlib.sha256(
                f"{url}:{chunk['index']}".encode()
            ).hexdigest()[:16]

            records.append(EmbeddingRecord(
                id=chunk_id,
                text=chunk["text"],
                vector=hash_embedding(chunk["text"], dim=self.dim),
                wing=wing,
                room=room,
                source_url=url,
                content_hash=content_hash,
                metadata={
                    **(metadata or {}),
                    "chunk_index": chunk["index"],
                    "char_start": chunk["start"],
                    "char_end": chunk["end"],
                },
            ))

        return records

    def store_local(self, records: list[EmbeddingRecord]) -> int:
        """Store records in local LanceDB."""
        if not self.lance_store:
            return 0
        return self.lance_store.add(records)

    async def store_neon(self, conn, records: list[EmbeddingRecord]) -> int:
        """Store records in Neon pgvector."""
        if not self.neon_store:
            return 0
        return await self.neon_store.add(conn, records)

    def search_local(
        self,
        query: str,
        *,
        limit: int = 10,
        wing: str = "",
        room: str = "",
    ) -> list[dict[str, Any]]:
        """Search local LanceDB store."""
        if not self.lance_store:
            return []
        query_vec = hash_embedding(query, dim=self.dim)
        return self.lance_store.search(
            query_vec, limit=limit, wing=wing, room=room
        )

    async def search_neon(
        self,
        conn,
        query: str,
        *,
        limit: int = 10,
        wing: str = "",
        room: str = "",
    ) -> list[dict[str, Any]]:
        """Search Neon pgvector store."""
        if not self.neon_store:
            return []
        query_vec = hash_embedding(query, dim=self.dim)
        return await self.neon_store.search(
            conn, query_vec, limit=limit, wing=wing, room=room
        )
