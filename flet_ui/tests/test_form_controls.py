"""Tests for shared form fields and buttons."""

from __future__ import annotations

import pytest

from components.forms.buttons import PrimaryActionButton
from components.forms.fields import (
    LabeledDropdown,
    LabeledNumberField,
    LabeledTextField,
    PathField,
)


def test_dropdown_matches_numeric_input_dimensions() -> None:
    dropdown = LabeledDropdown("Device", ("COM3",), "COM3")
    number_field = LabeledNumberField("Sample period (s)", "0.010")

    assert dropdown.dropdown.height == number_field.field.height
    assert dropdown.dropdown.expand is True


def test_fields_expose_their_text_as_value() -> None:
    assert LabeledNumberField("Kp", "1.5").value == "1.5"
    assert LabeledTextField("Unit").value == ""
    assert PathField("~/data").value == "~/data"


def test_dropdown_set_options_rejects_value_outside_options() -> None:
    dropdown = LabeledDropdown("Device", ("COM3",), "COM3")

    with pytest.raises(ValueError, match="'Dev1' is not in options"):
        dropdown.set_options(("COM4",), "Dev1")


def test_primary_action_button_requests_opposite_state() -> None:
    requests: list[bool] = []
    button = PrimaryActionButton("Start", "Stop", on_toggle=requests.append)

    button._handle_click(None)
    button.set_running(True)
    button._handle_click(None)

    assert requests == [True, False]
