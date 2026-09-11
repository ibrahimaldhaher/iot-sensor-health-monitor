"""The decision logic: averages, per-reading verdicts, and batch summary."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from iot_monitor.config import DEFAULT_THRESHOLDS, Thresholds
from iot_monitor.models import Evaluation, Reading, Status, Summary


def mean(values: Sequence[float]) -> float:
    """Arithmetic mean.

    Raises ``ValueError`` on an empty sequence rather than returning 0.0: an
    average of "no data" is not zero, and silently returning zero would let a
    dead sensor look like a cold machine.
    """
    if not values:
        raise ValueError("cannot compute the mean of an empty sequence")
    return sum(values) / len(values)


def evaluate_reading(
    reading: Reading,
    thresholds: Thresholds = DEFAULT_THRESHOLDS,
) -> Evaluation:
    """Apply the rule base to one reading.

    Rule (Lecture 1): temperature > 80 C **or** vibration > 5.0 -> Abnormal.
    """
    breached: list[str] = []
    if thresholds.temperature_exceeded(reading.temperature_c):
        breached.append(f"temperature > {thresholds.temperature_c:g} C")
    if thresholds.vibration_exceeded(reading.vibration):
        breached.append(f"vibration > {thresholds.vibration:g}")

    status = Status.ABNORMAL if breached else Status.NORMAL
    return Evaluation(reading=reading, status=status, breached=tuple(breached))


def evaluate_all(
    readings: Iterable[Reading],
    thresholds: Thresholds = DEFAULT_THRESHOLDS,
) -> list[Evaluation]:
    """Evaluate a batch of readings, preserving input order."""
    return [evaluate_reading(r, thresholds) for r in readings]


def summarize(evaluations: Sequence[Evaluation]) -> Summary:
    """Aggregate a batch into the figures the exercise asks to print."""
    if not evaluations:
        return Summary(
            count=0,
            average_temperature_c=0.0,
            average_vibration=0.0,
            abnormal_count=0,
        )

    return Summary(
        count=len(evaluations),
        average_temperature_c=mean([e.reading.temperature_c for e in evaluations]),
        average_vibration=mean([e.reading.vibration for e in evaluations]),
        abnormal_count=sum(1 for e in evaluations if e.is_abnormal),
    )
