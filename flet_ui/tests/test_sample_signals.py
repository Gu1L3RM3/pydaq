"""Tests for the static placeholder chart curves."""

from __future__ import annotations

import pytest

from components.charts.sample_signals import sample_signals, sample_times
from components.charts.signal_plot import SignalPlot


def test_sample_times_span_the_whole_duration() -> None:
    times = sample_times(10, points=5)

    assert times == (0.0, 2.5, 5.0, 7.5, 10.0)


def test_sample_times_reject_empty_duration() -> None:
    with pytest.raises(ValueError, match="duration_s must be positive"):
        sample_times(0)


@pytest.mark.parametrize("value_range", [(-6.0, 6.0), (0.0, 6.0), (-10.0, 2.0)])
def test_sample_signals_stay_inside_value_range(value_range: tuple[float, float]) -> None:
    times, values = sample_signals(("A0", "A1", "A2"), 30, value_range)

    low, high = value_range
    assert set(values) == {"A0", "A1", "A2"}
    assert all(len(curve) == len(times) for curve in values.values())
    assert all(low <= value <= high for curve in values.values() for value in curve)


def test_sample_signals_are_static() -> None:
    assert sample_signals(("y",), 10, (0, 5)) == sample_signals(("y",), 10, (0, 5))


def test_signal_plot_show_sample_fills_every_series() -> None:
    plot = SignalPlot(("u", "y"), y_range=(0, 6), duration_s=20)

    plot.show_sample()

    assert all(len(series.points) == 200 for series in plot._chart.data_series)
    assert all(point.x <= 20 for point in plot._chart.data_series[0].points)
    assert plot._empty_hint.visible is False
