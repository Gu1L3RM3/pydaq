"""Data acquisition route."""

from __future__ import annotations

import flet as ft

from components.acquisition_panel import AcquisitionSetupPanel
from components.device_selector import DeviceSelector
from components.live_chart import LiveSignalChart
from components.page_header import PageHeader
from components.workflow_layout import WorkflowLayout
from pages.demo_devices import ACQUISITION_DEVICE_CHOICES
from pydaq.core.acquisition import AcquisitionSource, SampleBatch
from pydaq.devices.simulated import SimulatedSource
from services.acquisition_session import AcquisitionSession


class GetDataView(WorkflowLayout):
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
        header = PageHeader(
            "Data acquisition",
            "Acquire and visualize real-time data from your device.",
            trailing=DeviceSelector(on_change=self._panel.set_device_family),
        )
        super().__init__(header, setup=self._panel, results=self._chart)

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
