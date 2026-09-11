"""Decision thresholds.

Keeping the thresholds in one immutable object - instead of hard-coding 80 and
5.0 at the comparison site - is what lets the same logic be re-tuned per machine
without touching the decision code, and what makes the boundary cases testable.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Values from Lecture 1, section 1.22.
DEFAULT_TEMPERATURE_LIMIT_C = 80.0
DEFAULT_VIBRATION_LIMIT = 5.0


@dataclass(frozen=True, slots=True)
class Thresholds:
    """Upper limits above which a measurement is considered abnormal.

    The comparison is *strictly greater than*: a reading exactly equal to the
    limit is still Normal, matching the wording of the exercise
    ("Temperature > 80 C -> Abnormal").
    """

    temperature_c: float = DEFAULT_TEMPERATURE_LIMIT_C
    vibration: float = DEFAULT_VIBRATION_LIMIT

    def __post_init__(self) -> None:
        if self.temperature_c <= 0:
            raise ValueError("temperature_c must be positive")
        if self.vibration <= 0:
            raise ValueError("vibration must be positive")

    def temperature_exceeded(self, value: float) -> bool:
        return value > self.temperature_c

    def vibration_exceeded(self, value: float) -> bool:
        return value > self.vibration


DEFAULT_THRESHOLDS = Thresholds()
