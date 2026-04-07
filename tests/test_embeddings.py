"""Tests for src/embeddings.py — LanceDB + pgvector embedding pipeline."""

from __future__ import annotations

from src.embeddings import (
    EmbeddingPipeline,
    EmbeddingRecord,
    chunk_text,
    hash_embedding,
)


class TestChunkText:
    def test_basic_chunking(self):
        text = "a" * 1024
        chunks = chunk_text(text, chunk_size=512, overlap=64)
        assert len(chunks) >= 2
        assert all(c["text"] for c in chunks)

    def test_chunk_has_metadata(self):
        chunks = chunk_text("hello world this is a test", chunk_size=10, overlap=2)
        assert len(chunks) >= 1
        first = chunks[0]
        assert "text" in first
        assert "start" in first
        assert "end" in first
        assert "index" in first
        assert first["index"] == 0

    def test_short_text_single_chunk(self):
        chunks = chunk_text("short", chunk_size=512)
        assert len(chunks) == 1
        assert chunks[0]["text"] == "short"

    def test_empty_text_no_chunks(self):
        chunks = chunk_text("", chunk_size=512)
        assert len(chunks) == 0

    def test_overlap_creates_more_chunks(self):
        text = "a" * 1000
        no_overlap = chunk_text(text, chunk_size=500, overlap=0)
        with_overlap = chunk_text(text, chunk_size=500, overlap=100)
        assert len(with_overlap) >= len(no_overlap)


class TestHashEmbedding:
    def test_returns_correct_dimension(self):
        vec = hash_embedding("hello", dim=384)
        assert len(vec) == 384

    def test_custom_dimension(self):
        vec = hash_embedding("hello", dim=128)
        assert len(vec) == 128

    def test_deterministic(self):
        v1 = hash_embedding("test")
        v2 = hash_embedding("test")
        assert v1 == v2

    def test_different_inputs_different_vectors(self):
        v1 = hash_embedding("hello")
        v2 = hash_embedding("world")
        assert v1 != v2

    def test_normalized(self):
        vec = hash_embedding("test", dim=384)
        norm = sum(v * v for v in vec) ** 0.5
        assert abs(norm - 1.0) < 0.01  # approximately unit norm


class TestEmbeddingRecord:
    def test_defaults(self):
        r = EmbeddingRecord(id="1", text="hello", vector=[0.1, 0.2])
        assert r.wing == ""
        assert r.room == ""
        assert r.metadata == {}

    def test_mempalace_taxonomy(self):
        r = EmbeddingRecord(
            id="1",
            text="hello",
            vector=[0.1],
            wing="docs",
            room="tool-use",
            source_url="https://example.com",
        )
        assert r.wing == "docs"
        assert r.room == "tool-use"


class TestEmbeddingPipeline:
    def test_embed_page(self):
        pipeline = EmbeddingPipeline(dim=384, chunk_size=100)
        records = pipeline.embed_page(
            url="https://example.com/page",
            content="This is a test page with enough content to create at least one chunk.",
            wing="docs",
            room="testing",
            content_hash="abc123",
        )
        assert len(records) >= 1
        for r in records:
            assert isinstance(r, EmbeddingRecord)
            assert r.wing == "docs"
            assert r.room == "testing"
            assert r.source_url == "https://example.com/page"
            assert len(r.vector) == 384

    def test_embed_page_metadata(self):
        pipeline = EmbeddingPipeline(dim=384, chunk_size=100)
        records = pipeline.embed_page(
            url="https://example.com",
            content="A" * 200,
            metadata={"skill": "crawl-ingest"},
        )
        for r in records:
            assert "chunk_index" in r.metadata
            assert "char_start" in r.metadata
            assert r.metadata.get("skill") == "crawl-ingest"

    def test_search_local_without_store(self):
        pipeline = EmbeddingPipeline()
        results = pipeline.search_local("test query")
        assert results == []

    def test_store_local_without_store(self):
        pipeline = EmbeddingPipeline()
        count = pipeline.store_local([])
        assert count == 0
