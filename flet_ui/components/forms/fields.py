"""Labeled input fields with the shared PyDAQ input style."""

from __future__ import annotations

from collections.abc import Callable, Sequence

import flet as ft

from components.forms.buttons import SecondaryButton
from components.mounting import update_if_mounted
from theme import (
    BORDER,
    CONTROL_HEIGHT,
    CONTROL_RADIUS,
    INPUT_FILL,
    NAVY,
    SPACE_SM,
    TEXT_LABEL,
)

ValueCallback = Callable[[str], None]

_INPUT_PADDING = ft.Padding.symmetric(horizontal=12, vertical=2)


def outline_border(color: str = BORDER) -> ft.OutlineInputBorder:
    return ft.OutlineInputBorder(
        side=ft.BorderSide(width=1, color=color),
        border_radius=CONTROL_RADIUS,
    )


def field_label(text: str) -> ft.Text:
    """Label text placed above or beside every form input."""
    return ft.Text(text, size=TEXT_LABEL, weight=ft.FontWeight.W_500, color=NAVY)


def _text_input(
    value: str,
    keyboard_type: ft.KeyboardType,
    suffix_icon: ft.IconData | None = None,
) -> ft.TextField:
    return ft.TextField(
        value=value,
        height=CONTROL_HEIGHT,
        text_size=TEXT_LABEL,
        color=NAVY,
        keyboard_type=keyboard_type,
        filled=True,
        fill_color=INPUT_FILL,
        border=outline_border(),
        content_padding=_INPUT_PADDING,
        suffix_icon=suffix_icon,
    )


def _labeled_column(label: str, control: ft.Control) -> list[ft.Control]:
    return [field_label(label), control]


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
            height=CONTROL_HEIGHT,
            text_size=TEXT_LABEL,
            color=NAVY,
            filled=True,
            fill_color=INPUT_FILL,
            border=outline_border(),
            content_padding=_INPUT_PADDING,
            on_select=self._handle_select,
            expand=True,
        )
        super().__init__(
            controls=_labeled_column(label, ft.Row(controls=[self.dropdown], spacing=0)),
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    @property
    def value(self) -> str:
        return self.dropdown.value or ""

    def set_options(self, options: Sequence[str], value: str) -> None:
        """Replace available values while keeping the field valid."""
        if value not in options:
            raise ValueError(f"value {value!r} is not in options {tuple(options)!r}")
        self.dropdown.options = [
            ft.DropdownOption(key=option, text=option) for option in options
        ]
        self.dropdown.value = value
        update_if_mounted(self.dropdown)

    def _handle_select(self, _event: ft.Event[ft.Dropdown]) -> None:
        if self._on_value_change is not None:
            self._on_value_change(self.value)


class LabeledTextField(ft.Column):
    """Free-text input such as Unit, Numerator or System equation."""

    def __init__(
        self,
        label: str,
        value: str = "",
        keyboard_type: ft.KeyboardType = ft.KeyboardType.TEXT,
    ) -> None:
        self.field = _text_input(value, keyboard_type)
        super().__init__(
            controls=_labeled_column(label, self.field),
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    @property
    def value(self) -> str:
        return self.field.value or ""


class LabeledNumberField(LabeledTextField):
    """Numeric input; the text is parsed by the page's form service."""

    def __init__(self, label: str, value: str) -> None:
        super().__init__(label, value, keyboard_type=ft.KeyboardType.NUMBER)


class PathField(ft.Column):
    """Path input with an attached browse action."""

    def __init__(
        self,
        value: str,
        on_browse: Callable[[], None] | None = None,
        label: str = "Path",
    ) -> None:
        self.field = _text_input(
            value, ft.KeyboardType.TEXT, suffix_icon=ft.Icons.FOLDER_OUTLINED
        )
        self.field.expand = True
        browse = SecondaryButton("Browse", on_click=on_browse)
        super().__init__(
            controls=_labeled_column(
                label, ft.Row(controls=[self.field, browse], spacing=SPACE_SM)
            ),
            spacing=2,
        )

    @property
    def value(self) -> str:
        return self.field.value or ""

    def set_value(self, value: str) -> None:
        """Show a path chosen elsewhere, e.g. from a file picker."""
        self.field.value = value
        update_if_mounted(self.field)
