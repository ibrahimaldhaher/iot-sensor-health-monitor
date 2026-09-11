"""Data access: the lecture's own values, plus a CSV loader.

The exercise hard-codes two Python lists. Real IoT data arrives as a stream or a
file, so the same readings are also shipped as CSV and loaded through the same
type - the analysis code never learns where the numbers came from.
"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path

from iot_monitor.models import Reading

#: The exact values given in the Lecture 1 programming question.
LECTURE_TEMPERATURE: tuple[float, ...] = (72.0, 75.0, 83.0, 78.0, 85.0)
LECTURE_VIBRATION: tuple[float, ...] = (2.1, 3.0, 6.2, 2.8, 5.5)


def readings_from_lists(
    temperature: Sequence[float],
    vibration: Sequence[float],
) -> list[Reading]:
    """Zip two parallel lists into :class:`Reading` objects.

    Mismatched lengths are a data-integrity error, not something to silently
    truncate with ``zip``: a dropped sample is a decision never made.
    """
    if len(temperature) != len(vibration):
        raise ValueError(
            "temperature and vibration must have the same length "
            f"(got {len(temperature)} and {len(vibration)})"
        )
    return [
        Reading(index=i, temperature_c=float(t), vibration=float(v))
        for i, (t, v) in enumerate(zip(temperature, vibration, strict=True), start=1)
    ]


#: Ready-made readings for the lecture data set.
LECTURE_READINGS: list[Reading] = readings_from_lists(
    LECTURE_TEMPERATURE, LECTURE_VIBRATION
)


def load_readings(path: str | Path) -> list[Reading]:
    """Load readings from a CSV file with ``temperature_c`` and ``vibration``.

    An optional ``index`` column is honoured; otherwise rows are numbered in
    file order.
    """
    path = Path(path)
    readings: list[Reading] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = {"temperature_c", "vibration"} - set(reader.fieldnames or ())
        if missing:
            raise ValueError(
                f"{path} is missing required column(s): {', '.join(sorted(missing))}"
            )
        for position, row in enumerate(reader, start=1):
            readings.append(
                Reading(
                    index=int(row.get("index") or position),
                    temperature_c=float(row["temperature_c"]),
                    vibration=float(row["vibration"]),
                )
            )
    if not readings:
        raise ValueError(f"{path} contains no data rows")
    return readings
