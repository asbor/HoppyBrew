# HoppyBrew API Guide

The HoppyBrew API powers recipe management, batch tracking, ingredient inventories, and style reference tooling for the platform. This guide highlights how to explore the automatically generated documentation and provides practical `curl` examples you can copy into a terminal.

## Getting Started
- Start the backend from `services/backend` with:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
- Open the interactive Swagger UI at `http://localhost:8000/docs` or the raw OpenAPI schema at `http://localhost:8000/openapi.json`.
- All endpoints currently operate without authentication; secure the API before exposing it publicly.

## OpenAPI Metadata
- **Title:** HoppyBrew API
- **Version:** 1.0.0
- **Description:** Brewing-focused CRUD endpoints for recipes, inventory, batches, and reference data.
- **Contact:** support@hoppybrew.io
- **License:** MIT

## Tag Overview
| Tag | Description |
| --- | --- |
| system | Operational status endpoints. |
| recipes | Manage recipe definitions and ingredients. |
| batches | Track active and archived brew batches. |
| hops / fermentables / miscs / yeasts | Inventory and recipe ingredient management. |
| style_guidelines / styles | Reference BJCP guidelines and parsed style records. |
| references | External resource catalogue and BeerXML import/export. |
| health / logs | Observability endpoints for monitoring and support. |
| refresh-beer-styles | Utility endpoints that refresh cached beer style data. |

## Example Requests
The snippets assume the service runs on `localhost:8000`. Adjust hostnames, ports, and IDs for your environment.

### 1. Check API Health
```bash
curl -s http://localhost:8000/ | jq
```
```json
{
  "message": "Welcome to the HoppyBrew API",
  "status": "online"
}
```

### 2. Create a Recipe
```bash
curl -s -X POST http://localhost:8000/recipes \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Citrus IPA",
    "type": "All Grain",
    "batch_size": 20.0,
    "ibu_method": "Tinseth",
    "hops": [{
      "name": "Cascade",
      "origin": "USA",
      "alpha": 5.5,
      "form": "Pellet",
      "use": "Boil",
      "time": 60
    }],
    "fermentables": [{
      "name": "Pilsner Malt",
      "type": "Grain",
      "amount": 4.5,
      "yield_": 80.0,
      "color": 2
    }],
    "miscs": [{
      "name": "Irish Moss",
      "type": "Fining",
      "use": "Boil",
      "amount": 14,
      "time": 10
    }],
    "yeasts": [{
      "name": "SafAle US-05",
      "type": "Ale",
      "form": "Dry",
      "attenuation": 78.0
    }]
  }' | jq '.id, .name, .hops[0].name'
```

### 3. Launch a Batch from a Recipe
```bash
curl -s -X POST http://localhost:8000/batches \
  -H 'Content-Type: application/json' \
  -d '{
    "recipe_id": 42,
    "batch_name": "Citrus IPA - March Run",
    "batch_number": 1,
    "batch_size": 20.0,
    "brewer": "Alex Brewer",
    "brew_date": "2024-03-21T08:00:00Z"
  }' | jq '.id, .inventory_hops[0].name'
```

### 4. Import Reference Data (BeerXML)
```bash
curl -s -X POST http://localhost:8000/references/import \
  -F 'file=@sample-data/references.xml' | jq
```
```json
{
  "message": "References imported successfully",
  "imported_records": 12,
  "skipped_records": 2
}
```

### 5. Trigger Beer Style Refresh
```bash
curl -s -X POST http://localhost:8000/refresh-beer-styles | jq
```
```json
{
  "message": "Beer style refresh queued for processing.",
  "task_id": "refresh-beer-styles-20240321T101500Z"
}
```

## Response Shapes
All structured responses reflect the examples declared in the Pydantic models. Use the `/docs` interface to inspect each schema, example payload, and any nested dependencies.

## Troubleshooting
- **Database errors:** ensure the PostgreSQL instance defined in `services/backend/database.py` is reachable before hitting write endpoints.
- **Missing examples:** refresh the OpenAPI schema in your browser (`Ctrl`/`Cmd` + `F5`) after restarting the backend to see the latest documentation.
- **CORS issues from the frontend:** review the `origins` list in `services/backend/main.py` and add additional hosts as needed.

