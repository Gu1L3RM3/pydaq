"""Data acquisition route.

UI only for now: the form is validated and the chart shows static placeholder
curves; no device or simulated source is read until the backend is connected.
"""

from __future__ import annotations

import flet as ft

from components.acquisition_panel import AcquisitionSetupPanel
from components.device_selector import DeviceSelector
from components.live_chart import LiveSignalChart
from components.mounting import is_mounted
from components.page_header import PageHeader
from components.workflow_layout import WorkflowLayout
from pages.demo_devices import ACQUISITION_DEVICE_CHOICES

NOT_CONNECTED_MESSAGE = (
    "Acquisition is not available yet; the setup is valid and ready."
)


class GetDataView(WorkflowLayout):
    """Get Data route: setup panel beside the live signal chart."""

    def __init__(self) -> None:
        self._chart = LiveSignalChart()
        self._panel = AcquisitionSetupPanel(
            ACQUISITION_DEVICE_CHOICES, on_acquisition_change=self._request_acquisition
        )
        header = PageHeader(
            "Data acquisition",
            "Acquire and visualize real-time data from your device.",
            trailing=DeviceSelector(on_change=self._panel.set_device_family),
        )
        super().__init__(header, setup=self._panel, results=self._chart)

    def _request_acquisition(self, start: bool) -> None:
        if not start:
            self._panel.set_running(False)
            return
        try:
            config = self._panel.read_config()
        except ValueError as error:
            self._show_message(str(error))
            return
        self._chart.preview(config)
        self._show_message(NOT_CONNECTED_MESSAGE)

    def _show_message(self, message: str) -> None:
        if not is_mounted(self):
            return
        self.page.show_dialog(ft.SnackBar(ft.Text(message)))


def build_get_data_page() -> ft.Control:
    return GetDataView()
