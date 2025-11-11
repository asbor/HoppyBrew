# API Documentation

Complete reference for the HoppyBrew REST API.

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [API Explorer](#api-explorer)
- [Common Patterns](#common-patterns)
- [Error Handling](#error-handling)
- [Endpoints by Domain](#endpoints-by-domain)
- [Examples](#examples)
- [Integration Guides](#integration-guides)

---

## Overview

HoppyBrew exposes a comprehensive REST API built with FastAPI. The API provides programmatic access to all brewing management features including recipes, batches, inventory, and external integrations.

**Key Features:**
- 🔍 **OpenAPI/Swagger Documentation**: Interactive API explorer at `/docs`
- ✅ **Type-Safe**: Pydantic models ensure data validation
- 📊 **Well-Organized**: Endpoints grouped by logical domains
- 🏠 **HomeAssistant Integration**: Dedicated endpoints for smart home monitoring
- 🧮 **Brewing Calculators**: Helper endpoints for common brewing calculations

---

## Base URL

**Local Development:**
```
http://localhost:8000
```

**Docker Deployment:**
```
http://your-host:8000
```

**Production (with Cloudflare Tunnel):**
```
https://your-domain.com
```

---

## Authentication

**Current Status:** The API is currently **open** (no authentication required).

⚠️ **Security Note:** For production deployments:
- Place behind VPN or Cloudflare Access policies
- Restrict network access to trusted sources
- Future versions will include JWT authentication

**Planned Authentication:**
```http
Authorization: Bearer <jwt-token>
```

See [ROADMAP.md](ROADMAP.md) for authentication implementation timeline.

---

## API Explorer

HoppyBrew includes an interactive API documentation interface powered by Swagger UI.

**Access the API Explorer:**
```
http://localhost:8000/docs
```

**Features:**
- ✅ Try endpoints directly from your browser
- ✅ View request/response schemas
- ✅ See example payloads
- ✅ Generate code snippets

**Alternative Documentation (ReDoc):**
```
http://localhost:8000/redoc
```

---

## Common Patterns

### Request Format

All requests use JSON with UTF-8 encoding:

```http
POST /recipes HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "Pale Ale",
  "batch_size_l": 20,
  "efficiency": 72
}
```

### Response Format

Successful responses return JSON with appropriate HTTP status codes:

```json
{
  "id": "uuid-here",
  "name": "Pale Ale",
  "batch_size_l": 20.0,
  "efficiency": 72.0,
  "created_at": "2025-01-01T12:00:00Z"
}
```

### Pagination

For list endpoints, pagination is handled client-side. Future versions will add:
```
GET /recipes?page=1&per_page=20
```

### Filtering

Many endpoints support query parameters for filtering:
```
GET /hops?alpha_acid_min=10&usage=boil
GET /recipes?style=IPA
GET /batches?status=fermenting
```

---

## Error Handling

The API uses standard HTTP status codes and returns detailed error messages.

### Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created successfully |
| `204` | No Content | Request successful, no body returned |
| `400` | Bad Request | Invalid request data |
| `404` | Not Found | Resource not found |
| `409` | Conflict | Duplicate resource or business rule violation |
| `422` | Unprocessable Entity | Validation error (Pydantic) |
| `500` | Internal Server Error | Server-side error |

### Error Response Format

```json
{
  "detail": "Resource not found"
}
```

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "batch_size_l"],
      "msg": "value must be greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Endpoints by Domain

### System & Health

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service heartbeat |
| `/health` | GET | Health check for monitoring |

### Recipes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recipes` | GET | List all recipes |
| `/recipes/{id}` | GET | Get recipe details |
| `/recipes` | POST | Create new recipe |
| `/recipes/{id}` | PUT | Update recipe |
| `/recipes/{id}` | DELETE | Delete recipe |
| `/recipes/{id}/clone` | POST | Clone existing recipe |

**Recipe Schema:**
```typescript
{
  id: string;
  name: string;
  style_id?: string;
  batch_size_l: number;
  efficiency: number;
  og?: number;  // Original gravity
  fg?: number;  // Final gravity
  abv?: number; // Alcohol by volume
  ibu?: number; // International bitterness units
  srm?: number; // Color (Standard Reference Method)
  hops: Hop[];
  fermentables: Fermentable[];
  yeasts: Yeast[];
  miscs?: Misc[];
}
```

### Batches

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/batches` | GET | List all batches |
| `/batches/{id}` | GET | Get batch details |
| `/batches` | POST | Create new batch |
| `/batches/{id}` | PUT | Update batch |
| `/batches/{id}` | DELETE | Delete batch |
| `/batches/{id}/readings` | POST | Add fermentation reading |

**Batch Lifecycle:**
```
planning → brew_day → fermenting → conditioning → packaged → archived
```

### Ingredients

#### Hops
```
GET    /hops              List all hops
GET    /hops/{id}         Get hop details
POST   /hops              Add new hop
PUT    /hops/{id}         Update hop
DELETE /hops/{id}         Delete hop
```

#### Fermentables
```
GET    /fermentables      List all fermentables
GET    /fermentables/{id} Get fermentable details
POST   /fermentables      Add new fermentable
PUT    /fermentables/{id} Update fermentable
DELETE /fermentables/{id} Delete fermentable
```

#### Yeasts
```
GET    /yeasts            List all yeasts
GET    /yeasts/{id}       Get yeast details
POST   /yeasts            Add new yeast
PUT    /yeasts/{id}       Update yeast
DELETE /yeasts/{id}       Delete yeast
```

#### Miscellaneous
```
GET    /miscs             List all misc ingredients
GET    /miscs/{id}        Get misc details
POST   /miscs             Add new misc
PUT    /miscs/{id}        Update misc
DELETE /miscs/{id}        Delete misc
```

### Profiles

#### Equipment Profiles
```
GET    /equipment-profiles      List equipment profiles
GET    /equipment-profiles/{id} Get profile details
POST   /equipment-profiles      Create profile
PUT    /equipment-profiles/{id} Update profile
DELETE /equipment-profiles/{id} Delete profile
```

#### Mash Profiles
```
GET    /mash-profiles      List mash profiles
GET    /mash-profiles/{id} Get profile details
POST   /mash-profiles      Create profile
PUT    /mash-profiles/{id} Update profile
DELETE /mash-profiles/{id} Delete profile
```

#### Water Profiles
```
GET    /water-profiles      List water profiles
GET    /water-profiles/{id} Get profile details
POST   /water-profiles      Create profile
PUT    /water-profiles/{id} Update profile
DELETE /water-profiles/{id} Delete profile
```

#### Fermentation Profiles
```
GET    /fermentation-profiles      List profiles
GET    /fermentation-profiles/{id} Get profile details
POST   /fermentation-profiles      Create profile
PUT    /fermentation-profiles/{id} Update profile
DELETE /fermentation-profiles/{id} Delete profile
```

### Beer Styles

```
GET /beer-styles                    List all styles
GET /beer-styles/{id}               Get style details
GET /style-categories               List style categories
GET /style-guideline-sources        List style sources (BJCP)
POST /refresh-beer-styles           Trigger style database refresh
```

### Calculators

```
POST /calculators/strike-water      Calculate strike water temperature
POST /calculators/abv               Calculate alcohol by volume
POST /calculators/priming-sugar     Calculate priming sugar amounts
POST /calculators/yeast-starter     Calculate yeast starter size
POST /calculators/dilution          Calculate dilution for target gravity
```

### HomeAssistant Integration

```
GET /homeassistant/batches          List batches for HA sensors
GET /homeassistant/batches/{id}     Get batch sensor data
GET /homeassistant/summary          Get brewery summary
```

**HomeAssistant Response Format:**
```json
{
  "batch_id": "uuid",
  "batch_name": "Pale Ale #3",
  "status": "fermenting",
  "status_icon": "mdi:fermentation",
  "days_in_fermenter": 5,
  "current_gravity": 1.015,
  "target_gravity": 1.012,
  "gravity_delta": 0.003,
  "temperature_c": 19.5,
  "temperature_alerts": []
}
```

### Devices

```
GET    /devices           List connected devices
GET    /devices/{id}      Get device details
POST   /devices           Register new device
PUT    /devices/{id}      Update device
DELETE /devices/{id}      Remove device
```

### Logs

```
GET /logs?limit=100        Get recent log entries
```

---

## Examples

### Creating a Recipe

```bash
curl -X POST http://localhost:8000/recipes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Citra Pale Ale",
    "style_id": "18B",
    "batch_size_l": 20,
    "efficiency": 72,
    "fermentables": [
      {
        "fermentable_id": "pale-malt-2-row",
        "amount_kg": 4.5,
        "lovibond": 2
      },
      {
        "fermentable_id": "caramel-20",
        "amount_kg": 0.5,
        "lovibond": 20
      }
    ],
    "hops": [
      {
        "hop_id": "citra",
        "amount_g": 25,
        "alpha_acid": 12.5,
        "time_min": 60,
        "usage": "boil"
      },
      {
        "hop_id": "citra",
        "amount_g": 50,
        "alpha_acid": 12.5,
        "time_min": 0,
        "usage": "whirlpool"
      }
    ],
    "yeasts": [
      {
        "yeast_id": "us-05",
        "attenuation": 77,
        "temperature_min": 15,
        "temperature_max": 22
      }
    ]
  }'
```

### Starting a Batch

```bash
curl -X POST http://localhost:8000/batches \
  -H "Content-Type: application/json" \
  -d '{
    "recipe_id": "recipe-uuid-here",
    "batch_number": "2025-001",
    "brew_date": "2025-01-15",
    "status": "planning"
  }'
```

### Recording Fermentation Reading

```bash
curl -X POST http://localhost:8000/batches/{batch_id}/readings \
  -H "Content-Type: application/json" \
  -d '{
    "gravity": 1.015,
    "temperature_c": 19.5,
    "ph": 4.2,
    "notes": "Fermentation progressing well"
  }'
```

### Calculating ABV

```bash
curl -X POST http://localhost:8000/calculators/abv \
  -H "Content-Type: application/json" \
  -d '{
    "og": 1.052,
    "fg": 1.012
  }'
```

**Response:**
```json
{
  "abv": 5.25,
  "attenuation": 76.92
}
```

---

## Integration Guides

### HomeAssistant REST Sensors

Add these sensors to your `configuration.yaml`:

```yaml
sensor:
  # Brewery Summary
  - platform: rest
    name: "Brewery Summary"
    resource: http://your-hoppybrew-host:8000/homeassistant/summary
    value_template: "{{ value_json.active_batches }}"
    json_attributes:
      - total_recipes
      - batches_fermenting
      - batches_conditioning
      - inventory_items
    
  # Active Batch Monitoring
  - platform: rest
    name: "Current Batch"
    resource: http://your-hoppybrew-host:8000/homeassistant/batches/{batch_id}
    value_template: "{{ value_json.status }}"
    json_attributes:
      - batch_name
      - days_in_fermenter
      - current_gravity
      - target_gravity
      - temperature_c
    scan_interval: 300  # Update every 5 minutes
```

### Python Client Example

```python
import requests

class HoppyBrewClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def get_recipes(self):
        response = requests.get(f"{self.base_url}/recipes")
        response.raise_for_status()
        return response.json()
        
    def create_batch(self, recipe_id, batch_data):
        response = requests.post(
            f"{self.base_url}/batches",
            json={"recipe_id": recipe_id, **batch_data}
        )
        response.raise_for_status()
        return response.json()
        
# Usage
client = HoppyBrewClient()
recipes = client.get_recipes()
print(f"Found {len(recipes)} recipes")
```

### JavaScript/TypeScript Client

```typescript
class HoppyBrewAPI {
  constructor(private baseURL = 'http://localhost:8000') {}
  
  async getRecipes() {
    const response = await fetch(`${this.baseURL}/recipes`);
    if (!response.ok) throw new Error('Failed to fetch recipes');
    return response.json();
  }
  
  async createBatch(recipeId: string, batchData: any) {
    const response = await fetch(`${this.baseURL}/batches`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipe_id: recipeId, ...batchData })
    });
    if (!response.ok) throw new Error('Failed to create batch');
    return response.json();
  }
}

