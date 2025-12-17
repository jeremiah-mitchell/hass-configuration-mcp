"""Views for ha_crud component."""

from .dashboards import (
    DashboardConfigView,
    DashboardDetailView,
    DashboardListView,
)

__all__ = [
    "DashboardListView",
    "DashboardDetailView",
    "DashboardConfigView",
]
