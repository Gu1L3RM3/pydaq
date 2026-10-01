"""Route registry for the Flet application shell."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import flet as ft

from components.navigation.navigation import NavigationItem
from pages.get_data import build_get_data_page
from pages.get_model import build_get_model_page
from pages.lqr_control import build_lqr_control_page
from pages.pid_control import build_pid_control_page
from pages.send_data import build_send_data_page
from pages.step_response import build_step_response_page

PageBuilder = Callable[[], ft.Control]


@dataclass(frozen=True)
class AppRoute:
    """One page of the shell; tuple order is the navigation order."""

    title: str
    icon: ft.IconData
    build: PageBuilder


APP_ROUTES = (
    AppRoute("Get Data", ft.Icons.BAR_CHART_ROUNDED, build_get_data_page),
    AppRoute("Send Data", ft.Icons.SEND_OUTLINED, build_send_data_page),
    AppRoute("Step Response", ft.Icons.SHOW_CHART_ROUNDED, build_step_response_page),
    AppRoute("Get Model", ft.Icons.VIEW_IN_AR_OUTLINED, build_get_model_page),
    AppRoute("PID Control", ft.Icons.TUNE_ROUNDED, build_pid_control_page),
    AppRoute("LQR Control", ft.Icons.ACCOUNT_TREE_OUTLINED, build_lqr_control_page),
)


def navigation_items(
    routes: Sequence[AppRoute] = APP_ROUTES,
) -> tuple[NavigationItem, ...]:
    """Derive menu entries from routes so both always share index order."""
    return tuple(NavigationItem(route.title, route.icon) for route in routes)
