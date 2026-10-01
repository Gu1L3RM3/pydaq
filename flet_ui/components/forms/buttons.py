"""Action buttons shared by setup panels."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from components.mounting import update_if_mounted
from theme import (
    ACCENT,
    ACCENT_DARK,
    ACTION_HEIGHT,
    BORDER,
    CONTROL_HEIGHT,
    CONTROL_RADIUS,
    NAVY,
    SECONDARY_FILL,
    SPACE_SM,
    TEXT_ACTION,
)

ClickCallback = Callable[[], None]
RunToggleCallback = Callable[[bool], None]


class SecondaryButton(ft.Button):
    """Neutral input-height button for Browse, Config signal, Insert matrices…"""

    def __init__(
        self,
        label: str,
        on_click: ClickCallback | None = None,
        icon: ft.IconData | None = None,
    ) -> None:
        self._on_press = on_click
        super().__init__(
            label,
            icon=icon,
            height=CONTROL_HEIGHT,
            style=ft.ButtonStyle(
                color=NAVY,
                bgcolor=SECONDARY_FILL,
                side=ft.BorderSide(width=1, color=BORDER),
                shape=ft.RoundedRectangleBorder(radius=CONTROL_RADIUS),
            ),
            on_click=self._handle_click,
        )

    def _handle_click(self, _event: ft.Event[ft.Button]) -> None:
        if self._on_press is not None:
            self._on_press()


class PrimaryActionButton(ft.Container):
    """Full-width start/stop action of a setup panel.

    Clicking only *requests* a change through ``on_toggle(start)``; the host
    confirms with ``set_running`` once the session actually starts or ends.

    Example::

        PrimaryActionButton("Send data", "Stop sending", on_toggle=page.request_run)
    """

    def __init__(
        self,
        idle_label: str,
        running_label: str,
        on_toggle: RunToggleCallback | None = None,
        idle_icon: ft.IconData = ft.Icons.PLAY_ARROW_ROUNDED,
        running_icon: ft.IconData = ft.Icons.STOP_ROUNDED,
    ) -> None:
        self._labels = (idle_label, running_label)
        self._icons = (idle_icon, running_icon)
        self._on_toggle = on_toggle
        self.running = False
        self._icon = ft.Icon(idle_icon, color=ft.Colors.WHITE)
        self._label = ft.Text(
            idle_label,
            color=ft.Colors.WHITE,
            size=TEXT_ACTION,
            weight=ft.FontWeight.W_600,
        )
        super().__init__(
            height=ACTION_HEIGHT,
            bgcolor=ACCENT,
            border_radius=CONTROL_RADIUS,
            alignment=ft.Alignment.CENTER,
            ink=True,
            on_click=self._handle_click,
            content=ft.Row(
                controls=[self._icon, self._label], spacing=SPACE_SM, tight=True
            ),
        )

    def set_running(self, running: bool) -> None:
        """Show the idle or running action without notifying the host."""
        self.running = running
        self._icon.icon = self._icons[running]
        self._label.value = self._labels[running]
        self.bgcolor = ACCENT_DARK if running else ACCENT
        update_if_mounted(self)

    def _handle_click(self, _event: ft.Event[ft.Container]) -> None:
        if self._on_toggle is not None:
            self._on_toggle(not self.running)
