"""Data acquisition route."""

from __future__ import annotations

import flet as ft

from components.acquisition_panel import AcquisitionSetupPanel
from components.device_selector import DeviceSelector
from components.live_chart import LiveSignalChart
from theme import MUTED, NAVY


def build_get_data_page() -> ft.Control:
    """Compose the responsive data acquisition workflow."""
    signal_chart = LiveSignalChart()
    setup_panel = AcquisitionSetupPanel(
        on_acquisition_change=signal_chart.set_acquiring
    )
    device_selector = DeviceSelector(on_change=setup_panel.set_device_family)

    header = ft.ResponsiveRow(
        controls=[
            ft.Column(
                col={"xs": 12, "md": 7},
                controls=[
                    ft.Text(
                        "Data acquisition",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=NAVY,
                    ),
                    ft.Text(
                        "Acquire and visualize real-time data from your device.",
                        size=16,
                        color=MUTED,
                    ),
                ],
                spacing=2,
            ),
            ft.Container(
                col={"xs": 12, "md": 5},
                alignment=ft.Alignment.CENTER_RIGHT,
                content=device_selector,
            ),
        ],
        spacing=8,
        run_spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    content = ft.ResponsiveRow(
        controls=[
            ft.Container(col={"xs": 12, "lg": 4}, content=setup_panel),
            ft.Container(col={"xs": 12, "lg": 8}, content=signal_chart),
        ],
        spacing=10,
        run_spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    return ft.Column(
        controls=[header, ft.Container(height=4), content],
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
