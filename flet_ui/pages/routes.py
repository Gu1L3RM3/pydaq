"""Route registry for the Flet application shell."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from pages.get_data import build_get_data_page
from pages.get_model import build_get_model_page
from pages.lqr_control import build_lqr_control_page
from pages.pid_control import build_pid_control_page
from pages.send_data import build_send_data_page
from pages.step_response import build_step_response_page

PageBuilder = Callable[[], ft.Control]


@dataclass(frozen=True)
class AppRoute:
    title: str
    build: PageBuilder


APP_ROUTES = (
    AppRoute("Get Data", build_get_data_page),
    AppRoute("Send Data", build_send_data_page),
    AppRoute("Step Response", build_step_response_page),
    AppRoute("Get Model", build_get_model_page),
    AppRoute("PID Control", build_pid_control_page),
    AppRoute("LQR Control", build_lqr_control_page),
)
