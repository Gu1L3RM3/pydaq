"""Tests for segmented choices, toggles and channel picking."""

from __future__ import annotations

import pytest

from components.forms.choices import (
    ChannelPicker,
    ChoiceTabs,
    LabeledChoice,
    ToggleSetting,
    format_channels,
    toggle_channel,
)


def test_toggle_channel_adds_in_available_order() -> None:
    assert toggle_channel(("A1",), "A0", ("A0", "A1")) == ("A0", "A1")


def test_toggle_channel_removes_selected_channel() -> None:
    assert toggle_channel(("A0", "A1"), "A0", ("A0", "A1")) == ("A1",)


def test_toggle_channel_keeps_last_channel() -> None:
    assert toggle_channel(("A0",), "A0", ("A0", "A1")) == ("A0",)


def test_toggle_channel_rejects_unknown_channel() -> None:
    with pytest.raises(ValueError, match="'A9' is not in"):
        toggle_channel(("A0",), "A9", ("A0", "A1"))


def test_channel_picker_reports_selection_changes() -> None:
    changes: list[tuple[str, ...]] = []
    picker = ChannelPicker("AI channels", ("A0", "A1"), ("A0",), on_change=changes.append)

    picker.toggle("A1")

    assert picker.value == ("A0", "A1")
    assert changes == [("A0", "A1")]
    assert [item.checked for item in picker._menu.items] == [True, True]


def test_channel_picker_rejects_selection_outside_available() -> None:
    with pytest.raises(ValueError, match="non-empty subset"):
        ChannelPicker("AI channels", ("A0",), ("ai0",))


def test_format_channels_joins_names() -> None:
    assert format_channels(("A0", "A1")) == "A0, A1"


def test_choice_tabs_notify_only_on_change() -> None:
    changes: list[str] = []
    tabs = ChoiceTabs(("P", "PI", "PID"), "PID", on_change=changes.append)

    tabs.select("PID")
    tabs.select("PI")

    assert tabs.value == "PI"
    assert changes == ["PI"]


def test_choice_tabs_reject_unknown_option() -> None:
    tabs = ChoiceTabs(("P", "PI"), "P")

    with pytest.raises(ValueError, match="unknown choice 'PD'"):
        tabs.select("PD")


def test_labeled_choice_and_toggle_expose_values() -> None:
    assert LabeledChoice("Plot data?", ("Real time", "Off"), "Off").value == "Off"
    assert ToggleSetting("Save data?", value=True).value is True
