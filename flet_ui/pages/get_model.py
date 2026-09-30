"""Get Model route."""

from __future__ import annotations

import flet as ft

from pages.placeholder import build_placeholder_page


def build_get_model_page() -> ft.Control:
    return build_placeholder_page(
        "Get Model", "Identify and configure the system model."
    )
