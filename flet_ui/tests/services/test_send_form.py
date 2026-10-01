"""Tests for mapping Send Data form text to a request."""

from __future__ import annotations

from pathlib import Path

import pytest

from pydaq.core.acquisition import DeviceFamily
from services.send_form import build_send_request, parse_output_range


def test_form_maps_arduino_labels_to_request_without_range() -> None:
    request = build_send_request(
        DeviceFamily.ARDUINO, "COM3 · Arduino Uno", "D2, D3", "/tmp/data.dat", "0,5", "Off"
    )

    assert request.device == "COM3"
    assert request.channels == ("D2", "D3")
    assert request.data_path == Path("/tmp/data.dat")
    assert request.sample_period_s == 0.5
    assert request.plot_mode == "Off"
    assert request.output_range is None


def test_form_expands_home_in_data_path() -> None:
    request = build_send_request(
        DeviceFamily.NIDAQ, "Dev1", "ao0", "~/data.dat", "1", "Off", ("0", "5")
    )

    assert request.data_path == Path.home() / "data.dat"
    assert request.output_range == (0.0, 5.0)


@pytest.mark.parametrize(
    ("path", "period", "message"),
    [
        ("  ", "1", "Choose the data file to send."),
        ("data.dat", "0", "Sample period must be greater than zero, not '0'."),
    ],
)
def test_form_rejects_missing_file_or_period(path: str, period: str, message: str) -> None:
    with pytest.raises(ValueError, match=message.replace(".", r"\.")):
        build_send_request(DeviceFamily.ARDUINO, "COM3", "D2", path, period, "Off")


def test_form_requires_an_output_channel() -> None:
    with pytest.raises(ValueError, match="at least one output channel"):
        build_send_request(DeviceFamily.ARDUINO, "COM3", "", "data.dat", "1", "Off")


@pytest.mark.parametrize(
    ("minimum", "maximum", "message"),
    [
        ("low", "5", "Output minimum must be a voltage, not 'low'."),
        ("5", "5", r"Output minimum \(5 V\) must be below the maximum \(5 V\)."),
    ],
)
def test_output_range_rejects_invalid_limits(minimum: str, maximum: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_output_range(minimum, maximum)


def test_output_range_accepts_negative_minimum() -> None:
    assert parse_output_range("-10", "10,5") == (-10.0, 10.5)
