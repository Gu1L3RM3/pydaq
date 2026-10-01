"""Hardware-free acquisition source for demos and UI development."""

from __future__ import annotations

import math
import time
from collections.abc import Callable

from pydaq.core.acquisition import AcquisitionConfig, SampleBatch

# (amplitude V, phase offset s) per channel index, cycling; matches the
# reference signals in the design package.
_WAVEFORMS = ((4.0, 8.0), (1.9, 12.0))
_PERIOD_S = 35.0


def simulated_voltage(channel_index: int, time_s: float) -> float:
    amplitude, offset = _WAVEFORMS[channel_index % len(_WAVEFORMS)]
    return amplitude * math.sin((time_s - offset) * math.tau / _PERIOD_S)


class SimulatedSource:
    """Sine-wave ``AcquisitionSource`` paced like a real device.

    ``sleep`` is injectable so tests run instantly.
    """

    def __init__(
        self, batch_size: int = 10, sleep: Callable[[float], None] = time.sleep
    ) -> None:
        if batch_size < 1:
            raise ValueError(f"batch_size must be at least 1, received {batch_size}")
        self._batch_size = batch_size
        self._sleep = sleep
        self._config: AcquisitionConfig | None = None
        self._next_index = 0

    def start(self, config: AcquisitionConfig) -> None:
        self._config = config
        self._next_index = 0

    def read_batch(self) -> SampleBatch | None:
        config = self._config
        if config is None or self._next_index >= config.sample_count:
            return None
        end = min(self._next_index + self._batch_size, config.sample_count)
        indexes = range(self._next_index, end)
        self._next_index = end
        self._sleep(len(indexes) * config.sample_period_s)
        times = tuple(index * config.sample_period_s for index in indexes)
        return SampleBatch(
            times_s=times,
            channel_values={
                channel: tuple(simulated_voltage(position, t) for t in times)
                for position, channel in enumerate(config.channels)
            },
        )

    def stop(self) -> None:
        self._config = None
