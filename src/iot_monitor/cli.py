"""Command-line entry point.

    python -m iot_monitor
    python -m iot_monitor --csv data/lecture1_readings.csv
    python -m iot_monitor --temperature-limit 78 --vibration-limit 4.5 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from iot_monitor.analysis import evaluate_all, summarize
from iot_monitor.config import (
    DEFAULT_TEMPERATURE_LIMIT_C,
    DEFAULT_VIBRATION_LIMIT,
    Thresholds,
)
from iot_monitor.data import LECTURE_READINGS, load_readings
from iot_monitor.report import format_report

EXIT_OK = 0
EXIT_ABNORMAL = 1
EXIT_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iot-monitor",
        description=(
            "Rule-based Normal/Abnormal monitoring of industrial motor readings "
            "(Lecture 1 - Advanced Distributed Computing / ML for IoT)."
        ),
    )
    parser.add_argument(
        "--csv",
        metavar="PATH",
        help="CSV with temperature_c and vibration columns "
        "(default: the readings given in the lecture).",
    )
    parser.add_argument(
        "--temperature-limit",
        type=float,
        default=DEFAULT_TEMPERATURE_LIMIT_C,
        metavar="C",
        help=f"Abnormal above this value (default: {DEFAULT_TEMPERATURE_LIMIT_C:g}).",
    )
    parser.add_argument(
        "--vibration-limit",
        type=float,
        default=DEFAULT_VIBRATION_LIMIT,
        metavar="V",
        help=f"Abnormal above this value (default: {DEFAULT_VIBRATION_LIMIT:g}).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a text report.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the monitor. Returns 1 when any reading is abnormal, 2 on error."""
    args = build_parser().parse_args(argv)

    try:
        readings = load_readings(args.csv) if args.csv else LECTURE_READINGS
        thresholds = Thresholds(
            temperature_c=args.temperature_limit,
            vibration=args.vibration_limit,
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_ERROR

    evaluations = evaluate_all(readings, thresholds)
    summary = summarize(evaluations)

    if args.json:
        print(
            json.dumps(
                {
                    "thresholds": {
                        "temperature_c": thresholds.temperature_c,
                        "vibration": thresholds.vibration,
                    },
                    "readings": [
                        {
                            "index": e.reading.index,
                            "temperature_c": e.reading.temperature_c,
                            "vibration": e.reading.vibration,
                            "status": e.status.value,
                            "breached": list(e.breached),
                        }
                        for e in evaluations
                    ],
                    "summary": {
                        "count": summary.count,
                        "average_temperature_c": round(
                            summary.average_temperature_c, 4
                        ),
                        "average_vibration": round(summary.average_vibration, 4),
                        "normal": summary.normal_count,
                        "abnormal": summary.abnormal_count,
                    },
                },
                indent=2,
            )
        )
    else:
        print(format_report(evaluations, summary))

    return EXIT_ABNORMAL if summary.abnormal_count else EXIT_OK


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
