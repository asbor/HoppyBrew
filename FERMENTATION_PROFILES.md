# Fermentation Profile Management System

## Overview

The Fermentation Profile Management System allows brewers to create, manage, and apply temperature schedules and fermentation stages for different beer styles. This system supports both standard and pressurized fermentation profiles with multiple configurable steps.

## Features

### Profile Management
- **Create Profiles**: Define custom fermentation profiles with multiple steps
- **Template Profiles**: Pre-configured profiles for Ale, Lager, and NEIPA styles
- **Pressurized Fermentation**: Support for pressure settings in each step
- **Profile Metadata**: Name, description, and template flags

### Fermentation Steps
- **Step Configuration**: Configure each step with:
  - Step name and type (primary, secondary, conditioning, cold crash, diacetyl rest, lagering)
  - Temperature settings (°C)
  - Duration (days)
  - Ramp time for gradual temperature changes (days)
  - Pressure settings for pressurized fermentation (PSI)
  - Notes for each step
- **Step Ordering**: Automatic step ordering and reordering support
- **Step Management**: Add, update, and delete individual steps

## Database Schema

### fermentation_profiles Table
```sql
CREATE TABLE fermentation_profiles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_pressurized BOOLEAN DEFAULT false,
    is_template BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### fermentation_steps Table
```sql
CREATE TABLE fermentation_steps (
    id SERIAL PRIMARY KEY,
    fermentation_profile_id INTEGER REFERENCES fermentation_profiles(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    name VARCHAR(255),
    step_type VARCHAR(50) DEFAULT 'primary',
    temperature DECIMAL(5,2),
    duration_days INTEGER,
    ramp_days INTEGER DEFAULT 0,
    pressure_psi DECIMAL(5,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Fermentation Profiles

#### List All Profiles
```
GET /fermentation-profiles
```
Returns all fermentation profiles with their steps.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Standard Ale",
    "description": "Basic ale fermentation profile",
    "is_pressurized": false,
    "is_template": true,
    "created_at": "2025-11-06T10:00:00",
    "updated_at": "2025-11-06T10:00:00",
    "steps": [...]
  }
]
```

#### Get Specific Profile
```
GET /fermentation-profiles/{id}
```
Returns a specific profile with all its steps.

#### Create Profile
```
POST /fermentation-profiles
```

**Request Body:**
```json
{
  "name": "My Custom Ale",
  "description": "Custom fermentation profile",
  "is_pressurized": false,
  "is_template": false,
  "steps": [
    {
      "step_order": 1,
      "name": "Primary Fermentation",
      "step_type": "primary",
      "temperature": 20,
      "duration_days": 7,
      "ramp_days": 0,
      "notes": "Primary fermentation phase"
    }
  ]
}
```

#### Update Profile
```
PUT /fermentation-profiles/{id}
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "is_pressurized": true
}
```

#### Delete Profile
```
DELETE /fermentation-profiles/{id}
```
Deletes the profile and all associated steps (cascade).

### Fermentation Steps

#### Get Steps for Profile
```
GET /fermentation-profiles/{profile_id}/steps
```

#### Add Step to Profile
```
POST /fermentation-profiles/{profile_id}/steps
```

**Request Body:**
```json
{
  "step_order": 1,
  "name": "Primary Fermentation",
  "step_type": "primary",
  "temperature": 20,
  "duration_days": 7,
  "ramp_days": 0
}
```

#### Update Step
```
PUT /fermentation-steps/{step_id}
```

**Request Body:**
```json
{
  "temperature": 22,
  "duration_days": 10
}
```

#### Delete Step
```
DELETE /fermentation-steps/{step_id}
```

## Frontend Pages

### Profile List Page
**Route:** `/profiles/fermentation`

Displays all fermentation profiles in a table with:
- Profile name and description
- Template indicator
- Fermentation type (standard/pressurized)
- Number of steps
- Total fermentation days
- Edit and delete actions

### Create Profile Page
**Route:** `/profiles/fermentation/new`

Allows creating new profiles with:
- Template selection (Ale, Lager, NEIPA)
- Profile details form
- Step management interface
- Real-time total days calculation

### Edit Profile Page
**Route:** `/profiles/fermentation/{id}`

Allows editing existing profiles with:
- Profile details editing
- Step management with auto-save
- Add/remove/reorder steps
- Pressurized fermentation toggle

## Template Profiles

### Standard Ale
- **Duration:** 14 days total
- **Steps:**
  1. Primary Fermentation: 20°C for 7 days
  2. Conditioning: 18°C for 7 days (1 day ramp)

### Lager
- **Duration:** 44 days total
- **Steps:**
  1. Primary Fermentation: 10°C for 14 days
  2. Diacetyl Rest: 18°C for 2 days (1 day ramp)
  3. Lagering: 2°C for 28 days (2 day ramp)

### NEIPA
- **Duration:** 9 days total
- **Steps:**
  1. Primary Fermentation: 19°C for 4 days
  2. Dry Hop Conditioning: 21°C for 3 days
  3. Cold Crash: 4°C for 2 days (1 day ramp)

## Step Types

The system supports the following step types:
- `primary` - Primary Fermentation
- `secondary` - Secondary Fermentation
- `conditioning` - Conditioning
- `cold_crash` - Cold Crash
- `diacetyl_rest` - Diacetyl Rest
- `lagering` - Lagering

## Usage Examples

### Creating a Custom Profile via API

```python
import requests

