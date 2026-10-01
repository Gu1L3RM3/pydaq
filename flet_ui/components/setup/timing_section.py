"""Sampling and session timing fields."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.forms.fields import LabeledNumberField
from theme import FORM_GAP


class TimingSection(ft.Column):
    """Sample period, optional session duration and workflow-specific times.

    ``extra_fields`` covers values such as ``Step ON (s)`` or
    ``Start saving data (s)``::

        step_on = LabeledNumberField("Step ON (s)", "5")
        TimingSection(extra_fields=(step_on,))
    """

    def __init__(
        self,
        sample_period: str = "0.010",
        duration: str | None = "100",
        extra_fields: Sequence[LabeledNumberField] = (),
        sample_period_label: str = "Sample period (s)",
    ) -> None:
        self.sample_period = LabeledNumberField(sample_period_label, sample_period)
        self.duration = (
            LabeledNumberField("Session duration (s)", duration)
            if duration is not None
            else None
        )
        fields = [self.sample_period]
        if self.duration is not None:
            fields.append(self.duration)
        super().__init__(
            controls=[*fields, *extra_fields],
            spacing=FORM_GAP,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
