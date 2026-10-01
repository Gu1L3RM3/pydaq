"""Reusable real-time signal chart."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft
import flet_charts as fch

from components.panel import PanelCard
from pydaq.core.acquisition import AcquisitionConfig, SampleBatch
from theme import (
    BORDER,
    MUTED,
    NAVY,
    SIGNAL_A0,
    SIGNAL_A1,
    SPACE_MD,
    SUCCESS,
)

CHANNEL_COLORS = (SIGNAL_A0, SIGNAL_A1)
_TICK_STEPS = (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000)
_MAX_TIME_TICKS = 11


def channel_color(index: int) -> str:
    return CHANNEL_COLORS[index % len(CHANNEL_COLORS)]


def time_axis_ticks(duration_s: float) -> tuple[int, ...]:
    """Round tick positions covering ``duration_s`` with at most 11 labels."""
    if duration_s <= 0:
        raise ValueError(f"duration_s must be positive, received {duration_s}")
    step = next(
        (step for step in _TICK_STEPS if duration_s / step < _MAX_TIME_TICKS),
        _TICK_STEPS[-1],
    )
    return tuple(range(0, int(duration_s) + 1, step))


def _tick_interval(ticks: tuple[int, ...]) -> int:
    return ticks[1] - ticks[0] if len(ticks) > 1 else 1


def format_sample_rate(sample_period_s: float) -> str:
    if sample_period_s <= 0:
        raise ValueError(f"sample_period_s must be positive, received {sample_period_s}")
    return f"{1 / sample_period_s:g} Hz"


def _axis_labels(values: tuple[int, ...]) -> list[fch.ChartAxisLabel]:
    return [
        fch.ChartAxisLabel(
            value=value,
            label=ft.Text(str(value), size=11, color=MUTED),
        )
        for value in values
    ]


class LiveSignalChart(PanelCard):
    """Live signal card that plots ``SampleBatch`` streams per channel.

    Call ``reset(config)`` before a session and ``append_batch`` per batch.
    """

    def __init__(
        self,
        channels: Sequence[str] = ("A0", "A1"),
        duration_s: float = 100.0,
        sample_period_s: float = 0.01,
    ) -> None:
        self._status_dot = ft.Container(
            width=10, height=10, border_radius=5, bgcolor=SUCCESS
        )
        self._status_label = ft.Text("Connected", color=SUCCESS, size=13)
        self._rate_label = ft.Text(
            format_sample_rate(sample_period_s), size=13, color=NAVY
        )
        self._series: dict[str, fch.LineChartData] = {}
        self._chart = self._build_chart(duration_s)
        self._legend = ft.Row(spacing=SPACE_MD, alignment=ft.MainAxisAlignment.END)
        self._empty_hint = ft.Text(
            "Start an acquisition to stream data here.", size=14, color=MUTED
        )
        self._show_channels(channels)
        header = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"xs": 12, "md": 7},
                    controls=[
                        ft.Text(
                            "Live signal",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=NAVY,
                        ),
                        ft.Text(
                            "Real-time data from analog input channels.",
                            size=14,
                            color=MUTED,
                        ),
                    ],
                    spacing=2,
                ),
                ft.Container(
                    col={"xs": 12, "md": 5},
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=ft.Row(
                        controls=[
                            self._status_dot,
                            self._status_label,
                            ft.Container(width=1, height=22, bgcolor=BORDER),
                            ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=19, color=NAVY),
                            self._rate_label,
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ),
            ],
            spacing=8,
            run_spacing=8,
        )
        plot = ft.Stack(
            controls=[
                self._chart,
                ft.Container(content=self._empty_hint, alignment=ft.Alignment.CENTER),
            ],
            expand=True,
        )
        chart_area = ft.Column(
            controls=[
                header,
                ft.Container(height=8),
                self._legend,
                ft.Container(content=plot, height=500),
            ],
            spacing=6,
        )
        super().__init__(chart_area, padding=20)

    @staticmethod
    def _build_chart(duration_s: float) -> fch.LineChart:
        return fch.LineChart(
            data_series=[],
            min_x=0,
            max_x=duration_s,
            min_y=-6,
            max_y=6,
            interactive=True,
            expand=True,
            border=ft.Border.only(
                left=ft.BorderSide(width=1, color=MUTED),
                bottom=ft.BorderSide(width=1, color=MUTED),
            ),
            horizontal_grid_lines=fch.ChartGridLines(
                interval=2, color=BORDER, width=1
            ),
            vertical_grid_lines=fch.ChartGridLines(
                interval=_tick_interval(time_axis_ticks(duration_s)),
                color=BORDER,
                width=1,
            ),
            left_axis=fch.ChartAxis(
                title=ft.Text("Voltage (V)", size=12, color=NAVY),
                title_size=42,
                labels=_axis_labels((-6, -4, -2, 0, 2, 4, 6)),
                label_size=30,
            ),
            bottom_axis=fch.ChartAxis(
                title=ft.Text("Time (s)", size=12, color=NAVY),
                title_size=38,
                labels=_axis_labels(time_axis_ticks(duration_s)),
                label_size=28,
            ),
        )

    def _show_channels(self, channels: Sequence[str]) -> None:
        self._series = {
            channel: fch.LineChartData(
                points=[],
                color=channel_color(index),
                stroke_width=2,
                curved=False,
                point=False,
            )
            for index, channel in enumerate(channels)
        }
        self._chart.data_series = list(self._series.values())
        self._legend.controls = [
            control
            for index, channel in enumerate(channels)
            for control in (
                ft.Container(width=24, height=2, bgcolor=channel_color(index)),
                ft.Text(channel, size=12, color=NAVY),
            )
        ]
        self._empty_hint.visible = True

    def reset(self, config: AcquisitionConfig) -> None:
        """Clear plotted data and fit axes, legend and rate to a new session."""
        ticks = time_axis_ticks(config.duration_s)
        self._chart.max_x = config.duration_s
        self._chart.bottom_axis.labels = _axis_labels(ticks)
        self._chart.vertical_grid_lines.interval = _tick_interval(ticks)
        self._rate_label.value = format_sample_rate(config.sample_period_s)
        self._show_channels(config.channels)
        self.update()

    def append_batch(self, batch: SampleBatch) -> None:
        """Extend each channel line; channels missing from ``reset`` are ignored."""
        for channel, values in batch.channel_values.items():
            series = self._series.get(channel)
            if series is None:
                continue
            series.points.extend(
                fch.LineChartDataPoint(time, value, show_tooltip=False)
                for time, value in zip(batch.times_s, values)
            )
        self._empty_hint.visible = False
        self._chart.update()
        self._empty_hint.update()

    def set_acquiring(self, running: bool) -> None:
        """Update status presentation when acquisition starts or stops."""
        self._status_label.value = "Acquiring" if running else "Connected"
        self._status_label.color = SIGNAL_A0 if running else SUCCESS
        self._status_dot.bgcolor = SIGNAL_A0 if running else SUCCESS
        self.update()
