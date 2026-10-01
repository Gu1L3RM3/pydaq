"""Shared presentation for sections that are not implemented yet."""

from __future__ import annotations

import flet as ft

from components.page_header import PageHeader
from theme import BORDER, CARD_RADIUS, MUTED, SPACE_SM, SURFACE, TEXT_LABEL


def build_placeholder_page(title: str, description: str) -> ft.Control:
    """Build an empty route while keeping the app hierarchy consistent."""
    return ft.Column(
        controls=[
            PageHeader(title, description),
            ft.Container(height=SPACE_SM),
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                bgcolor=SURFACE,
                border=ft.Border.all(width=1, color=BORDER),
                border_radius=CARD_RADIUS,
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CONSTRUCTION_ROUNDED, size=38, color=MUTED),
                        ft.Text(
                            "Page ready for implementation",
                            color=MUTED,
                            size=TEXT_LABEL,
                        ),
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ],
        expand=True,
    )
