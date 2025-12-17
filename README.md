# HA CRUD REST API

A Home Assistant custom component that exposes REST endpoints for managing Lovelace dashboards programmatically. Designed to integrate with Claude or other AI tools via MCP.

## Features

- Full CRUD operations for Lovelace dashboards
- Separate endpoints for dashboard metadata vs. configuration (views/cards)
- Bearer token authentication (uses HA long-lived access tokens)
- Admin permission enforcement for write operations
- Support for storage-mode dashboards (YAML dashboards are read-only)

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS
2. Search for "HA CRUD REST API" and install
3. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/ha_crud` folder to your Home Assistant config directory:

```bash
cp -r custom_components/ha_crud /path/to/homeassistant/config/custom_components/
```

2. Restart Home Assistant

3. Verify installation by checking the logs for:
   ```
   HA CRUD REST API registered. Dashboard endpoints available at /api/config/dashboards
   ```

## Configuration

No configuration is required. The component auto-loads on startup and registers the API endpoints.

## Authentication

All endpoints require a valid Home Assistant long-lived access token.

### Creating a Long-Lived Access Token

1. Go to your Home Assistant profile (click your username in the sidebar)
2. Scroll to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Give it a name (e.g., "Claude Dashboard API")
5. Copy the token (you won't see it again)

### Using the Token

Include the token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://homeassistant.local:8123/api/config/dashboards
```

## API Reference

### Base URL

```
http://homeassistant.local:8123/api/config/dashboards
```

### Endpoints

| Method | Endpoint | Description | Admin Required |
|--------|----------|-------------|----------------|
| GET | `/` | List all dashboards | No |
| POST | `/` | Create new dashboard | Yes |
| GET | `/{id}` | Get dashboard metadata | No |
| PUT | `/{id}` | Full update metadata | Yes |
| PATCH | `/{id}` | Partial update metadata | Yes |
| DELETE | `/{id}` | Delete dashboard | Yes |
| GET | `/{id}/config` | Get dashboard config (views/cards) | No |
| PUT | `/{id}/config` | Replace dashboard config | Yes |

### List All Dashboards

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://homeassistant.local:8123/api/config/dashboards
```

**Response:**
```json
[
  {
    "id": "lovelace",
    "url_path": null,
    "mode": "storage",
    "title": "Home",
    "icon": "mdi:home",
    "show_in_sidebar": true,
    "require_admin": false
  },
  {
    "id": "my-dashboard",
    "url_path": "my-dashboard",
    "mode": "storage",
    "title": "My Dashboard",
    "icon": "mdi:view-dashboard",
    "show_in_sidebar": true,
    "require_admin": false
  }
]
```

### Get Dashboard Metadata

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://homeassistant.local:8123/api/config/dashboards/my-dashboard
```

Use `lovelace` as the ID for the default dashboard.

### Get Dashboard Configuration (Views/Cards)

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://homeassistant.local:8123/api/config/dashboards/my-dashboard/config
```

**Response:**
```json
{
  "views": [
    {
      "title": "Living Room",
      "path": "living-room",
      "cards": [
        {
          "type": "light",
          "entity": "light.living_room"
        }
      ]
    }
  ]
}
```

### Create a New Dashboard

```bash
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url_path": "my-new-dashboard",
    "title": "My New Dashboard",
    "icon": "mdi:view-dashboard",
    "show_in_sidebar": true,
    "require_admin": false
  }' \
  http://homeassistant.local:8123/api/config/dashboards
```

**Note:** The `url_path` must contain a hyphen (Home Assistant requirement).

**Response (201 Created):**
```json
{
  "id": "my-new-dashboard",
  "url_path": "my-new-dashboard",
  "title": "My New Dashboard",
  "icon": "mdi:view-dashboard",
  "show_in_sidebar": true,
  "require_admin": false,
  "mode": "storage"
}
```

### Upload Dashboard Configuration

```bash
curl -X PUT \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "views": [
      {
        "title": "Main",
        "path": "main",
        "cards": [
          {
            "type": "markdown",
            "content": "Welcome to my dashboard!"
          }
        ]
      }
    ]
  }' \
  http://homeassistant.local:8123/api/config/dashboards/my-new-dashboard/config
```

### Update Dashboard Metadata (Full)

```bash
curl -X PUT \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "icon": "mdi:home-assistant",
    "show_in_sidebar": true,
    "require_admin": false
  }' \
  http://homeassistant.local:8123/api/config/dashboards/my-dashboard
```

### Update Dashboard Metadata (Partial)

```bash
curl -X PATCH \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title"}' \
  http://homeassistant.local:8123/api/config/dashboards/my-dashboard
```

### Delete a Dashboard

```bash
curl -X DELETE \
  -H "Authorization: Bearer TOKEN" \
  http://homeassistant.local:8123/api/config/dashboards/my-dashboard
```

**Response:** `204 No Content`

**Note:** Cannot delete the default `lovelace` dashboard or YAML-based dashboards.

## Error Responses

All errors return JSON with a message and error code:

```json
{
  "message": "Dashboard 'xyz' not found",
  "code": "dashboard_not_found"
}
```

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `invalid_config` | Request body validation failed |
| 401 | - | Missing or invalid authentication |
| 404 | `dashboard_not_found` | Dashboard does not exist |
| 409 | `dashboard_already_exists` | URL path already in use |
| 409 | `yaml_dashboard_readonly` | Cannot modify YAML dashboard |
| 409 | `default_dashboard_protected` | Cannot delete default dashboard |

## Claude/MCP Integration

The `mcp_tools.json` file contains tool definitions for integrating with Claude or other MCP-compatible AI systems.

### Setup with Claude

1. Locate the `mcp_tools.json` file in the component directory
2. Update the `baseUrl` to match your Home Assistant instance
3. Configure your MCP server to use these tool definitions
4. Set the Bearer token in your MCP authentication config

### Available Tools

| Tool Name | Description |
|-----------|-------------|
| `ha_list_dashboards` | List all dashboards |
| `ha_get_dashboard` | Get dashboard metadata |
| `ha_get_dashboard_config` | Get dashboard views/cards |
| `ha_create_dashboard` | Create new dashboard |
| `ha_update_dashboard` | Full update metadata |
| `ha_patch_dashboard` | Partial update metadata |
| `ha_update_dashboard_config` | Upload dashboard config |
| `ha_delete_dashboard` | Delete dashboard |

## Troubleshooting

### "Dashboard collection not available"

This error occurs when Lovelace is running in YAML mode. The component requires storage mode for creating/modifying dashboards.

To check your mode:
1. Go to Settings > Dashboards
2. If you see "Edit Dashboard" in the overflow menu, you're in storage mode

### "URL path must contain a hyphen"

Home Assistant requires dashboard URL paths to contain at least one hyphen. Use paths like `my-dashboard` instead of `mydashboard`.

### "Admin permission required"

Write operations (POST, PUT, PATCH, DELETE) require the token owner to be an admin user.

## License

MIT License - See LICENSE file for details.

## Contributing

Issues and pull requests welcome at the project repository.
