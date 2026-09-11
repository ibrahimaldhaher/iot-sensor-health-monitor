"""Unit tests for the decision logic.

The interesting tests are the boundary ones: the exercise says *greater than*,
so a reading sitting exactly on the limit must stay Normal. Getting that wrong
is the classic off-by-one of threshold monitoring - it turns every machine
running at its rated maximum into a false alarm.
"""

from __future__ import annotations

import pytest

from iot_monitor import (
    LECTURE_READINGS,
    Reading,
    Status,
    Thresholds,
    evaluate_all,
    evaluate_reading,
    mean,
    readings_from_lists,
    summarize,
)


class TestMean:
    def test_matches_the_lecture_values(self) -> None:
        assert mean([72, 75, 83, 78, 85]) == pytest.approx(78.6)
        assert mean([2.1, 3.0, 6.2, 2.8, 5.5]) == pytest.approx(3.92)

    def test_single_value(self) -> None:
        assert mean([42.0]) == pytest.approx(42.0)

    def test_empty_sequence_is_an_error_not_zero(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            mean([])


class TestEvaluateReading:
    def test_within_limits_is_normal(self) -> None:
        result = evaluate_reading(Reading(1, 72.0, 2.1))
        assert result.status is Status.NORMAL
        assert result.breached == ()

    def test_temperature_alone_triggers_abnormal(self) -> None:
        result = evaluate_reading(Reading(1, 83.0, 2.0))
        assert result.status is Status.ABNORMAL
        assert result.breached == ("temperature > 80 C",)

    def test_vibration_alone_triggers_abnormal(self) -> None:
        result = evaluate_reading(Reading(1, 70.0, 6.2))
        assert result.status is Status.ABNORMAL
        assert result.breached == ("vibration > 5",)

    def test_both_rules_are_reported(self) -> None:
        result = evaluate_reading(Reading(1, 85.0, 5.5))
        assert result.status is Status.ABNORMAL
        assert len(result.breached) == 2

    @pytest.mark.parametrize(
        ("temperature", "vibration", "expected"),
        [
            (80.0, 5.0, Status.NORMAL),   # exactly on both limits -> still Normal
            (80.1, 5.0, Status.ABNORMAL),
            (80.0, 5.01, Status.ABNORMAL),
            (79.999, 4.999, Status.NORMAL),
        ],
    )
    def test_boundaries_use_strictly_greater_than(
        self, temperature: float, vibration: float, expected: Status
    ) -> None:
        assert evaluate_reading(Reading(1, temperature, vibration)).status is expected

    def test_custom_thresholds_change_the_verdict(self) -> None:
        reading = Reading(1, 78.0, 2.8)
        assert evaluate_reading(reading).status is Status.NORMAL
        tighter = Thresholds(temperature_c=75.0, vibration=2.5)
        assert evaluate_reading(reading, tighter).status is Status.ABNORMAL


class TestSummary:
    def test_lecture_dataset(self) -> None:
        summary = summarize(evaluate_all(LECTURE_READINGS))
        assert summary.count == 5
        assert summary.average_temperature_c == pytest.approx(78.6)
        assert summary.average_vibration == pytest.approx(3.92)
        assert summary.abnormal_count == 2      # readings 3 and 5
        assert summary.normal_count == 3
        assert summary.abnormal_rate == pytest.approx(0.4)

    def test_empty_batch_is_reported_as_empty(self) -> None:
        summary = summarize([])
        assert summary.count == 0
        assert summary.abnormal_count == 0
        assert summary.abnormal_rate == 0.0

    def test_order_is_preserved(self) -> None:
        evaluations = evaluate_all(LECTURE_READINGS)
        assert [e.reading.index for e in evaluations] == [1, 2, 3, 4, 5]


class TestReadingsFromLists:
    def test_builds_one_reading_per_sample(self) -> None:
        readings = readings_from_lists([70, 90], [1.0, 2.0])
        assert [r.index for r in readings] == [1, 2]
        assert readings[1].temperature_c == 90.0

    def test_mismatched_lengths_are_rejected(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            readings_from_lists([70, 90], [1.0])


class TestThresholds:
    @pytest.mark.parametrize(("temp", "vib"), [(0, 5.0), (-1, 5.0), (80.0, 0)])
    def test_non_positive_limits_are_rejected(self, temp: float, vib: float) -> None:
        with pytest.raises(ValueError):
            Thresholds(temperature_c=temp, vibration=vib)
