"""Tests for the UI-only Get Data route."""

from __future__ import annotations

from components.charts.status_badge import SessionStatus
from pages.get_data import GetDataView


def test_get_data_starts_with_static_sample_curves() -> None:
    view = GetDataView()

    assert view._chart.plot.series_names == ("A0", "A1")
    assert all(series.points for series in view._chart.plot._chart.data_series)


def test_start_validates_and_previews_without_acquiring() -> None:
    view = GetDataView()

    view._request_acquisition(True)

    assert view._chart.status.status is SessionStatus.IDLE
    assert all(series.points for series in view._chart.plot._chart.data_series)
