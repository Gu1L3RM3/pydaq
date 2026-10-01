"""Tests for the UI-agnostic acquisition interface and simulated source."""

from __future__ import annotations

import pytest

from pydaq.core.acquisition import AcquisitionConfig, DeviceFamily, SampleBatch
from pydaq.devices.simulated import SimulatedSource, simulated_voltage


class RecordingSleep:
    """Fake clock that records requested pauses instead of sleeping."""

    def __init__(self) -> None:
        self.durations: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.durations.append(seconds)


def make_config(**overrides: object) -> AcquisitionConfig:
    fields = {
        "device_family": DeviceFamily.ARDUINO,
        "device": "COM3",
        "channels": ("A0", "A1"),
        "sample_period_s": 0.5,
        "duration_s": 2.0,
    }
    fields.update(overrides)
    return AcquisitionConfig(**fields)


def test_config_derives_sample_count() -> None:
    assert make_config(sample_period_s=0.01, duration_s=100).sample_count == 10_000


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"device": ""}, "device must be a non-empty name"),
        ({"channels": ()}, "channels must contain at least one"),
        ({"sample_period_s": 0}, "sample_period_s must be positive, received 0"),
        ({"duration_s": 0.1}, r"duration_s must be at least sample_period_s \(0.5\)"),
    ],
)
def test_config_rejects_invalid_values(overrides: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        make_config(**overrides)


def test_sample_batch_rejects_misaligned_channel() -> None:
    with pytest.raises(ValueError, match="channel 'A0' has 1 values, expected 2"):
        SampleBatch(times_s=(0.0, 0.1), channel_values={"A0": (1.0,)})


def test_simulated_source_streams_whole_session_in_batches() -> None:
    sleep = RecordingSleep()
    source = SimulatedSource(batch_size=3, sleep=sleep)
    source.start(make_config())

    batches = []
    while (batch := source.read_batch()) is not None:
        batches.append(batch)

    assert [batch.times_s for batch in batches] == [(0.0, 0.5, 1.0), (1.5,)]
    assert sleep.durations == [1.5, 0.5]
    assert batches[0].channel_values["A1"][0] == simulated_voltage(1, 0.0)


def test_simulated_source_returns_nothing_after_stop() -> None:
    source = SimulatedSource(sleep=RecordingSleep())
    source.start(make_config())
    source.stop()

    assert source.read_batch() is None


def test_simulated_source_rejects_empty_batches() -> None:
    with pytest.raises(ValueError, match="batch_size must be at least 1, received 0"):
        SimulatedSource(batch_size=0)
