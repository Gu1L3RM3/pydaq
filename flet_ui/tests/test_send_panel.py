"""Tests for the Send Data setup panel composition."""

from __future__ import annotations

from components.send_panel import SendSetupPanel
from pages.demo_devices import OUTPUT_DEVICE_CHOICES
from pages.send_data import SendDataView
from pydaq.core.acquisition import DeviceFamily


def test_arduino_panel_hides_output_range_and_reads_digital_request() -> None:
    panel = SendSetupPanel(OUTPUT_DEVICE_CHOICES)

    request = panel.read_request()

    assert panel.output_range.visible is False
    assert (request.device, request.channels) == ("COM3", ("D2",))
    assert request.sample_period_s == 1.0
    assert request.output_range is None


def test_nidaq_panel_shows_output_range_and_reads_it() -> None:
    panel = SendSetupPanel(OUTPUT_DEVICE_CHOICES)

    panel.set_device_family(DeviceFamily.NIDAQ)
    request = panel.read_request()

    assert panel.output_range.visible is True
    assert (request.device, request.channels) == ("Dev1", ("ao0",))
    assert request.output_range == (0.0, 5.0)


def test_real_time_warning_follows_plot_mode() -> None:
    panel = SendSetupPanel(OUTPUT_DEVICE_CHOICES)

    panel.plot_mode.tabs.select("At the end")
    hidden = panel._plot_warning.visible
    panel.plot_mode.tabs.select("Real time")

    assert hidden is False
    assert panel._plot_warning.visible is True


def test_set_data_file_updates_the_read_path() -> None:
    panel = SendSetupPanel(OUTPUT_DEVICE_CHOICES)

    panel.set_data_file("/data/step.dat")

    assert str(panel.read_request().data_path) == "/data/step.dat"


def test_send_view_prepares_chart_for_selected_channels() -> None:
    view = SendDataView()

    view._request_send(True)

    assert view._chart.plot.series_names == ("D2",)


def test_send_view_legend_follows_device_family() -> None:
    view = SendDataView()

    view._change_device_family(DeviceFamily.NIDAQ)

    assert view._chart.plot.series_names == ("ao0",)
