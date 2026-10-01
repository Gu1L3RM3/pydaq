"""Reusable acquisition form controls."""

from __future__ import annotations

from collections.abc import Callable, Sequence

import flet as ft

from theme import (
    ACCENT,
    BORDER,
    CONTROL_RADIUS,
    INPUT_FILL,
    MUTED,
    NAVY,
    SPACE_SM,
)

ValueCallback = Callable[[str], None]


def _outline_border(color: str = BORDER) -> ft.OutlineInputBorder:
    return ft.OutlineInputBorder(
        side=ft.BorderSide(width=1, color=color),
        border_radius=CONTROL_RADIUS,
    )


class LabeledDropdown(ft.Column):
    """A consistently styled labeled dropdown."""

    def __init__(
        self,
        label: str,
        options: Sequence[str],
        value: str,
        on_change: ValueCallback | None = None,
    ) -> None:
        self._on_value_change = on_change
        self.dropdown = ft.Dropdown(
            value=value,
            options=[ft.DropdownOption(key=option, text=option) for option in options],
            height=36,
            text_size=14,
            color=NAVY,
            filled=True,
            fill_color=INPUT_FILL,
            border=_outline_border(),
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=2),
            on_select=self._handle_select,
            expand=True,
        )
        super().__init__(
            controls=[
                ft.Text(label, size=14, weight=ft.FontWeight.W_500, color=NAVY),
                ft.Row(controls=[self.dropdown], spacing=0),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    @property
    def value(self) -> str:
        return self.dropdown.value or ""

    def set_options(self, options: Sequence[str], value: str) -> None:
        """Replace available values while keeping the field valid."""
        self.dropdown.options = [
            ft.DropdownOption(key=option, text=option) for option in options
        ]
        self.dropdown.value = value
        self.dropdown.update()

    def _handle_select(self, _event: ft.Event[ft.Dropdown]) -> None:
        if self._on_value_change is not None:
            self._on_value_change(self.value)


class LabeledNumberField(ft.Column):
    """A numeric text field sharing the same dimensions as dropdowns."""

    def __init__(self, label: str, value: str) -> None:
        self.field = ft.TextField(
            value=value,
            height=36,
            text_size=14,
            color=NAVY,
            keyboard_type=ft.KeyboardType.NUMBER,
            filled=True,
            fill_color=INPUT_FILL,
            border=_outline_border(),
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=2),
        )
        super().__init__(
            controls=[
                ft.Text(label, size=14, weight=ft.FontWeight.W_500, color=NAVY),
                self.field,
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )


class ToggleSetting(ft.Row):
    """A compact label/switch/value row."""

    def __init__(self, label: str, value: bool = False) -> None:
        self.value_label = ft.Text("Yes" if value else "No", size=14, color=NAVY)
        self.switch = ft.Switch(
            value=value,
            active_color=ft.Colors.WHITE,
            active_track_color=ACCENT,
            inactive_thumb_color=ft.Colors.WHITE,
            inactive_track_color="#B8C1D0",
            on_change=self._handle_change,
            height=32,
        )
        super().__init__(
            controls=[
                ft.Text(label, size=14, weight=ft.FontWeight.W_500, color=NAVY),
                ft.Container(expand=True),
                self.switch,
                self.value_label,
            ],
            spacing=SPACE_SM,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _handle_change(self, _event: ft.Event[ft.Switch]) -> None:
        self.value_label.value = "Yes" if self.switch.value else "No"
        self.value_label.update()


class ChoiceTabs(ft.Row):
    """Small segmented selection control used by acquisition settings."""

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
        self._segments: dict[str, ft.Container] = {}
        controls = [
            self._build_segment(option, index, len(options))
            for index, option in enumerate(options)
        ]
        super().__init__(controls=controls, spacing=0, expand=True)
        self._refresh_styles()

    def _build_segment(
        self, option: str, index: int, total_options: int
    ) -> ft.Container:
        segment = ft.Container(
            height=32,
            expand=True,
            alignment=ft.Alignment.CENTER,
            border=ft.Border.all(width=1, color=BORDER),
            border_radius=self._segment_radius(index, total_options),
            on_click=lambda _event, choice=option: self.select(choice),
            ink=True,
            content=ft.Text(option, size=13, color=MUTED),
        )
        self._segments[option] = segment
        return segment

    @staticmethod
    def _segment_radius(index: int, total_options: int) -> ft.BorderRadius:
        if index == 0:
            return ft.BorderRadius.horizontal(left=CONTROL_RADIUS)
        if index == total_options - 1:
            return ft.BorderRadius.horizontal(right=CONTROL_RADIUS)
        return ft.BorderRadius.all(0)

    def select(self, option: str) -> None:
        """Select one segment and notify consumers."""
        if option == self.value:
            return
        if option not in self._segments:
            raise ValueError(f"unknown choice {option!r}")
        self.value = option
        self._refresh_styles()
        self.update()
        if self._on_value_change is not None:
            self._on_value_change(option)

    def _refresh_styles(self) -> None:
        for option, segment in self._segments.items():
            selected = option == self.value
            segment.bgcolor = ACCENT if selected else INPUT_FILL
            label = segment.content
            if isinstance(label, ft.Text):
                label.color = ft.Colors.WHITE if selected else MUTED
                label.weight = ft.FontWeight.W_500 if selected else ft.FontWeight.W_400


class PathField(ft.Column):
    """Path input with an attached browse action."""

    def __init__(self, value: str, on_browse: Callable[[], None] | None = None) -> None:
        self._on_browse = on_browse
        self.field = ft.TextField(
            value=value,
            height=36,
            expand=True,
            text_size=14,
            color=NAVY,
            filled=True,
            fill_color=INPUT_FILL,
            border=_outline_border(),
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=2),
            suffix_icon=ft.Icons.FOLDER_OUTLINED,
        )
        browse = ft.Button(
            "Browse",
            height=36,
            style=ft.ButtonStyle(
                color=NAVY,
                bgcolor="#F1F4F8",
                side=ft.BorderSide(width=1, color=BORDER),
                shape=ft.RoundedRectangleBorder(radius=CONTROL_RADIUS),
            ),
            on_click=self._browse,
        )
        super().__init__(
            controls=[
                ft.Text("Path", size=14, weight=ft.FontWeight.W_500, color=NAVY),
                ft.Row(controls=[self.field, browse], spacing=SPACE_SM),
            ],
            spacing=2,
        )

    def _browse(self, _event: ft.Event[ft.Button]) -> None:
        if self._on_browse is not None:
            self._on_browse()
