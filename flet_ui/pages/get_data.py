"""Data acquisition route."""

from __future__ import annotations

import flet as ft

from pages.placeholder import build_placeholder_page


def build_get_data_page() -> ft.Control:
    """Build the data acquisition page."""
    return build_placeholder_page(
        "Data acquisition",
        "Acquire and visualize real-time data from your device.",
    )
