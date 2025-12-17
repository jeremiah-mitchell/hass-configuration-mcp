# Claude Development Guide for HA CRUD

This document explains how to develop and test this custom component locally without pushing releases to GitHub.

## Environment

- **Home Assistant** runs in Kubernetes
- **Namespace:** `home-assistant`
- **Config path:** `/config/custom_components/`
- **API endpoint:** `https://home.kgamble.dev`
- **API token:** Stored in `.env` as `HASS_API_TOKEN`

## API Base Path

All endpoints use `/api/ha_crud/` prefix (NOT `/api/config/` to avoid conflicts with HA built-in routes).

## Local Development Deployment Flow

### 1. Get the current HA pod name

```bash
kubectl get pods -n home-assistant | grep -E "^home-assistant-[0-9a-z]+-[0-9a-z]+ "
```

The pod name follows the pattern: `home-assistant-<deployment-hash>-<pod-hash>`

### 2. Deploy the component to the container

```bash
# Set the pod name (get from step 1)
HA_POD="home-assistant-XXXXX-XXXXX"

# Remove old and copy new
kubectl exec -n home-assistant ${HA_POD} -c home-assistant -- rm -rf /config/custom_components/ha_crud
kubectl cp custom_components/ha_crud home-assistant/${HA_POD}:/config/custom_components/ha_crud -c home-assistant
```

### 3. Restart Home Assistant

Via API (use the token directly - don't source .env as it has shell compatibility issues):
```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  https://home.kgamble.dev/api/services/homeassistant/restart
```

### 4. Wait for HA to come back online (~30-45 seconds)

```bash
curl -s -H "Authorization: Bearer YOUR_TOKEN_HERE" https://home.kgamble.dev/api/
# Should return: {"message":"API running."}
```

### 5. Test the endpoints

```bash
# List dashboards
curl -s -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  https://home.kgamble.dev/api/ha_crud/dashboards

# Get default dashboard metadata
curl -s -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  https://home.kgamble.dev/api/ha_crud/dashboards/lovelace

# Get default dashboard config (views/cards)
curl -s -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  https://home.kgamble.dev/api/ha_crud/dashboards/lovelace/config
```

## One-Liner Deploy Script

```bash
HA_POD="home-assistant-XXXXX-XXXXX" && \
kubectl exec -n home-assistant ${HA_POD} -c home-assistant -- rm -rf /config/custom_components/ha_crud && \
kubectl cp custom_components/ha_crud home-assistant/${HA_POD}:/config/custom_components/ha_crud -c home-assistant && \
curl -X POST -H "Authorization: Bearer YOUR_TOKEN_HERE" https://home.kgamble.dev/api/services/homeassistant/restart && \
echo "Deployed and restarting HA..."
```

## Check Logs for Errors

```bash
HA_POD="home-assistant-XXXXX-XXXXX"
kubectl logs -n home-assistant ${HA_POD} -c home-assistant --tail=100 | grep -i ha_crud
```

## Important Notes

1. **Config flow setup required** - After first deployment, go to Settings > Integrations > Add Integration > "HA CRUD REST API" to enable the component

2. **Pod name changes** - The pod name changes on each deployment restart, update `HA_POD` variable accordingly

3. **HTTP views persist** - Once registered, HTTP views cannot be unregistered without a full HA restart

4. **Don't delete user dashboards** - This is a real Home Assistant instance. Test creates/updates on new dashboards only

5. **Shell sourcing issues** - Don't use `source .env` with curl commands as it can cause auth failures. Use the token directly.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ha_crud/dashboards` | List all dashboards |
| POST | `/api/ha_crud/dashboards` | Create new dashboard |
| GET | `/api/ha_crud/dashboards/{id}` | Get dashboard metadata |
| PUT | `/api/ha_crud/dashboards/{id}` | Full update metadata |
| PATCH | `/api/ha_crud/dashboards/{id}` | Partial update metadata |
| DELETE | `/api/ha_crud/dashboards/{id}` | Delete dashboard |
| GET | `/api/ha_crud/dashboards/{id}/config` | Get dashboard config (views/cards) |
| PUT | `/api/ha_crud/dashboards/{id}/config` | Replace dashboard config |

## Project Structure

```
custom_components/ha_crud/
├── __init__.py           # Entry point, registers views based on config
├── config_flow.py        # UI setup flow with resource selection
├── const.py              # Constants, resource types, API paths
├── errors.py             # Custom exceptions
├── manifest.json         # HA integration manifest
├── mcp_tools.json        # MCP tool definitions for Claude
├── strings.json          # UI translations
├── validation.py         # Request validation schemas
└── views/
    ├── __init__.py       # Exports view classes
    └── dashboards.py     # Dashboard CRUD endpoints
```

## Adding New Resource Types

1. Add constants in `const.py` (e.g., `RESOURCE_AUTOMATIONS`, `API_BASE_PATH_AUTOMATIONS`)
2. Create views in `views/automations.py`
3. Export from `views/__init__.py`
4. Register in `__init__.py` `_register_views()` function
5. Update `mcp_tools.json` with new tool definitions
