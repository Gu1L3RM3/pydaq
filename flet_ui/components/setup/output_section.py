"""Filtering, plotting and saving options shared by acquisition workflows."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.forms.choices import LabeledChoice, ToggleSetting
from components.forms.fields import PathField
from theme import FORM_GAP

PLOT_MODES = ("Real time", "At the end", "Off")
DEFAULT_SAVE_PATH = "~/Documents/PYDAQ"


class OutputSection(ft.Column):
    """Optional digital filter, plot mode, save toggle and the output path.

    Rows a workflow does not offer are omitted and their attribute is ``None``;
    Send Data, for instance, has no save toggle::

        OutputSection(show_save=False)
    """

    def __init__(
        self,
        plot_modes: Sequence[str] | None = PLOT_MODES,
        show_save: bool = True,
        show_filter: bool = False,
        path: str = DEFAULT_SAVE_PATH,
    ) -> None:
        self.digital_filter = ToggleSetting("Digital filter?") if show_filter else None
        self.plot_mode = (
            LabeledChoice("Plot data?", plot_modes, plot_modes[0]) if plot_modes else None
        )
        self.save = ToggleSetting("Save data?") if show_save else None
        self.path = PathField(path)
        rows = [self.digital_filter, self.plot_mode, self.save, self.path]
        super().__init__(
            controls=[row for row in rows if row is not None],
            spacing=FORM_GAP,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
