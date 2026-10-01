"""Acquisition configuration in, sample batches out, with no plotting.

Example::

    config = AcquisitionConfig(
        DeviceFamily.ARDUINO, "COM3", ("A0", "A1"), sample_period_s=0.01, duration_s=10
    )
    source.start(config)
    while (batch := source.read_batch()) is not None:
        consume(batch)
    source.stop()
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol


class DeviceFamily(str, Enum):
    ARDUINO = "arduino"
    NIDAQ = "nidaq"


@dataclass(frozen=True)
class AcquisitionConfig:
    device_family: DeviceFamily
    device: str
    channels: tuple[str, ...]
    sample_period_s: float
    duration_s: float
    save_path: Path | None = None

    def __post_init__(self) -> None:
        if not self.device:
            raise ValueError("device must be a non-empty name such as 'COM3' or 'Dev1'")
        if not self.channels:
            raise ValueError("channels must contain at least one channel name")
        if self.sample_period_s <= 0:
            raise ValueError(
                f"sample_period_s must be positive, received {self.sample_period_s}"
            )
        if self.duration_s < self.sample_period_s:
            raise ValueError(
                f"duration_s must be at least sample_period_s ({self.sample_period_s}), "
                f"received {self.duration_s}"
            )

    @property
    def sample_count(self) -> int:
        return round(self.duration_s / self.sample_period_s)


@dataclass(frozen=True)
class SampleBatch:
    """Consecutive samples; ``channel_values`` aligns index-wise with ``times_s``."""

    times_s: tuple[float, ...]
    channel_values: Mapping[str, tuple[float, ...]]

    def __post_init__(self) -> None:
        for channel, values in self.channel_values.items():
            if len(values) != len(self.times_s):
                raise ValueError(
                    f"channel {channel!r} has {len(values)} values, "
                    f"expected {len(self.times_s)} to match times_s"
                )


class AcquisitionSource(Protocol):
    """A device that streams samples; ``read_batch`` blocks until data arrives."""

    def start(self, config: AcquisitionConfig) -> None: ...

    def read_batch(self) -> SampleBatch | None:
        """Return the next batch, or ``None`` once the session duration is reached."""
        ...

    def stop(self) -> None: ...
