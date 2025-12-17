"""Constants for ha_crud component."""

DOMAIN = "ha_crud"

# API Base paths
API_BASE_PATH = "/api/config/dashboards"

# Lovelace data keys
LOVELACE_DATA = "lovelace"

# Dashboard modes
MODE_STORAGE = "storage"
MODE_YAML = "yaml"

# Configuration keys
CONF_URL_PATH = "url_path"
CONF_TITLE = "title"
CONF_ICON = "icon"
CONF_SHOW_IN_SIDEBAR = "show_in_sidebar"
CONF_REQUIRE_ADMIN = "require_admin"

# Error codes
ERR_DASHBOARD_NOT_FOUND = "dashboard_not_found"
ERR_DASHBOARD_EXISTS = "dashboard_already_exists"
ERR_INVALID_CONFIG = "invalid_config"
ERR_YAML_DASHBOARD = "yaml_dashboard_readonly"
ERR_DEFAULT_DASHBOARD = "default_dashboard_protected"
