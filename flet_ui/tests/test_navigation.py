"""Tests for route-derived navigation."""

from __future__ import annotations

from components.navigation.navigation import CompactNavigation, PydaqNavigationRail
from pages.routes import APP_ROUTES, navigation_items


def test_navigation_items_follow_route_order() -> None:
    items = navigation_items()

    assert [item.label for item in items] == [route.title for route in APP_ROUTES]
    assert [item.icon for item in items] == [route.icon for route in APP_ROUTES]


def test_navigation_controls_render_one_entry_per_route() -> None:
    items = navigation_items()

    assert len(PydaqNavigationRail(items)._destinations) == len(APP_ROUTES)
    assert len(CompactNavigation(items, on_change=lambda _index: None).items) == len(
        APP_ROUTES
    )
