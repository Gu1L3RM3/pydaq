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
SECONDARY_FILL = "#F1F4F8"
SWITCH_TRACK_OFF = "#B8C1D0"
MUTED_LIGHT = "#9AA6B8"
MUTED_LIGHTER = "#A5B0C0"

# The design package sets 44/25/17/13 on a 1680 px canvas; the Flet scale is
# reduced so the acquisition setup fits above the fold (commit 8c1593b).
TEXT_PAGE_TITLE = 32
TEXT_SECTION_TITLE = 20
TEXT_BODY = 16
TEXT_ACTION = 15
TEXT_LABEL = 14
TEXT_CAPTION = 13
TEXT_SMALL = 12
TEXT_XSMALL = 11
TEXT_XXSMALL = 10

SPACE_XS = 4
SPACE_SM = 8
SPACE_MD = 16
SPACE_LG = 24
SPACE_XL = 32
# Vertical gap between rows of a setup form.
FORM_GAP = 13

CONTROL_RADIUS = 8
CARD_RADIUS = 12

SEGMENT_HEIGHT = 32
CONTROL_HEIGHT = 36
ACTION_HEIGHT = 44
CHART_HEIGHT = 500
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
