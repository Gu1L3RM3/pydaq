"""Session status and sample-rate indicators for result cards."""

from __future__ import annotations

from enum import Enum

import flet as ft

from components.mounting import update_if_mounted
from theme import ACCENT_DARK, MUTED, NAVY, SIGNAL_A0, TEXT_CAPTION


class SessionStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"


_STATUS_COLORS = {
    SessionStatus.IDLE: MUTED,
    SessionStatus.RUNNING: SIGNAL_A0,
    SessionStatus.ERROR: ACCENT_DARK,
}


class StatusBadge(ft.Row):
    """Colored dot plus label; ``running_label`` names the activity.

    It reports the session, not the device link, so it starts as ``Idle``::

        badge = StatusBadge(running_label="Sending")
        badge.set_status(SessionStatus.RUNNING)
    """

    def __init__(
        self,
        status: SessionStatus = SessionStatus.IDLE,
        running_label: str = "Acquiring",
    ) -> None:
        self._labels = {
            SessionStatus.IDLE: "Idle",
            SessionStatus.RUNNING: running_label,
            SessionStatus.ERROR: "Error",
        }
        self._dot = ft.Container(width=10, height=10, border_radius=5)
        self._label = ft.Text(size=TEXT_CAPTION)
        self.status = status
        self._apply(status)
        super().__init__(controls=[self._dot, self._label], spacing=8, tight=True)

    def set_status(self, status: SessionStatus) -> None:
        self._apply(status)
        update_if_mounted(self)

    def _apply(self, status: SessionStatus) -> None:
        self.status = status
        self._label.value = self._labels[status]
        self._label.color = _STATUS_COLORS[status]
        self._dot.bgcolor = _STATUS_COLORS[status]


class RateIndicator(ft.Row):
    """Icon and text such as ``100 Hz`` shown next to a status badge."""

    def __init__(self, text: str) -> None:
        self._text = ft.Text(text, size=TEXT_CAPTION, color=NAVY)
        super().__init__(
            controls=[
                ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=19, color=NAVY),
                self._text,
            ],
            spacing=8,
            tight=True,
        )

    def set_text(self, text: str) -> None:
        self._text.value = text
        update_if_mounted(self._text)