profile_data = {
    "name": "My Custom Profile",
    "description": "A custom fermentation schedule",
    "is_pressurized": False,
    "is_template": False,
    "steps": [
        {
            "step_order": 1,
            "name": "Primary",
            "step_type": "primary",
            "temperature": 20,
            "duration_days": 7,
            "ramp_days": 0
        }
    ]
}

response = requests.post(
    "http://localhost:8000/fermentation-profiles",
    json=profile_data
)
print(response.json())
```

### Using the Frontend Composable

```typescript
import { useFermentationProfiles } from '@/composables/useFermentationProfiles'

const { getAllProfiles, createProfile } = useFermentationProfiles()

// Fetch all profiles
const { data, loading, error } = await getAllProfiles()

// Create a new profile
const newProfile = {
  name: "Custom Ale",
  description: "My custom ale fermentation",
  is_pressurized: false,
  is_template: false,
  steps: [...]
}

await createProfile(newProfile)
```

## Testing

The system includes comprehensive test coverage:
- **Backend Tests:** 13 tests covering all endpoints
- **Test Coverage:** Profile CRUD, step management, cascade deletes
- **Test Location:** `services/backend/tests/test_endpoints/test_fermentation_profiles.py`

Run tests:
```bash
cd services/backend
python -m pytest tests/test_endpoints/test_fermentation_profiles.py -v
```

## Seeding Data

Seed the database with template profiles:
```bash
cd services/backend
python ../seeds/seed_fermentation_profiles.py
```

Or run the master seed script:
```bash
python seeds/seed_all.py
```

## Integration Points

The fermentation profile system is designed to integrate with:
- **Recipe Management:** Associate profiles with recipes
- **Batch Management:** Apply profiles to active batches
- **Temperature Monitoring:** Track actual vs. planned temperatures
- **Notification System:** Alerts for step transitions
- **Equipment Control:** Automated temperature control

## Future Enhancements

Potential future improvements:
- Visual temperature/time charts
- Automatic step progression tracking
- Temperature deviation alerts
- Import/export functionality
- Mobile-optimized interface
- Batch history and statistics
- Multi-unit support (°F conversion)

## Dependencies

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- Python 3.11+

### Frontend
- Nuxt 3
- Vue 3
- TypeScript
- Shadcn-vue UI components

## File Locations

### Backend
- **Models:** `services/backend/Database/Models/Profiles/fermentation_profiles.py`
- **Schemas:** `services/backend/Database/Schemas/fermentation_profiles.py`
- **Endpoints:** `services/backend/api/endpoints/fermentation_profiles.py`
- **Tests:** `services/backend/tests/test_endpoints/test_fermentation_profiles.py`

### Frontend
- **Composable:** `services/nuxt3-shadcn/composables/useFermentationProfiles.ts`
- **List Page:** `services/nuxt3-shadcn/pages/profiles/fermentation/index.vue`
- **Create Page:** `services/nuxt3-shadcn/pages/profiles/fermentation/new.vue`
- **Edit Page:** `services/nuxt3-shadcn/pages/profiles/fermentation/[id].vue`

### Seeds
- **Seed Script:** `seeds/seed_fermentation_profiles.py`
- **Master Seed:** `seeds/seed_all.py` (includes fermentation profiles)