// Usage
const api = new HoppyBrewAPI();
const recipes = await api.getRecipes();
console.log(`Found ${recipes.length} recipes`);
```

---

## Rate Limiting

**Current Status:** No rate limiting implemented.

**Planned:** Rate limiting will be added in future versions for public deployments.

---

## Versioning

**Current Version:** 1.0.0

The API version is included in the `/` endpoint response:

```json
{
  "message": "Welcome to the HoppyBrew API",
  "status": "online",
  "version": "1.0.0"
}
```

**Versioning Strategy:**
- Breaking changes will be communicated via CHANGELOG
- Major version increments for breaking API changes
- Backwards compatibility maintained within major versions

---

## Additional Resources

- 📚 [Interactive API Docs](http://localhost:8000/docs) - Try endpoints in your browser
- 📖 [Wiki](wiki/Home.md) - Architecture and guides
- 🏠 [HomeAssistant Config Example](homeassistant_config_example.yaml)
- 🐛 [Report API Issues](https://github.com/asbor/HoppyBrew/issues)
- 💬 [Discussions](https://github.com/asbor/HoppyBrew/discussions)

---

## Support

Having trouble with the API?

1. Check the [interactive documentation](http://localhost:8000/docs)
2. Review [common issues](wiki/Development-Guide.md#troubleshooting)
3. Search [existing issues](https://github.com/asbor/HoppyBrew/issues)
4. Open a [new issue](https://github.com/asbor/HoppyBrew/issues/new)

---

**Last Updated:** 2025-01-15  
**API Version:** 1.0.0
