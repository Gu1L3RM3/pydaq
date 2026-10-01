"""Tests for signal chart axis and label helpers."""

from __future__ import annotations

import pytest

from components.live_chart import (
    CHANNEL_COLORS,
    channel_color,
    format_sample_rate,
    time_axis_ticks,
)


@pytest.mark.parametrize(
    ("duration_s", "expected"),
    [
        (100, tuple(range(0, 101, 10))),
        (150, tuple(range(0, 141, 20))),
        (7, tuple(range(0, 8))),
        (0.5, (0,)),
    ],
)
def test_time_axis_ticks_use_round_steps(duration_s: float, expected: tuple[int, ...]) -> None:
    assert time_axis_ticks(duration_s) == expected


def test_time_axis_ticks_reject_non_positive_duration() -> None:
    with pytest.raises(ValueError, match="duration_s must be positive, received 0"):
        time_axis_ticks(0)


def test_format_sample_rate_inverts_period() -> None:
    assert format_sample_rate(0.01) == "100 Hz"
    assert format_sample_rate(0.4) == "2.5 Hz"


def test_channel_color_cycles_through_palette() -> None:
    assert channel_color(0) == CHANNEL_COLORS[0]
    assert channel_color(len(CHANNEL_COLORS)) == CHANNEL_COLORS[0]
