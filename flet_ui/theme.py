"""Shared visual tokens for the Flet interface."""

from __future__ import annotations

import flet as ft

NAVY = "#102342"
MUTED = "#71809A"
BACKGROUND = "#F7F9FC"
SURFACE = "#FFFFFF"
BORDER = "#DFE5EF"
ACCENT = "#B56C70"
ACCENT_DARK = "#A65E63"
ACCENT_SOFT = "#F8EFF0"
SUCCESS = "#148A2E"
SIGNAL_A0 = "#087FF5"
SIGNAL_A1 = "#11A89C"
INPUT_FILL = "#FBFCFE"

SPACE_XS = 4
SPACE_SM = 8
SPACE_MD = 16
SPACE_LG = 24
SPACE_XL = 32

CONTROL_RADIUS = 8
CARD_RADIUS = 12
SIDEBAR_WIDTH = 208
MOBILE_BREAKPOINT = 900


def app_theme() -> ft.Theme:
    """Return the application theme built from the design package tokens."""
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ACCENT,
            on_primary=ft.Colors.WHITE,
            surface=SURFACE,
            on_surface=NAVY,
            outline=BORDER,
        ),
        font_family="Arial",
    )
