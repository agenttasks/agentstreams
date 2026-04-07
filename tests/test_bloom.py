"""Tests for src/bloom.py — probabilistic bloom filter with persistence."""

from __future__ import annotations

import math

from src.bloom import BloomFilter


class TestBloomFilter:
    """Test the bit-array bloom filter implementation."""

    def test_empty_filter_contains_nothing(self):
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        assert "hello" not in bf
        assert "world" not in bf
        assert len(bf) == 0

    def test_add_and_contains(self):
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        bf.add("hello")
        assert "hello" in bf
        assert len(bf) == 1

    def test_is_new_returns_true_for_new_items(self):
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        assert bf.is_new("first") is True
        assert bf.is_new("second") is True
        # Second call for same item should return False
        assert bf.is_new("first") is False

    def test_add_returns_true_for_new(self):
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        assert bf.add("new_item") is True
        assert bf.add("new_item") is False  # already present

    def test_optimal_size_increases_with_items(self):
        small = BloomFilter._optimal_size(100, 0.01)
        large = BloomFilter._optimal_size(10000, 0.01)
        assert large > small

    def test_optimal_size_increases_with_precision(self):
        rough = BloomFilter._optimal_size(1000, 0.1)
        precise = BloomFilter._optimal_size(1000, 0.001)
        assert precise > rough

    def test_optimal_hashes(self):
        m = BloomFilter._optimal_size(1000, 0.01)
        k = BloomFilter._optimal_hashes(m, 1000)
        assert k >= 1
        # Optimal k ≈ ln(2) * m/n ≈ 0.693 * m/1000
        expected = math.log(2) * m / 1000
        assert abs(k - expected) <= 2

    def test_no_false_negatives(self):
        """Bloom filters must never have false negatives."""
        bf = BloomFilter(expected_items=100, fp_rate=0.01)
        items = [f"item_{i}" for i in range(100)]
        for item in items:
            bf.add(item)
        for item in items:
            assert item in bf, f"False negative for {item}"

    def test_estimated_fp_rate_starts_at_zero(self):
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        assert bf.estimated_fp_rate == 0.0

    def test_estimated_fp_rate_increases_with_items(self):
        bf = BloomFilter(expected_items=100, fp_rate=0.01)
        for i in range(50):
            bf.add(f"item_{i}")
        mid_rate = bf.estimated_fp_rate
        for i in range(50, 100):
            bf.add(f"item_{i}")
        full_rate = bf.estimated_fp_rate
        assert full_rate >= mid_rate

    def test_serialization_roundtrip(self):
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        bf.add("hello")
        bf.add("world")

        data = bf.to_bytes()
        restored = BloomFilter.from_bytes(
            data,
            expected_items=1000,
            fp_rate=0.01,
            num_hashes=bf.num_hashes,
        )

        assert "hello" in restored
        assert "world" in restored
        assert "missing" not in restored

    def test_clear(self):
        bf = BloomFilter(expected_items=100, fp_rate=0.01)
        bf.add("test")
        assert "test" in bf
        bf.clear()
        assert "test" not in bf
        assert len(bf) == 0

    def test_large_item_count(self):
        """Verify filter works with many items without excessive false positives."""
        n = 10_000
        bf = BloomFilter(expected_items=n, fp_rate=0.01)
        for i in range(n):
            bf.add(f"url:https://example.com/page/{i}")

        # Check false positive rate with unseen items
        false_positives = 0
        test_count = 1000
        for i in range(n, n + test_count):
            if f"url:https://example.com/page/{i}" in bf:
                false_positives += 1

        fp_rate = false_positives / test_count
        # Allow 5x the target rate as tolerance
        assert fp_rate < 0.05, f"FP rate {fp_rate} exceeds 5%"

    def test_hash_positions_deterministic(self):
        bf = BloomFilter(expected_items=100, fp_rate=0.01)
        positions1 = bf._hash_positions("test")
        positions2 = bf._hash_positions("test")
        assert positions1 == positions2

    def test_hash_positions_differ_for_different_items(self):
        bf = BloomFilter(expected_items=100, fp_rate=0.01)
        positions1 = bf._hash_positions("hello")
        positions2 = bf._hash_positions("world")
        assert positions1 != positions2
