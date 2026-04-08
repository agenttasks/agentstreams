"""Tests for scripts/generate-timeseries.py — time-series data generators."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Import using importlib since filename has hyphens
from importlib import import_module

mod = import_module("generate-timeseries")
hour_of_day = mod.hour_of_day
daily_wave = mod.daily_wave
gen_counter = mod.gen_counter
gen_timer = mod.gen_timer
gen_gauge = mod.gen_gauge
gen_distribution = mod.gen_distribution
escape_sql = mod.escape_sql
METRICS = mod.METRICS
TOTAL_STEPS = mod.TOTAL_STEPS


class TestHourOfDay:
    def test_midnight(self):
        assert hour_of_day(0) == 0.0

    def test_noon(self):
        assert hour_of_day(12 * 60) == 12.0

    def test_wraps_at_24h(self):
        assert hour_of_day(24 * 60) == 0.0

    def test_fractional(self):
        assert hour_of_day(90) == 1.5  # 1.5 hours


class TestDailyWave:
    def test_returns_around_base(self):
        val = daily_wave(0, 10.0, 5.0)
        assert 5.0 <= val <= 15.0

    def test_peak_at_afternoon(self):
        # Peak should be around step for ~15:00 (hour 15)
        val_afternoon = daily_wave(15 * 60, 10.0, 5.0)
        val_morning = daily_wave(6 * 60, 10.0, 5.0)
        assert val_afternoon > val_morning


class TestGenCounter:
    def test_positive_rate(self):
        val = gen_counter(100, {"status": "200"})
        assert val >= 0

    def test_low_rate_for_429(self):
        # 429 rate-limits should be lower on average
        vals_429 = [gen_counter(i * 60, {"status": "429"}) for i in range(100)]
        vals_200 = [gen_counter(i * 60, {"status": "200"}) for i in range(100)]
        avg_429 = sum(vals_429) / len(vals_429)
        avg_200 = sum(vals_200) / len(vals_200)
        assert avg_429 < avg_200


class TestGenTimer:
    def test_positive_duration(self):
        val = gen_timer(100, {"stage": "extract"})
        assert val > 0

    def test_stage_baseline_varies(self):
        # Extract should be slower than transform on average
        vals_extract = [gen_timer(i * 60, {"stage": "extract"}) for i in range(100)]
        vals_transform = [gen_timer(i * 60, {"stage": "transform"}) for i in range(100)]
        avg_extract = sum(vals_extract) / len(vals_extract)
        avg_transform = sum(vals_transform) / len(vals_transform)
        assert avg_extract > avg_transform


class TestGenGauge:
    def test_bloom_fpr_bounded(self):
        val = gen_gauge(100, {"method": "bloom"})
        assert 0 <= val <= 1

    def test_exact_near_zero(self):
        vals = [gen_gauge(i, {"method": "exact"}) for i in range(100)]
        avg = sum(vals) / len(vals)
        assert avg < 0.02

    def test_eval_score_high(self):
        val = gen_gauge(100, {"assertion_type": "is-json"})
        assert 0 <= val <= 1


class TestGenDistribution:
    def test_positive_cost(self):
        val = gen_distribution(100, {"model": "claude-opus-4-6"})
        assert val > 0

    def test_opus_more_expensive(self):
        vals_opus = [gen_distribution(i, {"model": "claude-opus-4-6"}) for i in range(200)]
        vals_haiku = [
            gen_distribution(i, {"model": "claude-haiku-4-5-20251001"}) for i in range(200)
        ]
        assert sum(vals_opus) / len(vals_opus) > sum(vals_haiku) / len(vals_haiku)

    def test_mythos_most_expensive(self):
        vals_mythos = [gen_distribution(i, {"model": "claude-mythos-preview"}) for i in range(200)]
        vals_opus = [gen_distribution(i, {"model": "claude-opus-4-6"}) for i in range(200)]
        assert sum(vals_mythos) / len(vals_mythos) > sum(vals_opus) / len(vals_opus)


class TestEscapeSql:
    def test_escapes_single_quotes(self):
        assert escape_sql("it's") == "it''s"

    def test_no_change_clean(self):
        assert escape_sql("clean") == "clean"


class TestMetricsConfig:
    def test_ten_metrics_defined(self):
        assert len(METRICS) == 10

    def test_all_have_type(self):
        for name, config in METRICS.items():
            assert "type" in config, f"{name} missing type"

    def test_all_have_tags_combos(self):
        for name, config in METRICS.items():
            assert "tags_combos" in config, f"{name} missing tags_combos"
            assert len(config["tags_combos"]) > 0, f"{name} has empty tags_combos"

    def test_total_series_count(self):
        total = sum(len(c["tags_combos"]) for c in METRICS.values())
        assert total == 48  # 33 original + 11 task metrics + 4 mythos-preview
