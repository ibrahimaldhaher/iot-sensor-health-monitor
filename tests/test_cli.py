"""End-to-end tests for the command-line interface and the CSV loader."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from iot_monitor.cli import EXIT_ABNORMAL, EXIT_ERROR, EXIT_OK, main
from iot_monitor.data import load_readings

DATA = Path(__file__).resolve().parents[1] / "data" / "lecture1_readings.csv"


def test_csv_matches_the_hard_coded_lecture_values() -> None:
    readings = load_readings(DATA)
    assert [r.temperature_c for r in readings] == [72.0, 75.0, 83.0, 78.0, 85.0]
    assert [r.vibration for r in readings] == [2.1, 3.0, 6.2, 2.8, 5.5]


def test_missing_column_is_reported(tmp_path: Path) -> None:
    bad = tmp_path / "bad.csv"
    bad.write_text("temperature_c\n72\n", encoding="utf-8")
    with pytest.raises(ValueError, match="vibration"):
        load_readings(bad)


def test_empty_file_is_reported(tmp_path: Path) -> None:
    empty = tmp_path / "empty.csv"
    empty.write_text("index,temperature_c,vibration\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no data rows"):
        load_readings(empty)


def test_default_run_reports_two_abnormal(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main([])
    out = capsys.readouterr().out
    assert exit_code == EXIT_ABNORMAL
    assert "Abnormal measurements  : 2" in out
    assert "78.60 C" in out


def test_json_output_is_valid(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["abnormal"] == 2
    assert payload["summary"]["average_vibration"] == pytest.approx(3.92)
    assert len(payload["readings"]) == 5


def test_relaxed_thresholds_make_the_batch_clean(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["--temperature-limit", "120", "--vibration-limit", "10"])
    capsys.readouterr()
    assert exit_code == EXIT_OK


def test_missing_file_exits_with_error(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--csv", "does-not-exist.csv"])
    assert exit_code == EXIT_ERROR
    assert "error:" in capsys.readouterr().err
