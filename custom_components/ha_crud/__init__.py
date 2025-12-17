"""Home Assistant CRUD REST API component.

This component exposes REST endpoints for managing Home Assistant
resources like Lovelace dashboards.

Endpoints:
    GET  /api/config/dashboards         - List all dashboards
    POST /api/config/dashboards         - Create new dashboard
    GET  /api/config/dashboards/{id}    - Get dashboard metadata
    PUT  /api/config/dashboards/{id}    - Full update metadata
    PATCH /api/config/dashboards/{id}   - Partial update metadata
    DELETE /api/config/dashboards/{id}  - Delete dashboard
    GET  /api/config/dashboards/{id}/config  - Get dashboard config
    PUT  /api/config/dashboards/{id}/config  - Replace dashboard config
"""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .views import (
    DashboardConfigView,
    DashboardDetailView,
    DashboardListView,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HA CRUD REST API component."""

    # Register HTTP views for dashboard management
    hass.http.register_view(DashboardListView())
    hass.http.register_view(DashboardDetailView())
    hass.http.register_view(DashboardConfigView())

    _LOGGER.info(
        "HA CRUD REST API registered. Dashboard endpoints available at /api/config/dashboards"
    )

    return True
