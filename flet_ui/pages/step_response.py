"""Step Response route."""

from __future__ import annotations

import flet as ft

from pages.placeholder import build_placeholder_page


def build_step_response_page() -> ft.Control:
    return build_placeholder_page(
        "Step Response", "Analyze the step response of your system."
    )
