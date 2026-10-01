"""Standard two-column layout: setup on the left, results on the right."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import flet as ft

from components.mounting import update_if_mounted
from theme import FADE_IN_MS, SPACE_XS

# Side by side the results column is twice the setup column (lg=8 vs lg=4);
# stacked, both span the full width.
_SIDE_BY_SIDE_RATIO = 1.5
# Sub-pixel differences come from layout rounding; ignoring them stops resize loops.
_SLACK_TOLERANCE = 0.5


@runtime_checkable
class AbsorbsSlack(Protocol):
    """Cards that can add empty height so both columns end on the same line."""

    slack: float

    def set_slack(self, height: float) -> None: ...


def balanced_slack(
    setup_width: float, setup_height: float, results_width: float, results_height: float
) -> tuple[float, float]:
    """Extra (setup, results) height that evens out side-by-side columns.

    Heights are content-only (without any slack already added). Stacked or
    unmeasured columns need none.
    """
    if setup_width <= 0 or results_width < setup_width * _SIDE_BY_SIDE_RATIO:
        return (0.0, 0.0)
    tallest = max(setup_height, results_height)
    return (tallest - setup_height, tallest - results_height)


class WorkflowLayout(ft.Column):
    """Header above a setup panel (``lg=4``) and a results area (``lg=8``).

    Below the ``lg`` breakpoint the setup stacks above the results. Side by
    side, the shorter card grows through ``AbsorbsSlack`` so both end on the
    same line. The cards stay transparent until both are measured and evened
    out, so the first visible frame is already final. Pages subclass it or build it directly::

        WorkflowLayout(PageHeader("Send Data", "..."), setup_panel, signal_card)
    """

    def __init__(
        self, header: ft.Control, setup: ft.Control, results: ft.Control
    ) -> None:
        self._setup = setup
        self._results = results
        self._sizes = {"setup": (0.0, 0.0), "results": (0.0, 0.0)}
        # ``ResponsiveRow`` cannot stretch its runs inside a scrolling column, so
        # the heights are evened out from measured sizes instead.
        self._content = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 12, "lg": 4},
                    content=setup,
                    on_size_change=lambda event: self._record("setup", event),
                ),
                ft.Container(
                    col={"xs": 12, "lg": 8},
                    content=results,
                    on_size_change=lambda event: self._record("results", event),
                ),
            ],
            spacing=10,
            run_spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
            # Revealed by ``_reveal``; without this the action visibly jumps
            # down when the slack lands one layout pass after the first frame.
            opacity=0,
            animate_opacity=ft.Animation(FADE_IN_MS, ft.AnimationCurve.EASE_OUT),
        )
        super().__init__(
            controls=[header, ft.Container(height=SPACE_XS), self._content],
            spacing=6,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    @property
    def revealed(self) -> bool:
        return self._content.opacity == 1

    def _record(self, column: str, event: ft.LayoutSizeChangeEvent[ft.Container]) -> None:
        self.measure(column, event.width, event.height)

    def measure(self, column: str, width: float, height: float) -> None:
        """Take a rendered size of the ``"setup"`` or ``"results"`` column."""
        if column not in self._sizes:
            raise ValueError(f"column must be 'setup' or 'results', not {column!r}")
        self._sizes[column] = (width, height)
        self._balance()
        self._reveal()

    def _balance(self) -> None:
        setup_width, setup_height = self._sizes["setup"]
        results_width, results_height = self._sizes["results"]
        setup_slack, results_slack = balanced_slack(
            setup_width,
            setup_height - _current_slack(self._setup),
            results_width,
            results_height - _current_slack(self._results),
        )
        _apply_slack(self._setup, setup_slack)
        _apply_slack(self._results, results_slack)

    def _reveal(self) -> None:
        both_measured = all(width > 0 for width, _height in self._sizes.values())
        if self.revealed or not both_measured:
            return
        self._content.opacity = 1
        update_if_mounted(self._content)


def _current_slack(card: ft.Control) -> float:
    return card.slack if isinstance(card, AbsorbsSlack) else 0.0


def _apply_slack(card: ft.Control, height: float) -> None:
    if not isinstance(card, AbsorbsSlack):
        return
    if abs(card.slack - height) < _SLACK_TOLERANCE:
        return
    card.set_slack(height)
