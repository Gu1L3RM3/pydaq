"""Data acquisition route."""

from __future__ import annotations

import flet as ft

from components.acquisition_panel import AcquisitionSetupPanel
from components.device_selector import DeviceSelector
from components.live_chart import LiveSignalChart
from pages.demo_devices import ACQUISITION_DEVICE_CHOICES
from pydaq.core.acquisition import AcquisitionSource, SampleBatch
from pydaq.devices.simulated import SimulatedSource
from services.acquisition_session import AcquisitionSession
from theme import MUTED, NAVY


class GetDataView(ft.Column):
    """Get Data route: connects the setup panel and chart to one session."""

    def __init__(self, source: AcquisitionSource) -> None:
        self._chart = LiveSignalChart()
        self._panel = AcquisitionSetupPanel(
            ACQUISITION_DEVICE_CHOICES, on_acquisition_change=self._request_acquisition
        )
        self._session = AcquisitionSession(
            source,
            on_batch=self._show_batch,
            on_finished=self._show_finished,
            on_error=self._show_error,
        )
        super().__init__(
            controls=_compose_layout(self._panel, self._chart),
            spacing=6,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def will_unmount(self) -> None:
        # Navigating away must not leave a device streaming into detached controls.
        self._session.stop()

    def _request_acquisition(self, start: bool) -> None:
        if not start:
            self._session.stop()
            return
        try:
            config = self._panel.read_config()
        except ValueError as error:
            self._show_error(str(error))
            return
        self._chart.reset(config)
        self._panel.set_running(True)
        self._chart.set_acquiring(True)
        self._session.start(config)

    def _show_batch(self, batch: SampleBatch) -> None:
        self._chart.append_batch(batch)

    def _show_finished(self) -> None:
        self._panel.set_running(False)
        self._chart.set_acquiring(False)

    def _show_error(self, message: str) -> None:
        self.page.show_dialog(ft.SnackBar(ft.Text(message)))


def build_get_data_page(source: AcquisitionSource | None = None) -> ft.Control:
    """Get Data route; ``source`` defaults to simulated data until hardware adapters land."""
    return GetDataView(source or SimulatedSource())


def _compose_layout(
    setup_panel: AcquisitionSetupPanel, signal_chart: LiveSignalChart
) -> list[ft.Control]:
    """Compose the responsive data acquisition workflow."""
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
    return [header, ft.Container(height=4), content]
