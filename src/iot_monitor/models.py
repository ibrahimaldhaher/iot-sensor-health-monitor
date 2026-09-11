"""Domain types: what a reading is, what a verdict is, what a summary is."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Status(str, Enum):
    """Machine state derived from a single measurement vector."""

    NORMAL = "Normal"
    ABNORMAL = "Abnormal"

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return self.value


@dataclass(frozen=True, slots=True)
class Reading:
    """One measurement vector x_t = [T_t, V_t] taken at a point in time.

    ``index`` is the 1-based sample number, so printed reports match the order
    the sensor produced the values in.
    """

    index: int
    temperature_c: float
    vibration: float

    def __post_init__(self) -> None:
        if self.index < 1:
            raise ValueError("index is 1-based and must be >= 1")


@dataclass(frozen=True, slots=True)
class Evaluation:
    """A reading plus the verdict and the reason for it.

    ``breached`` records *which* rule fired. A status without a reason is not
    actionable: a maintenance team needs to know whether the motor is running
    hot or shaking, not merely that something is wrong.
    """

    reading: Reading
    status: Status
    breached: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_abnormal(self) -> bool:
        return self.status is Status.ABNORMAL

    @property
    def reason(self) -> str:
        return ", ".join(self.breached) if self.breached else "within limits"


@dataclass(frozen=True, slots=True)
class Summary:
    """Aggregate answers required by the exercise."""

    count: int
    average_temperature_c: float
    average_vibration: float
    abnormal_count: int

    @property
    def normal_count(self) -> int:
        return self.count - self.abnormal_count

    @property
    def abnormal_rate(self) -> float:
        """Share of abnormal readings in [0, 1]; 0.0 for an empty batch."""
        return self.abnormal_count / self.count if self.count else 0.0
