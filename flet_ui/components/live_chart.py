"""Reusable real-time signal chart."""

from __future__ import annotations

import math
from dataclasses import dataclass

import flet as ft
import flet_charts as fch

from components.panel import PanelCard
from theme import (
    BORDER,
    MUTED,
    NAVY,
    SIGNAL_A0,
    SIGNAL_A1,
    SPACE_MD,
    SUCCESS,
)


@dataclass(frozen=True)
class SignalPoint:
    time: float
    value: float


@dataclass(frozen=True)
class SignalSeries:
    name: str
    color: str
    points: tuple[SignalPoint, ...]


def build_demo_series(
    duration: float = 105.0,
    point_count: int = 260,
) -> tuple[SignalSeries, SignalSeries]:
    """Create deterministic signals that resemble the design reference."""
    if duration <= 0:
        raise ValueError(f"duration must be positive, received {duration}")
    if point_count < 2:
        raise ValueError(f"point_count must be at least 2, received {point_count}")

    times = tuple(index * duration / (point_count - 1) for index in range(point_count))
    channel_a0 = tuple(
        SignalPoint(time, 4.0 * math.sin((time - 8.0) * math.tau / 35.0))
        for time in times
    )
    channel_a1 = tuple(
        SignalPoint(time, 1.9 * math.sin((time - 12.0) * math.tau / 35.0))
        for time in times
    )
    return (
        SignalSeries("A0", SIGNAL_A0, channel_a0),
        SignalSeries("A1", SIGNAL_A1, channel_a1),
    )


def _axis_labels(values: tuple[int, ...]) -> list[fch.ChartAxisLabel]:
    return [
        fch.ChartAxisLabel(
            value=value,
            label=ft.Text(str(value), size=11, color=MUTED),
        )
        for value in values
    ]


class LiveSignalChart(PanelCard):
    """Live signal card with connection state, rate and reusable line chart."""

    def __init__(self, series: tuple[SignalSeries, ...] | None = None) -> None:
        chart_series = series or build_demo_series()
        self._status_dot = ft.Container(
            width=10, height=10, border_radius=5, bgcolor=SUCCESS
        )
        self._status_label = ft.Text("Connected", color=SUCCESS, size=13)
        self._chart = self._build_chart(chart_series)
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
                            ft.Text("100 Hz", size=13, color=NAVY),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ),
            ],
            spacing=8,
            run_spacing=8,
        )
        chart_area = ft.Column(
            controls=[
                header,
                ft.Container(height=8),
                self._build_legend(chart_series),
                ft.Container(content=self._chart, height=500),
            ],
            spacing=6,
        )
        super().__init__(chart_area, padding=20)

    @staticmethod
    def _build_chart(series: tuple[SignalSeries, ...]) -> fch.LineChart:
        chart_series = [
            fch.LineChartData(
                points=[
                    fch.LineChartDataPoint(
                        point.time,
                        point.value,
                        show_tooltip=False,
                    )
                    for point in signal.points
                ],
                color=signal.color,
                stroke_width=2,
                curved=False,
                point=False,
            )
            for signal in series
        ]
        return fch.LineChart(
            data_series=chart_series,
            min_x=0,
            max_x=105,
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
                interval=10, color=BORDER, width=1
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
                labels=_axis_labels(tuple(range(0, 101, 10))),
                label_size=28,
            ),
        )

    @staticmethod
    def _build_legend(series: tuple[SignalSeries, ...]) -> ft.Row:
        controls: list[ft.Control] = []
        for signal in series:
            controls.extend(
                [
                    ft.Container(width=24, height=2, bgcolor=signal.color),
                    ft.Text(signal.name, size=12, color=NAVY),
                ]
            )
        return ft.Row(
            controls=controls,
            spacing=SPACE_MD,
            alignment=ft.MainAxisAlignment.END,
        )

    def set_acquiring(self, running: bool) -> None:
        """Update status presentation when acquisition starts or stops."""
        self._status_label.value = "Acquiring" if running else "Connected"
        self._status_label.color = SIGNAL_A0 if running else SUCCESS
        self._status_dot.bgcolor = SIGNAL_A0 if running else SUCCESS
        self.update()
