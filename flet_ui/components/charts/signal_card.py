"""Result card: title, status indicators and a ``SignalPlot``."""

from __future__ import annotations

from collections.abc import Sequence

import flet as ft

from components.mounting import update_if_mounted
from components.panel import PanelCard
from theme import BORDER, MUTED, NAVY, SPACE_SM, TEXT_LABEL, TEXT_SECTION_TITLE


class SignalCard(PanelCard):
    """Card with a heading, right-aligned ``indicators`` and a plot below.

    Example::

        SignalCard(
            "Step response",
            "Output after the step is applied.",
            plot=SignalPlot(("u", "y")),
            indicators=(StatusBadge(running_label="Running"),),
        )
    """

    def __init__(
        self,
        title: str,
        description: str,
        plot: ft.Control,
        indicators: Sequence[ft.Control] = (),
    ) -> None:
        header = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"xs": 12, "md": 7},
                    controls=[
                        ft.Text(
                            title,
                            size=TEXT_SECTION_TITLE,
                            weight=ft.FontWeight.BOLD,
                            color=NAVY,
                        ),
                        ft.Text(description, size=TEXT_LABEL, color=MUTED),
                    ],
                    spacing=2,
                ),
                ft.Container(
                    col={"xs": 12, "md": 5},
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=ft.Row(
                        controls=_separated(indicators),
                        spacing=SPACE_SM,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ),
            ],
            spacing=SPACE_SM,
            run_spacing=SPACE_SM,
        )
        self.slack = 0.0
        # Empty height added by ``WorkflowLayout`` so the card ends level with
        # the setup panel.
        self._spacer = ft.Container(height=0)
        super().__init__(
            ft.Column(
                controls=[
                    header,
                    ft.Container(height=SPACE_SM),
                    ft.Column(controls=[plot, self._spacer], spacing=0),
                ],
                spacing=6,
            ),
            padding=20,
        )

    def set_slack(self, height: float) -> None:
        """Grow by ``height`` below the plot (see ``WorkflowLayout``)."""
        self.slack = height
        self._spacer.height = height
        update_if_mounted(self._spacer)


def _separated(indicators: Sequence[ft.Control]) -> list[ft.Control]:
    controls: list[ft.Control] = []
    for indicator in indicators:
        if controls:
            controls.append(ft.Container(width=1, height=22, bgcolor=BORDER))
        controls.append(indicator)
    return controls
