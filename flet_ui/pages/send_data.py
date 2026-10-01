"""Send Data route.

UI only for now: the form is validated and the chart shows static placeholder
curves; no device is driven until the backend is connected.
"""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.charts.axes import format_sample_rate
from components.charts.signal_card import SignalCard
from components.charts.signal_plot import SignalPlot
from components.charts.status_badge import RateIndicator, StatusBadge
from components.device_selector import DeviceSelector
from components.mounting import is_mounted
from components.page_header import PageHeader
from components.send_panel import SendSetupPanel
from components.workflow_layout import WorkflowLayout
from pages.demo_devices import OUTPUT_DEVICE_CHOICES
from pydaq.core.acquisition import DeviceFamily
from services.send_form import SendRequest

DATA_FILE_EXTENSIONS = ["dat", "txt", "csv"]
NOT_CONNECTED_MESSAGE = (
    "Sending to devices is not available yet; the setup is valid and ready."
)


class SentSignalChart(SignalCard):
    """Result card for the values written to each output channel."""

    def __init__(
        self, channels: Sequence[str] = ("D2",), sample_period_s: float = 1.0
    ) -> None:
        self.plot = SignalPlot(
            channels,
            y_range=(0, 6),
            duration_s=10,
            empty_hint="Choose a data file and send it to plot the output here.",
        )
        self.status = StatusBadge(running_label="Sending")
        self._rate = RateIndicator(format_sample_rate(sample_period_s))
        super().__init__(
            "Sent signal",
            "Values written to the selected output channels.",
            plot=self.plot,
            indicators=(self.status, self._rate),
        )
        self.plot.show_sample()

    def show_channels(self, channels: Sequence[str]) -> None:
        """Name the legend after ``channels`` and redraw the placeholder curves."""
        self.plot.set_series(channels)
        self.plot.show_sample()

    def prepare(self, request: SendRequest) -> None:
        """Fit legend and rate to the channels and period about to be sent."""
        self.show_channels(request.channels)
        self._rate.set_text(format_sample_rate(request.sample_period_s))


class SendDataView(WorkflowLayout):
    """Send Data route: setup panel beside the sent-signal chart."""

    def __init__(self) -> None:
        self._chart = SentSignalChart()
        self._panel = SendSetupPanel(
            OUTPUT_DEVICE_CHOICES,
            on_send_change=self._request_send,
            on_browse=self._browse_data_file,
        )
        header = PageHeader(
            "Send data",
            "Replay a data file on your device's output channels.",
            trailing=DeviceSelector(on_change=self._change_device_family),
        )
        super().__init__(header, setup=self._panel, results=self._chart)

    def _change_device_family(self, family: DeviceFamily) -> None:
        self._panel.set_device_family(family)
        self._chart.show_channels(self._panel.device.ao_channels)

    def _request_send(self, start: bool) -> None:
        if not start:
            self._panel.set_running(False)
            return
        try:
            request = self._panel.read_request()
        except ValueError as error:
            self._show_message(str(error))
            return
        self._chart.prepare(request)
        self._show_message(NOT_CONNECTED_MESSAGE)

    def _browse_data_file(self) -> None:
        if is_mounted(self):
            self.page.run_task(self._pick_data_file)

    async def _pick_data_file(self) -> None:
        files = await ft.FilePicker().pick_files(
            dialog_title="Select the data file to send",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=DATA_FILE_EXTENSIONS,
        )
        # Cancelling returns no files; web builds expose no filesystem path.
        if files and files[0].path:
            self._panel.set_data_file(files[0].path)

    def _show_message(self, message: str) -> None:
        if not is_mounted(self):
            return
        self.page.show_dialog(ft.SnackBar(ft.Text(message)))


def build_send_data_page() -> ft.Control:
    return SendDataView()
