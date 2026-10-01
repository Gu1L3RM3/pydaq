"""Page title block shared by every route."""

from __future__ import annotations

import flet as ft

from theme import MUTED, NAVY, SPACE_SM, TEXT_BODY, TEXT_PAGE_TITLE


class PageHeader(ft.ResponsiveRow):
    """Title and description, with an optional right-aligned ``trailing`` control.

    Example::

        PageHeader("Data acquisition", "Acquire real-time data.", DeviceSelector())
    """

    def __init__(
        self, title: str, description: str, trailing: ft.Control | None = None
    ) -> None:
        heading = ft.Column(
            col={"xs": 12, "md": 7} if trailing else 12,
            controls=[
                ft.Text(
                    title,
                    size=TEXT_PAGE_TITLE,
                    weight=ft.FontWeight.BOLD,
                    color=NAVY,
                ),
                ft.Text(description, size=TEXT_BODY, color=MUTED),
            ],
            spacing=2,
        )
        controls: list[ft.Control] = [heading]
        if trailing is not None:
            controls.append(
                ft.Container(
                    col={"xs": 12, "md": 5},
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=trailing,
                )
            )
        super().__init__(
            controls=controls,
            spacing=SPACE_SM,
            run_spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
