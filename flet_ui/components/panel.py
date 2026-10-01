"""Reusable panel primitives."""

from __future__ import annotations

import flet as ft

from theme import (
    BORDER,
    CARD_RADIUS,
    MUTED,
    NAVY,
    SPACE_LG,
    SURFACE,
    TEXT_LABEL,
    TEXT_SECTION_TITLE,
)


class PanelCard(ft.Container):
    """A bordered surface with an optional title and description."""

    def __init__(
        self,
        content: ft.Control,
        *,
        title: str | None = None,
        description: str | None = None,
        padding: int = SPACE_LG,
        header_gap: int = 8,
        expand: bool | int | None = None,
    ) -> None:
        controls: list[ft.Control] = []
        if title is not None:
            controls.append(
                ft.Text(
                    title,
                    size=TEXT_SECTION_TITLE,
                    weight=ft.FontWeight.BOLD,
                    color=NAVY,
                )
            )
        if description is not None:
            controls.append(ft.Text(description, size=TEXT_LABEL, color=MUTED))
        if controls:
            controls.append(ft.Container(height=header_gap))
        controls.append(content)
        super().__init__(
            content=ft.Column(controls=controls, spacing=2),
            bgcolor=SURFACE,
            border=ft.Border.all(width=1, color=BORDER),
            border_radius=CARD_RADIUS,
            padding=padding,
            expand=expand,
        )
