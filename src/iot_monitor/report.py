"""Human-readable output. Formatting is kept away from the decision logic."""

from __future__ import annotations

from collections.abc import Sequence

from iot_monitor.models import Evaluation, Summary

_HEADERS = ("#", "Temperature (C)", "Vibration", "Status", "Reason")


def format_table(evaluations: Sequence[Evaluation]) -> str:
    """Render per-reading verdicts as a fixed-width table."""
    rows = [
        (
            str(e.reading.index),
            f"{e.reading.temperature_c:.1f}",
            f"{e.reading.vibration:.2f}",
            e.status.value,
            e.reason,
        )
        for e in evaluations
    ]
    widths = [
        max(len(header), *(len(row[col]) for row in rows)) if rows else len(header)
        for col, header in enumerate(_HEADERS)
    ]

    def line(cells: Sequence[str]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    separator = "  ".join("-" * w for w in widths)
    return "\n".join([line(_HEADERS), separator, *(line(row) for row in rows)])


def format_summary(summary: Summary) -> str:
    """Render the aggregate figures requested by the exercise."""
    return "\n".join(
        [
            f"Readings analysed      : {summary.count}",
            f"Average temperature    : {summary.average_temperature_c:.2f} C",
            f"Average vibration      : {summary.average_vibration:.2f}",
            f"Normal measurements    : {summary.normal_count}",
            f"Abnormal measurements  : {summary.abnormal_count}"
            f" ({summary.abnormal_rate:.0%} of the batch)",
        ]
    )


def format_report(evaluations: Sequence[Evaluation], summary: Summary) -> str:
    """Full report: the per-reading table followed by the summary block."""
    return "\n\n".join(
        [
            "PER-READING STATUS",
            format_table(evaluations),
            "SUMMARY",
            format_summary(summary),
        ]
    )
