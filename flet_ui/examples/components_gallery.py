"""Shared PyDAQ components composed into a Step Response-style page.

Reference for new routes and a visual check of the component kit. Run from
``flet_ui/``::

    uv run flet run examples/components_gallery.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import flet as ft

# Script directory imports (``from theme import …``) need ``flet_ui/`` on the path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components.charts.signal_card import SignalCard  # noqa: E402
from components.charts.signal_plot import SignalPlot  # noqa: E402
from components.charts.status_badge import (  # noqa: E402
    RateIndicator,
    SessionStatus,
    StatusBadge,
)
from components.device_selector import DeviceSelector  # noqa: E402
from components.forms.buttons import PrimaryActionButton, SecondaryButton  # noqa: E402
from components.forms.choices import LabeledChoice  # noqa: E402
from components.forms.fields import LabeledNumberField  # noqa: E402
from components.page_header import PageHeader  # noqa: E402
from components.setup.device_section import (  # noqa: E402
    ChannelOptions,
    DeviceChoices,
    DeviceSection,
)
from components.setup.output_section import OutputSection  # noqa: E402
from components.setup.setup_panel import SetupPanel  # noqa: E402
from components.setup.timing_section import TimingSection  # noqa: E402
from components.workflow_layout import WorkflowLayout  # noqa: E402
from theme import BACKGROUND, SPACE_LG, app_theme  # noqa: E402

STEP_CHOICES = DeviceChoices(
    devices=("COM3 · Arduino Uno",),
    ai_channels=ChannelOptions(("A0", "A1", "A2"), selected=("A0",)),
    ao_channels=ChannelOptions(("D9", "D10"), selected=("D9",)),
)


def _first_order_response(times: list[float]) -> tuple[list[float], list[float]]:
    step = [0.0 if time < 5 else 5.0 for time in times]
    output = [0.0 if time < 5 else 4.2 * (1 - math.exp(-(time - 5) / 3)) for time in times]
    return step, output


def _build_setup() -> SetupPanel:
    tuning = LabeledChoice("Get PID parameters?", ("No", "P", "PI", "PID"), "No")
    return SetupPanel(
        "Step setup",
        "Apply a step on the output and record the response.",
        sections=(
            DeviceSection(STEP_CHOICES),
            TimingSection(
                duration="30", extra_fields=(LabeledNumberField("Step ON (s)", "5"),)
            ),
            tuning,
            SecondaryButton("Advanced settings", icon=ft.Icons.TUNE_ROUNDED),
            OutputSection(),
        ),
        action=PrimaryActionButton("Start step response", "Stop step response"),
    )


def _build_results() -> SignalCard:
    plot = SignalPlot(("u", "y"), y_range=(0, 6), duration_s=30, height=360)
    times = [index * 0.1 for index in range(301)]
    step, output = _first_order_response(times)
    plot.set_points(times, {"u": step, "y": output})
    badges = [StatusBadge(status) for status in SessionStatus]
    return SignalCard(
        "Step response",
        "Static result rendered with SignalPlot.set_points.",
        plot=plot,
        indicators=(*badges, RateIndicator("10 Hz")),
    )


def main(page: ft.Page) -> None:
    page.title = "PyDAQ · Components"
    page.theme = app_theme()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BACKGROUND
    page.padding = SPACE_LG
    header = PageHeader(
        "Step response",
        "Every control below comes from flet_ui/components.",
        trailing=DeviceSelector(),
    )
    page.add(WorkflowLayout(header, setup=_build_setup(), results=_build_results()))


if __name__ == "__main__":
    ft.run(main, assets_dir="../assets")
