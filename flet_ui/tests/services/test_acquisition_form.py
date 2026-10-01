"""Tests for mapping acquisition form text to a config."""

from __future__ import annotations

import pytest

from pydaq.core.acquisition import DeviceFamily
from services.acquisition_form import build_acquisition_config


def test_form_maps_labels_and_numbers_to_config() -> None:
    config = build_acquisition_config(
        DeviceFamily.ARDUINO, "COM3 · Arduino Uno", "A0, A1", "0,010", "100"
    )

    assert config.device == "COM3"
    assert config.channels == ("A0", "A1")
    assert config.sample_period_s == 0.01
    assert config.duration_s == 100


@pytest.mark.parametrize(
    ("period", "duration", "message"),
    [
        ("fast", "100", "Sample period must be a number of seconds, not 'fast'."),
        ("0", "100", "Sample period must be greater than zero, not '0'."),
        ("0.01", "", "Session duration must be a number of seconds, not ''."),
        ("2", "1", "Session duration must be at least one sample period."),
    ],
)
def test_form_rejects_invalid_numbers_with_user_message(
    period: str, duration: str, message: str
) -> None:
    with pytest.raises(ValueError, match=message.replace(".", r"\.")):
        build_acquisition_config(DeviceFamily.NIDAQ, "Dev1", "ai0", period, duration)
