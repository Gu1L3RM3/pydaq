"""Tests for signal plot state and live chart status transitions."""

from __future__ import annotations

from components.charts.signal_plot import SignalPlot
from components.charts.status_badge import SessionStatus, StatusBadge
from components.live_chart import LiveSignalChart
from pydaq.core.acquisition import AcquisitionConfig, DeviceFamily, SampleBatch


def _point_counts(plot: SignalPlot) -> list[int]:
    return [len(series.points) for series in plot._chart.data_series]


def test_signal_plot_appends_known_series_only() -> None:
    plot = SignalPlot(("y",))

    plot.append((0.0, 0.1), {"y": (1.0, 2.0), "unknown": (3.0, 4.0)})

    assert _point_counts(plot) == [2]
    assert plot._empty_hint.visible is False


def test_signal_plot_set_points_replaces_previous_result() -> None:
    plot = SignalPlot(("u", "y"))
    plot.append((0.0,), {"u": (1.0,), "y": (1.0,)})

    plot.set_points((0.0, 1.0, 2.0), {"u": (0.0, 1.0, 1.0)})

    assert _point_counts(plot) == [3, 0]


def test_signal_plot_set_series_resets_legend_and_hint() -> None:
    plot = SignalPlot(("A0",))
    plot.append((0.0,), {"A0": (1.0,)})

    plot.set_series(("Setpoint", "y", "u"))

    assert plot.series_names == ("Setpoint", "y", "u")
    assert len(plot._legend.controls) == 6
    assert plot._empty_hint.visible is True


def test_status_badge_starts_idle_with_custom_running_label() -> None:
    badge = StatusBadge(running_label="Sending")

    badge.set_status(SessionStatus.RUNNING)

    assert badge._label.value == "Sending"


def test_live_chart_keeps_error_until_next_reset() -> None:
    chart = LiveSignalChart()
    config = AcquisitionConfig(DeviceFamily.ARDUINO, "COM3", ("A0",), 0.1, 1.0)

    chart.set_acquiring(True)
    chart.show_error()
    chart.set_acquiring(False)
    assert chart.status.status is SessionStatus.ERROR

    chart.reset(config)
    assert chart.status.status is SessionStatus.IDLE


def test_live_chart_plots_batches_for_reset_channels() -> None:
    chart = LiveSignalChart()
    chart.reset(AcquisitionConfig(DeviceFamily.NIDAQ, "Dev1", ("ai0",), 0.1, 1.0))

    chart.append_batch(SampleBatch((0.0, 0.1), {"ai0": (1.0, 2.0)}))

    assert chart.plot.series_names == ("ai0",)
    assert _point_counts(chart.plot) == [2]
