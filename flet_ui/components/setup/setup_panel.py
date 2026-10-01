"""Card that stacks setup sections above the primary action."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.mounting import update_if_mounted
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
        self.slack = 0.0
        # Empty height added by ``WorkflowLayout`` so the card ends level with
        # the results; it sits above the divider to keep the action at the bottom.
        self._spacer = ft.Container(height=0)
        form = ft.Column(
            controls=[
                *sections,
                ft.Column(
                    controls=[self._spacer, ft.Divider(height=4, color=BORDER)],
                    spacing=0,
                ),
                action,
            ],
            spacing=FORM_GAP,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        super().__init__(
            form, title=title, description=description, padding=14, header_gap=4
        )

    def set_slack(self, height: float) -> None:
        """Grow by ``height`` above the action (see ``WorkflowLayout``)."""
        self.slack = height
        self._spacer.height = height
        update_if_mounted(self._spacer)
