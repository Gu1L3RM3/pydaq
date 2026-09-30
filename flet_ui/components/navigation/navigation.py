"""Desktop and compact navigation controls."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from theme import ACCENT, ACCENT_SOFT, BORDER, MUTED, SIDEBAR_WIDTH, SURFACE

NavigationCallback = Callable[[int], None]


@dataclass(frozen=True)
class NavigationItem:
    """Metadata shared by desktop and compact navigation."""

    label: str
    icon: ft.IconData


NAVIGATION_ITEMS = (
    NavigationItem("Get Data", ft.Icons.BAR_CHART_ROUNDED),
    NavigationItem("Send Data", ft.Icons.SEND_OUTLINED),
    NavigationItem("Step Response", ft.Icons.SHOW_CHART_ROUNDED),
    NavigationItem("Get Model", ft.Icons.VIEW_IN_AR_OUTLINED),
    NavigationItem("PID Control", ft.Icons.TUNE_ROUNDED),
    NavigationItem("LQR Control", ft.Icons.ACCOUNT_TREE_OUTLINED),
)


class PydaqNavigationRail(ft.Container):
    """Navigation rail matching the PyDAQ desktop reference."""

    def __init__(
        self,
        on_change: NavigationCallback | None = None,
        selected_index: int = 0,
    ) -> None:
        self.selected_index = selected_index
        self.on_change = on_change
        self._destinations: list[tuple[ft.Container, ft.Container, ft.Icon, ft.Text]] = []
        menu_controls = [
            self._create_destination(index, item)
            for index, item in enumerate(NAVIGATION_ITEMS)
        ]
        super().__init__(
            width=SIDEBAR_WIDTH,
            bgcolor=SURFACE,
            border=ft.Border.only(right=ft.BorderSide(width=1, color=BORDER)),
            content=ft.Column(
                controls=[
                    self._create_logo(),
                    ft.Container(height=16),
                    *menu_controls,
                    ft.Container(expand=True),
                    self._create_footer(),
                ],
                spacing=2,
                expand=True,
            ),
        )
        self._update_destination_styles()

    @staticmethod
    def _create_logo() -> ft.Container:
        return ft.Container(
            height=120,
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.only(left=20, right=20, top=17),
            content=ft.Image(
                src="logo-no-background.png",
                width=172,
                fit=ft.BoxFit.CONTAIN,
                semantics_label="PyDAQ",
            ),
        )

    def _create_destination(self, index: int, item: NavigationItem) -> ft.Container:
        selection_bar = ft.Container(width=3, height=30, border_radius=4)
        icon = ft.Icon(item.icon, size=22, color=MUTED)
        label = ft.Text(item.label, size=14, color=MUTED, no_wrap=True)
        destination = ft.Container(
            height=48,
            margin=ft.Margin.symmetric(horizontal=8),
            padding=ft.Padding.only(right=8),
            border_radius=7,
            ink=True,
            on_click=lambda _event, item_index=index: self.select(item_index),
            content=ft.Row(
                controls=[
                    selection_bar,
                    ft.Container(width=6),
                    icon,
                    ft.Container(width=8),
                    label,
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        self._destinations.append((destination, selection_bar, icon, label))
        return destination

    @staticmethod
    def _create_footer() -> ft.Container:
        return ft.Container(
            padding=ft.Padding.only(left=19, right=12, bottom=18),
            content=ft.Column(
                controls=[
                    ft.Text("PYDAQ", size=12, color=MUTED, weight=ft.FontWeight.W_500),
                    ft.Text("Laboratory Data Acquisition", size=11, color="#9AA6B8"),
                    ft.Container(
                        width=83,
                        height=1.5,
                        bgcolor=ACCENT,
                        margin=ft.Margin.only(top=4, bottom=6),
                    ),
                    ft.Text("v1.0.0", size=10, color="#A5B0C0"),
                ],
                spacing=1,
            ),
        )

    def _update_destination_styles(self) -> None:
        for index, (destination, selection_bar, icon, label) in enumerate(
            self._destinations
        ):
            selected = index == self.selected_index
            destination.bgcolor = ACCENT_SOFT if selected else ft.Colors.TRANSPARENT
            selection_bar.bgcolor = ACCENT if selected else ft.Colors.TRANSPARENT
            icon.color = ACCENT if selected else MUTED
            label.color = ACCENT if selected else MUTED
            label.weight = ft.FontWeight.W_600 if selected else ft.FontWeight.W_400

    def select(self, index: int) -> None:
        """Select a destination and notify the application shell."""
        if index == self.selected_index:
            return
        self.selected_index = index
        self._update_destination_styles()
        self.update()
        if self.on_change is not None:
            self.on_change(index)


class CompactNavigation(ft.PopupMenuButton):
    """Space-efficient navigation used when the sidebar is hidden."""

    def __init__(self, on_change: NavigationCallback) -> None:
        super().__init__(
            icon=ft.Icons.MENU_ROUNDED,
            tooltip="Open navigation",
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[ft.Icon(item.icon, size=19), ft.Text(item.label)],
                        tight=True,
                    ),
                    on_click=lambda _event, item_index=index: on_change(item_index),
                )
                for index, item in enumerate(NAVIGATION_ITEMS)
            ],
        )


def create_sidebar(
    on_change: NavigationCallback | None = None,
    selected_index: int = 0,
) -> PydaqNavigationRail:
    """Create the standard desktop sidebar."""
    return PydaqNavigationRail(on_change=on_change, selected_index=selected_index)
