"""Send Data route."""

from __future__ import annotations

import flet as ft

from pages.placeholder import build_placeholder_page


def build_send_data_page() -> ft.Control:
    return build_placeholder_page("Send Data", "Send data to the connected device.")
