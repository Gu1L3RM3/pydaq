"""Line plot of named signals over time, with legend and empty state."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import flet as ft
import flet_charts as fch

from components.charts.axes import (
    ValueRange,
    axis_labels,
    channel_color,
    tick_interval,
    time_axis_ticks,
    value_axis_ticks,
)
from components.charts.sample_signals import sample_signals
from components.mounting import update_if_mounted
from theme import (
    BORDER,
    CHART_HEIGHT,
    MUTED,
    NAVY,
    SPACE_MD,
    TEXT_LABEL,
    TEXT_SMALL,
)

SeriesValues = Mapping[str, Sequence[float]]


class SignalPlot(ft.Column):
    """Time-based line chart; streaming via ``append``, results via ``set_points``.

    Example (PID result with setpoint, output and control effort)::

        plot = SignalPlot(("Setpoint", "y", "u"), y_range=(0, 5), y_label="Voltage (V)")
        plot.set_points(times, {"Setpoint": sp, "y": output, "u": effort})
    """

    def __init__(
        self,
        series: Sequence[str] = (),
        y_range: ValueRange = (-6, 6),
        y_label: str = "Voltage (V)",
        x_label: str = "Time (s)",
        duration_s: float = 100.0,
        height: float = CHART_HEIGHT,
        empty_hint: str = "Start an acquisition to stream data here.",
    ) -> None:
        self._series: dict[str, fch.LineChartData] = {}
        self._y_range = y_range
        self._duration_s = duration_s
        self._chart = _build_chart(y_range, y_label, x_label, duration_s)
        self._legend = ft.Row(spacing=SPACE_MD, alignment=ft.MainAxisAlignment.END)
        self._empty_hint = ft.Text(empty_hint, size=TEXT_LABEL, color=MUTED)
        self._apply_series(series)
        plot = ft.Stack(
            controls=[
                self._chart,
                ft.Container(content=self._empty_hint, alignment=ft.Alignment.CENTER),
            ],
            expand=True,
        )
        super().__init__(
            controls=[self._legend, ft.Container(content=plot, height=height)],
            spacing=6,
        )

    @property
    def series_names(self) -> tuple[str, ...]:
        return tuple(self._series)

    def set_series(self, names: Sequence[str]) -> None:
        """Replace the plotted signals with empty lines named ``names``."""
        self._apply_series(names)
        update_if_mounted(self)

    def set_time_range(self, duration_s: float) -> None:
        """Fit the time axis and its grid to ``[0, duration_s]``."""
        ticks = time_axis_ticks(duration_s)
        self._duration_s = duration_s
        self._chart.max_x = duration_s
        self._chart.bottom_axis.labels = axis_labels(ticks)
        self._chart.vertical_grid_lines.interval = tick_interval(ticks)
        update_if_mounted(self._chart)

    def append(self, times_s: Sequence[float], values: SeriesValues) -> None:
        """Extend each known series; unknown names are ignored."""
        for name, samples in values.items():
            series = self._series.get(name)
            if series is None:
                continue
            series.points.extend(
                fch.LineChartDataPoint(time, value, show_tooltip=False)
                for time, value in zip(times_s, samples)
            )
        self._empty_hint.visible = False
        update_if_mounted(self._chart)
        update_if_mounted(self._empty_hint)

    def set_points(self, times_s: Sequence[float], values: SeriesValues) -> None:
        """Show a finished result, replacing any plotted points."""
        for series in self._series.values():
            series.points = []
        self.append(times_s, values)

    def show_sample(self) -> None:
        """Fill every series with static placeholder curves (UI-only phase)."""
        times, values = sample_signals(self.series_names, self._duration_s, self._y_range)
        self.set_points(times, values)

    def _apply_series(self, names: Sequence[str]) -> None:
        self._series = {
            name: fch.LineChartData(
                points=[],
                color=channel_color(index),
                stroke_width=2,
                curved=False,
                point=False,
            )
            for index, name in enumerate(names)
        }
        self._chart.data_series = list(self._series.values())
        self._legend.controls = [
            control
            for index, name in enumerate(names)
            for control in (
                ft.Container(width=24, height=2, bgcolor=channel_color(index)),
                ft.Text(name, size=TEXT_SMALL, color=NAVY),
            )
        ]
        self._empty_hint.visible = True


def _build_chart(
    y_range: ValueRange, y_label: str, x_label: str, duration_s: float
) -> fch.LineChart:
    y_ticks = value_axis_ticks(y_range)
    time_ticks = time_axis_ticks(duration_s)
    return fch.LineChart(
        data_series=[],
        min_x=0,
        max_x=duration_s,
        min_y=y_range[0],
        max_y=y_range[1],
        interactive=True,
        expand=True,
        border=ft.Border.only(
            left=ft.BorderSide(width=1, color=MUTED),
            bottom=ft.BorderSide(width=1, color=MUTED),
        ),
        horizontal_grid_lines=fch.ChartGridLines(
            interval=tick_interval(y_ticks), color=BORDER, width=1
        ),
        vertical_grid_lines=fch.ChartGridLines(
            interval=tick_interval(time_ticks), color=BORDER, width=1
        ),
        left_axis=fch.ChartAxis(
            title=ft.Text(y_label, size=TEXT_SMALL, color=NAVY),
            title_size=42,
            labels=axis_labels(y_ticks),
            label_size=30,
        ),
        bottom_axis=fch.ChartAxis(
            title=ft.Text(x_label, size=TEXT_SMALL, color=NAVY),
            title_size=38,
            labels=axis_labels(time_ticks),
            label_size=28,
        ),
    )
