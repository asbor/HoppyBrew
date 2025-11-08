# API Reference

The FastAPI backend exposes a consistent REST surface across recipes, batches, inventory, references, and integrations. Every router is tagged so the OpenAPI UI (`/docs`) mirrors the structure in `api/router.py`.

- **Base URL (local dev)**: `http://localhost:8000`
- **Content type**: `application/json; charset=utf-8`
- **Authentication**: currently open for internal use; production deployments must sit behind VPN/Cloudflare Access until user auth hardening ships.
- **Schemas**: Pydantic models live under `services/backend/Database/Schemas`. They define the fields returned by each endpoint.

## Request Flow

![Create User Flow](diagrams/misc/create-new-user.png)

Typical workflow:

1. Frontend composable calls the matching router (`useRecipes`, `useBatches`, etc.).
2. Request hits the APIRouter tag (e.g., `recipes`) and is validated against the schema module.
3. Database session performs work via SQLAlchemy models under `Database/Models`.
4. Response is serialized back to the UI or an integration (HomeAssistant, ISpindel, etc.).

## Domain Surface Area

| Domain | Endpoints (HTTP verbs) | Notes |
| --- | --- | --- |
| Recipes (`/recipes`) | `GET /recipes`, `GET /recipes/{id}`, `POST /recipes`, `PUT /recipes/{id}`, `DELETE /recipes/{id}` | CRUD plus clone-from-template, integrated fermentable/hop/yeast lists |
| Batches (`/batches`) | Fetch all/by id, create, update status, delete | Tracks lifecycle states (planning → brew day → fermentation → conditioning → packaged) with gravity readings |
| Ingredients (`/hops`, `/fermentables`, `/yeasts`, `/miscs`) | Standard CRUD plus search filters | Values normalized to metric units (grams, liters, °C) with conversion helpers |
| Inventory (`/inventory`) | Derived from ingredient tables; use `/inventory/{id}` operations | Inventory rows reference the ingredient-specific IDs; see [Database Schema](Database-Schema.md) |
| Profiles (`/mash-profiles`, `/fermentation-profiles`, `/equipment`, `/water-profiles`) | Manage process templates | Each profile endpoint ensures dependent steps (mash steps, fermentation stages) stay consistent |
| References (`/style-guideline-sources`, `/beer-styles`, `/style-categories`) | Manage BJCP sources, categories, and individual styles | Supports bulk refresh via `/refresh-beer-styles` background task |
| Devices (`/devices`) | CRUD for external sensors/controllers | Coupled with `homeassistant` endpoints and future MQTT discovery |
| Logs & Health (`/logs`, `/health`) | Rolling log buffer access plus heartbeat | `/logs` provides paginated log lines for UI troubleshooting |
| HomeAssistant (`/homeassistant/batches`, `/homeassistant/batches/{id}`, `/homeassistant/summary`) | REST sensor payloads and brewery summaries | Output matches `HomeAssistantBatchSensor` & `HomeAssistantSummary` schemas |

> 📚 **Complete catalog** – See `api_endpoint_catalog.md` (auto-generated) for every verb/path combination, handler name, and schema reference.

## Usage Examples

### Recipes

```bash
curl -X POST http://localhost:8000/recipes \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Citra Pale Ale",
        "style_id": "uuid",
        "batch_size_l": 20,
        "efficiency": 72,
        "hops": [...],
        "fermentables": [...],
        "yeast_id": "uuid"
      }'
```

### Inventory Lookups

```bash
curl http://localhost:8000/hops?alpha_acid_min=10&usage=boil
```

### HomeAssistant REST Sensor

```yaml
sensor:
  - platform: rest
    resource: https://your-host/homeassistant/summary
    name: HoppyBrew Brewery Summary
    value_template: "{{ value_json.active_batches }}"
```

## Versioning & Compatibility

- All endpoints are versioned implicitly through Git tags/images. Breaking changes trigger a roadmap entry and wiki update.
- API responses return `200/201` for success, `404` for missing entities, `409` for duplicates, and `422` for validation errors.
- Pagination is currently basic (managed client-side). Future work adds explicit `limit/offset` parameters to heavy listings.

## Testing Strategy

- `services/backend/tests/test_endpoints` covers every router, including HomeAssistant-specific serialization.
- Contract fidelity is enforced by Pydantic models; add tests when evolving schemas (e.g., new mash step attributes).
- Contract-first development is encouraged: update PlantUML sequence diagrams + this page when altering flows.

## Integrations

| Integration | Endpoints | Description |
| --- | --- | --- |
| **HomeAssistant REST sensors** | `/homeassistant/batches`, `/homeassistant/batches/{id}`, `/homeassistant/summary` | Provides derived fields (`status_icon`, `gravity_delta`, `temperature_alerts`) for dashboards. Example configs live in `homeassistant_config_example.yaml`. |
| **Cloudflare Tunnel** | N/A | Secures 80/443/9501 ingress; configure Zero Trust policies to restrict API exposure. |
| **ISpindel** | Device callback hitting `/batches/{id}/readings` (coming soon) | Today data is entered manually; upcoming release ingests hydrometer pushes over port 9501. |

When exposing new resources, remember to:

1. Add router + schema modules.
2. Extend `api_endpoint_catalog.md` via the generation script.
3. Create/refresh fitting PlantUML diagrams in `documents/docs/plantuml` and re-run `scripts/render_plantuml_diagrams.py`.
