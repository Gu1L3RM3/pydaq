"""Card that stacks setup sections above the primary action."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.panel import PanelCard
from theme import BORDER, FORM_GAP


class SetupPanel(PanelCard):
    """Titled card: ``sections`` top to bottom, a divider, then ``action``.

    Example::

        SetupPanel(
            "Send setup",
            "Choose the output channels and timing.",
            sections=(DeviceSection(choices), TimingSection(duration=None)),
            action=PrimaryActionButton("Send data", "Stop sending"),
        )
    """

    def __init__(
        self,
        title: str,
        description: str,
        sections: Sequence[ft.Control],
        action: ft.Control,
    ) -> None:
        form = ft.Column(
            controls=[*sections, ft.Divider(height=4, color=BORDER), action],
            spacing=FORM_GAP,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        super().__init__(
            form, title=title, description=description, padding=14, header_gap=4
        )
