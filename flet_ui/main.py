"""PyDAQ Flet application entry point."""

from __future__ import annotations

import flet as ft

from components.navigation.navigation import CompactNavigation, create_sidebar
from pages.routes import APP_ROUTES, navigation_items
from theme import BACKGROUND, MOBILE_BREAKPOINT, NAVY, SPACE_LG, app_theme


class ApplicationShell(ft.Row):
    """Responsive navigation shell that owns route presentation."""

    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._page_host = ft.Container(expand=True, content=APP_ROUTES[0].build())
        menu_items = navigation_items()
        self._sidebar = create_sidebar(menu_items, on_change=self.select_page)
        self._compact_header = ft.Container(
            visible=False,
            padding=ft.Padding.only(left=12, right=16, top=6, bottom=6),
            content=ft.Row(
                controls=[
                    CompactNavigation(menu_items, on_change=self.select_page),
                    ft.Text("PYDAQ", weight=ft.FontWeight.BOLD, color=NAVY),
                ],
                tight=True,
            ),
        )
        content = ft.Column(
            controls=[
                self._compact_header,
                ft.Container(
                    content=self._page_host,
                    padding=ft.Padding.all(SPACE_LG),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
        super().__init__(
            controls=[self._sidebar, content],
            spacing=0,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def select_page(self, index: int) -> None:
        """Display one registered page and synchronize navigation state."""
        if not 0 <= index < len(APP_ROUTES):
            raise ValueError(f"route index {index} is outside the registered range")
        self._page_host.content = APP_ROUTES[index].build()
        if self._sidebar.selected_index != index:
            self._sidebar.select(index)
        self._page.title = f"PyDAQ · {APP_ROUTES[index].title}"
        self._page.update()

    def resize(self, width: float | None) -> None:
        """Switch navigation mode without rebuilding the current page."""
        desktop = width is None or width >= MOBILE_BREAKPOINT
        self._sidebar.visible = desktop
        self._compact_header.visible = not desktop
        self._page.update()


def main(page: ft.Page) -> None:
    """Configure the window and mount the application shell."""
    page.title = f"PyDAQ · {APP_ROUTES[0].title}"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = app_theme()
    page.padding = 0
    page.bgcolor = BACKGROUND
    page.window.min_width = 420
    page.window.min_height = 640

    shell = ApplicationShell(page)
    page.on_resize = lambda _event: shell.resize(page.width)
    page.add(shell)
    shell.resize(page.width)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
