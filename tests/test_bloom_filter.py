"""Tests for the bloom filter deduplication module."""

from agentstreams.bloom.filter import BloomFilter


def test_basic_add_and_contains():
    bf = BloomFilter(capacity=1000, fp_rate=0.01)
    assert "https://example.com" not in bf
    was_present = bf.add("https://example.com")
    assert not was_present
    assert "https://example.com" in bf


def test_duplicate_detection():
    bf = BloomFilter(capacity=1000, fp_rate=0.01)
    bf.add("https://example.com/page1")
    was_present = bf.add("https://example.com/page1")
    assert was_present


def test_count():
    bf = BloomFilter(capacity=1000, fp_rate=0.01)
    bf.add("url1")
    bf.add("url2")
    bf.add("url3")
    bf.add("url1")  # duplicate
    assert bf.count == 3


def test_serialization_roundtrip():
    bf = BloomFilter(capacity=5000, fp_rate=0.001)
    for i in range(100):
        bf.add(f"https://example.com/page-{i}")

    data = bf.to_bytes()
    bf2 = BloomFilter.from_bytes(data)

    assert bf2.count == bf.count
    assert bf2.capacity == bf.capacity
    # All items should still be present
    for i in range(100):
        assert f"https://example.com/page-{i}" in bf2


def test_merge():
    bf1 = BloomFilter(capacity=1000, fp_rate=0.01)
    bf2 = BloomFilter(capacity=1000, fp_rate=0.01)

    bf1.add("url1")
    bf1.add("url2")
    bf2.add("url3")
    bf2.add("url4")

    bf1.merge(bf2)

    assert "url1" in bf1
    assert "url2" in bf1
    assert "url3" in bf1
    assert "url4" in bf1


def test_stats():
    bf = BloomFilter(capacity=10000, fp_rate=0.001)
    for i in range(50):
        bf.add(f"url-{i}")

    stats = bf.stats()
    assert stats["capacity"] == 10000
    assert stats["count"] == 50
    assert stats["target_fp_rate"] == 0.001
    assert stats["fill_ratio"] > 0
    assert stats["estimated_fp_rate"] < stats["target_fp_rate"]


def test_false_positive_rate():
    """Empirical false positive rate should be near the target."""
    bf = BloomFilter(capacity=1000, fp_rate=0.01)
    for i in range(1000):
        bf.add(f"item-{i}")

    # Check items never added
    false_positives = sum(1 for i in range(1000, 11000) if f"item-{i}" in bf)
    fp_rate = false_positives / 10000
    # Should be within 3x of target (generous for small sample)
    assert fp_rate < 0.03, f"FP rate {fp_rate} too high (target 0.01)"
