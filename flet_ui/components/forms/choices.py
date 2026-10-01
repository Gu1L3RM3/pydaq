"""Selection controls: switches, segmented choices and channel pickers."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import flet as ft

from components.forms.fields import field_label
from components.mounting import update_if_mounted
from theme import (
    ACCENT,
    BORDER,
    CONTROL_HEIGHT,
    CONTROL_RADIUS,
    INPUT_FILL,
    MUTED,
    NAVY,
    SEGMENT_HEIGHT,
    SPACE_SM,
    SWITCH_TRACK_OFF,
    TEXT_CAPTION,
    TEXT_LABEL,
)

ValueCallback = Callable[[str], None]
ChannelsCallback = Callable[[tuple[str, ...]], None]


class ToggleSetting(ft.Row):
    """A compact label/switch/value row."""

    def __init__(self, label: str, value: bool = False) -> None:
        self.value_label = ft.Text(_yes_no(value), size=TEXT_LABEL, color=NAVY)
        self.switch = ft.Switch(
            value=value,
            active_color=ft.Colors.WHITE,
            active_track_color=ACCENT,
            inactive_thumb_color=ft.Colors.WHITE,
            inactive_track_color=SWITCH_TRACK_OFF,
            on_change=self._handle_change,
            height=SEGMENT_HEIGHT,
        )
        super().__init__(
            controls=[
                field_label(label),
                ft.Container(expand=True),
                self.switch,
                self.value_label,
            ],
            spacing=SPACE_SM,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    @property
    def value(self) -> bool:
        return bool(self.switch.value)

    def _handle_change(self, _event: ft.Event[ft.Switch]) -> None:
        self.value_label.value = _yes_no(self.value)
        update_if_mounted(self.value_label)


def _yes_no(value: bool) -> str:
    return "Yes" if value else "No"


@dataclass(frozen=True)
class _Segment:
    box: ft.Container
    label: ft.Text


class ChoiceTabs(ft.Row):
    """Small segmented selection, e.g. plot mode or P/PI/PID."""

    def __init__(
        self,
        options: Sequence[str],
        selected: str,
        on_change: ValueCallback | None = None,
    ) -> None:
        if selected not in options:
            raise ValueError(f"selected value {selected!r} is not in {tuple(options)!r}")
        self.value = selected
        self._on_value_change = on_change
        self._segments = {
            option: self._build_segment(option, index, len(options))
            for index, option in enumerate(options)
        }
        super().__init__(
            controls=[segment.box for segment in self._segments.values()],
            spacing=0,
            expand=True,
        )
        self._refresh_styles()

    def _build_segment(self, option: str, index: int, total_options: int) -> _Segment:
        label = ft.Text(option, size=TEXT_CAPTION, color=MUTED)
        box = ft.Container(
            height=SEGMENT_HEIGHT,
            expand=True,
            alignment=ft.Alignment.CENTER,
            border=ft.Border.all(width=1, color=BORDER),
            border_radius=self._segment_radius(index, total_options),
            on_click=lambda _event, choice=option: self.select(choice),
            ink=True,
            content=label,
        )
        return _Segment(box, label)

    @staticmethod
    def _segment_radius(index: int, total_options: int) -> ft.BorderRadius:
        if index == 0:
            return ft.BorderRadius.horizontal(left=CONTROL_RADIUS)
        if index == total_options - 1:
            return ft.BorderRadius.horizontal(right=CONTROL_RADIUS)
        return ft.BorderRadius.all(0)

    def select(self, option: str) -> None:
        """Select one segment and notify consumers."""
        if option not in self._segments:
            raise ValueError(
                f"unknown choice {option!r}; expected one of {tuple(self._segments)!r}"
            )
        if option == self.value:
            return
        self.value = option
        self._refresh_styles()
        update_if_mounted(self)
        if self._on_value_change is not None:
            self._on_value_change(option)

    def _refresh_styles(self) -> None:
        for option, segment in self._segments.items():
            selected = option == self.value
            segment.box.bgcolor = ACCENT if selected else INPUT_FILL
            segment.label.color = ft.Colors.WHITE if selected else MUTED
            segment.label.weight = ft.FontWeight.W_500 if selected else ft.FontWeight.W_400


class LabeledChoice(ft.Row):
    """Inline label followed by ``ChoiceTabs`` (``Plot data?``, ``Controller type``)."""

    def __init__(
        self,
        label: str,
        options: Sequence[str],
        selected: str,
        on_change: ValueCallback | None = None,
    ) -> None:
        self.tabs = ChoiceTabs(options, selected, on_change)
        super().__init__(
            controls=[
                ft.Text(label, size=TEXT_LABEL, weight=ft.FontWeight.W_500),
                ft.Container(content=self.tabs, expand=True),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    @property
    def value(self) -> str:
        return self.tabs.value


def toggle_channel(
    selected: Sequence[str], channel: str, available: Sequence[str]
) -> tuple[str, ...]:
    """Add or remove ``channel``, keeping ``available`` order and one channel minimum."""
    if channel not in available:
        raise ValueError(f"channel {channel!r} is not in {tuple(available)!r}")
    chosen = set(selected)
    if channel not in chosen:
        chosen.add(channel)
    elif len(chosen) > 1:
        chosen.remove(channel)
    return tuple(option for option in available if option in chosen)


def format_channels(channels: Sequence[str]) -> str:
    return ", ".join(channels)


class ChannelPicker(ft.Column):
    """Multi-channel selector styled like a dropdown (AI/AO channels).

    Each menu entry toggles one channel; at least one stays selected.

    Example::

        ChannelPicker("AI channels", ("A0", "A1", "A2"), selected=("A0", "A1"))
    """

    def __init__(
        self,
        label: str,
        available: Sequence[str],
        selected: Sequence[str],
        on_change: ChannelsCallback | None = None,
    ) -> None:
        self._on_channels_change = on_change
        self._available: tuple[str, ...] = ()
        self.value: tuple[str, ...] = ()
        self._summary = ft.Text(size=TEXT_LABEL, color=NAVY, no_wrap=True)
        self._menu = ft.PopupMenuButton(
            expand=True,
            menu_position=ft.PopupMenuPosition.UNDER,
            content=self._build_box(),
        )
        self._apply(available, selected)
        super().__init__(
            controls=[field_label(label), ft.Row(controls=[self._menu], spacing=0)],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def _build_box(self) -> ft.Container:
        return ft.Container(
            height=CONTROL_HEIGHT,
            bgcolor=INPUT_FILL,
            border=ft.Border.all(width=1, color=BORDER),
            border_radius=CONTROL_RADIUS,
            padding=ft.Padding.symmetric(horizontal=12),
            content=ft.Row(
                controls=[
                    ft.Container(content=self._summary, expand=True),
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=NAVY),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def set_options(self, available: Sequence[str], selected: Sequence[str]) -> None:
        """Replace the channel list, e.g. when the device family changes."""
        self._apply(available, selected)
        update_if_mounted(self)

    def toggle(self, channel: str) -> None:
        """Toggle one channel and notify the host."""
        self.value = toggle_channel(self.value, channel, self._available)
        self._refresh()
        update_if_mounted(self)
        if self._on_channels_change is not None:
            self._on_channels_change(self.value)

    def _apply(self, available: Sequence[str], selected: Sequence[str]) -> None:
        unknown = [channel for channel in selected if channel not in available]
        if not selected or unknown:
            raise ValueError(
                f"selected channels {tuple(selected)!r} must be a non-empty subset "
                f"of {tuple(available)!r}"
            )
        self._available = tuple(available)
        self.value = tuple(channel for channel in available if channel in selected)
        self._menu.items = [
            ft.PopupMenuItem(
                content=channel,
                on_click=lambda _event, choice=channel: self.toggle(choice),
            )
            for channel in self._available
        ]
        self._refresh()

    def _refresh(self) -> None:
        self._summary.value = format_channels(self.value)
        for channel, item in zip(self._available, self._menu.items):
            item.checked = channel in self.value
