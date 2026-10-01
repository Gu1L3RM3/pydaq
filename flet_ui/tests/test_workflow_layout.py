"""Tests for evening out the setup and results column heights."""

from __future__ import annotations

import flet as ft
import pytest

from components.charts.signal_card import SignalCard
from components.forms.buttons import PrimaryActionButton
from components.setup.setup_panel import SetupPanel
from components.workflow_layout import AbsorbsSlack, balanced_slack


def test_shorter_setup_gets_the_difference() -> None:
    assert balanced_slack(400, 600, 800, 634) == (34, 0)


def test_shorter_results_get_the_difference() -> None:
    assert balanced_slack(400, 638, 800, 634) == (0, 4)


@pytest.mark.parametrize(
    ("setup_width", "results_width"),
    [(0, 800), (800, 800), (380, 380)],
)
def test_stacked_or_unmeasured_columns_need_no_slack(
    setup_width: float, results_width: float
) -> None:
    assert balanced_slack(setup_width, 600, results_width, 634) == (0, 0)


def test_setup_panel_absorbs_slack_above_the_action() -> None:
    panel = SetupPanel(
        "Setup", "", sections=(ft.Text("field"),), action=PrimaryActionButton("Go", "Stop")
    )

    panel.set_slack(34)

    assert isinstance(panel, AbsorbsSlack)
    assert (panel.slack, panel._spacer.height) == (34, 34)


def test_signal_card_absorbs_slack_below_the_plot() -> None:
    card = SignalCard("Result", "", plot=ft.Text("plot"))

    card.set_slack(4)

    assert isinstance(card, AbsorbsSlack)
    assert (card.slack, card._spacer.height) == (4, 4)
