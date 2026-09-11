"""IoT sensor health monitoring.

Reference implementation for the programming exercise of Lecture 1,
*Introduction to Machine Learning, Deep Learning and IoT*
(MSc in Computer Science / IoT, University of Sumer, 2026-2027).

The exercise asks for averages and a rule-based Normal/Abnormal decision over
temperature and vibration measurements. This package implements that rule as a
small, testable domain model so the same code can run in a notebook, from the
command line, or inside an edge service.
"""

from iot_monitor.analysis import evaluate_all, evaluate_reading, mean, summarize
from iot_monitor.config import Thresholds
from iot_monitor.data import LECTURE_READINGS, load_readings, readings_from_lists
from iot_monitor.models import Evaluation, Reading, Status, Summary

__all__ = [
    "LECTURE_READINGS",
    "Evaluation",
    "Reading",
    "Status",
    "Summary",
    "Thresholds",
    "evaluate_all",
    "evaluate_reading",
    "load_readings",
    "mean",
    "readings_from_lists",
    "summarize",
]

__version__ = "1.0.0"
