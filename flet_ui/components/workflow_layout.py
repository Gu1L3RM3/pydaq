"""Standard two-column layout: setup on the left, results on the right."""

from __future__ import annotations

import flet as ft

from theme import SPACE_XS


class WorkflowLayout(ft.Column):
    """Header above a setup panel (``lg=4``) and a results area (``lg=8``).

    Below the ``lg`` breakpoint the setup stacks above the results. Pages
    subclass it or build it directly::

        WorkflowLayout(PageHeader("Send Data", "..."), setup_panel, signal_card)
    """

    def __init__(
        self, header: ft.Control, setup: ft.Control, results: ft.Control
    ) -> None:
        content = ft.ResponsiveRow(
            controls=[
                ft.Container(col={"xs": 12, "lg": 4}, content=setup),
                ft.Container(col={"xs": 12, "lg": 8}, content=results),
            ],
            spacing=10,
            run_spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        super().__init__(
            controls=[header, ft.Container(height=SPACE_XS), content],
            spacing=6,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
