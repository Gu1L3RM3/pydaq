"""Static placeholder curves shown in charts until pages reach the backend.

Every chart page shows these instead of live data during the UI-only phase::

    times, values = sample_signals(("A0", "A1"), duration_s=100, value_range=(-6, 6))
    plot.set_points(times, values)
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from components.charts.axes import ValueRange

# (fraction of the half range, phase as a fraction of the duration) per series,
# cycling; at 100 s and ±6 V they match the design package's A0/A1 curves.
_SAMPLE_WAVES = ((0.67, 0.08), (0.32, 0.12))
_PERIOD_FRACTION = 0.35
_SAMPLE_POINTS = 200

SampleValues = dict[str, tuple[float, ...]]


def sample_times(duration_s: float, points: int = _SAMPLE_POINTS) -> tuple[float, ...]:
    if duration_s <= 0 or points < 2:
        raise ValueError(
            f"duration_s must be positive and points at least 2, "
            f"received duration_s={duration_s}, points={points}"
        )
    step = duration_s / (points - 1)
    return tuple(index * step for index in range(points))


def sample_wave(
    index: int, times: Sequence[float], duration_s: float, value_range: ValueRange
) -> tuple[float, ...]:
    """One sine centered in ``value_range``; ``index`` picks its amplitude and phase."""
    fraction, phase = _SAMPLE_WAVES[index % len(_SAMPLE_WAVES)]
    low, high = value_range
    center, amplitude = (low + high) / 2, fraction * (high - low) / 2
    period = _PERIOD_FRACTION * duration_s
    return tuple(
        center + amplitude * math.sin((time - phase * duration_s) * math.tau / period)
        for time in times
    )


def sample_signals(
    names: Sequence[str], duration_s: float, value_range: ValueRange
) -> tuple[tuple[float, ...], SampleValues]:
    """Placeholder times and one curve per name, all inside ``value_range``."""
    times = sample_times(duration_s)
    values = {
        name: sample_wave(index, times, duration_s, value_range)
        for index, name in enumerate(names)
    }
    return times, values
