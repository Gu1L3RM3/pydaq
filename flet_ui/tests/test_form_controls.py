"""Regression tests for shared acquisition form sizing."""

from __future__ import annotations

from components.form_controls import LabeledDropdown, LabeledNumberField


def test_dropdown_matches_numeric_input_dimensions() -> None:
    dropdown = LabeledDropdown("Device", ("COM3",), "COM3")
    number_field = LabeledNumberField("Sample period (s)", "0.010")

    assert dropdown.dropdown.height == number_field.field.height
    assert dropdown.dropdown.expand is True
