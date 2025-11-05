# HoppyBrew Frontend Architecture

## Core Principles

### 1. **Backend-Driven Data (GOLDEN RULE)**
> **NO data in frontend components. ALL data comes from the backend API.**

- Never hardcode recipes, batches, inventory, or reference data
- All CRUD operations go through backend endpoints
- Frontend is a pure presentation layer

### 2. **Brewing Process Workflow**
The application supports the complete homebrewing lifecycle:

```
Recipe Design → Inventory Check → Brew Day → Fermentation → Packaging → Evaluation
```

### 3. **European Standards**
- Currency: EUR (€) not USD ($)
- Units: Metric (liters, grams, °C) with optional imperial display
- Dates: DD/MM/YYYY format
- Beer styles: BJCP 2021 guidelines

### 4. **Self-Hosted Hobbyist Focus**
- No commercial/sales features
- Personal recipe library management
- Small-batch tracking (5-50L typical)
- Inventory for home supplies
- Learning resources and calculators

## Page Structure

### Dashboard (/)
**Purpose:** Overview of current brewing activity and quick actions

**Data Sources (Backend):**
- Active batches (in fermentation)
- Recent recipes
- Low inventory items
- Upcoming brew days

**Key Metrics:**
- Total recipes
- Active batches
- Inventory items count
- Last brew date

**No sales, refunds, or commercial metrics**

### Recipes (/recipes)
**Purpose:** Manage personal recipe library

**Features:**
- Clean list view (name, style, ABV, IBU, efficiency)
- Card view with recipe photos
- Quick search and filter (style, ABV range, last brewed)
- Clone existing recipes
- Import BeerXML
- Calculate recipe statistics

**Detail View (/recipes/:id):**
- Recipe overview
- Ingredients (with inventory availability check)
- Mash schedule
- Hop additions timeline
- Yeast & fermentation
- Notes & brew history
- "Start Batch" button (creates batch from recipe)

### Batches (/batches)
**Purpose:** Track active and completed brews

**Batch Workflow States:**
1. **Planning** - Recipe selected, not started
2. **Brew Day** - Mashing, boiling, chilling
3. **Fermentation** - Primary, secondary, conditioning
4. **Conditioning** - Aging, carbonation
5. **Packaged** - Bottled/kegged, ready
6. **Completed** - All consumed, archived

**List View:**
- Batch name, recipe, brew date, current stage, days in stage
- Status indicators (temperature alerts, gravity readings due)
- Filter by status (active, fermenting, packaged, archived)

**Detail View (/batches/:id):**
- Batch timeline (visual progress through stages)
- Current readings (gravity, temperature, pH)
- Fermentation log (graph of gravity/temp over time)
- Brew day notes
- Tasting notes & ratings
- "Add Reading" quick action
- "Move to Next Stage" workflow button

### Inventory (/inventory)
**Purpose:** Track ingredients and supplies

**Categories:**
- Fermentables (malts, grains, extracts)
- Hops (pellets, leaf, varieties)
- Yeasts (liquid, dry, strains)
- Misc (spices, finings, salts, acids)
- Equipment (optional tracking)

**List View per Category:**
- Name, amount, unit, cost per unit (€), supplier
- Low stock warnings
- Last used date
- Actions: adjust quantity, edit, delete

**Features:**
- "Check Recipe" - verify if enough ingredients for a recipe
- Purchase history (optional)
- Expiration tracking for yeasts

### Brew Day (/batches/:id/brew)
**Purpose:** Interactive guide through brew day

**Steps:**
1. **Pre-Brew Checklist** - equipment ready, ingredients gathered
2. **Mash** - temperature steps, timer, readings
3. **Lauter/Sparge** - volume check, gravity reading
4. **Boil** - hop additions timer, evaporation calc
5. **Chill** - temperature monitoring
6. **Transfer** - final volume, OG reading, pitch yeast
7. **Cleanup** - mark complete

**Features:**
- Step-by-step checklist
- Timers for each stage
- Quick data entry (temperature, gravity, volume)
- Auto-update batch status
- Save notes at each step

### Fermentation Tracking (/batches/:id/fermentation)
**Purpose:** Monitor and log fermentation progress

**Features:**
- Add gravity readings (date, SG, temp, pH, notes)
- Temperature chart over time
- Gravity chart (estimate completion)
- Attenuation calculation
- Alerts (stuck fermentation, temperature out of range)
- "Move to Conditioning" when target FG reached

### Tools (/tools)
**Purpose:** Brewing calculators and utilities

**Calculators:**
- **ABV Calculator** - from OG/FG
- **IBU Calculator** - Tinseth, Rager methods
- **SRM Color** - from grain bill
- **Strike Water** - mash temperature
- **Priming Sugar** - carbonation
- **Dilution** - adjust gravity/volume
- **Yeast Starter** - cell count calculator
- **Water Chemistry** - mineral additions

**No commercial/sales tools**

### Library (/library)
**Purpose:** Browse recipe collections and styles

**Features:**
- Recipe templates by style
- BJCP style guidelines browser
- Clone community recipes (if sharing enabled)
- Recipe collections (IPAs, Stouts, Lagers, etc.)

### Settings (/settings)
**Purpose:** Application configuration

**Sections:**
- **Units** - Metric/Imperial toggle, temperature scale
- **Preferences** - default batch size, efficiency
- **Profile** - brewer name, location
- **Backup** - export/import data
- **About** - version, license

## Component Architecture

### Composables

#### `useApi.ts`
```typescript
// Base API client with error handling
// Returns: { data, loading, error, fetch, create, update, delete }
```

#### `useRecipes.ts`
```typescript
// Recipe CRUD operations
// GET /recipes, POST /recipes, PUT /recipes/:id, DELETE /recipes/:id
```

#### `useBatches.ts`
```typescript
// Batch CRUD and workflow
// GET /batches, POST /batches, PATCH /batches/:id/status
```

#### `useInventory.ts`
```typescript
// Inventory management
// Separate methods for hops, fermentables, yeasts, miscs
```

#### `useCalculators.ts`
```typescript
// Client-side brewing calculations (no backend needed)
// ABV, IBU, SRM, water chemistry, etc.
```

### Reusable Components

- `RecipeCard.vue` - Recipe summary card
- `BatchStatusBadge.vue` - Visual batch stage indicator
- `IngredientList.vue` - Formatted ingredient display
- `GravityChart.vue` - Fermentation progress chart
- `BrewTimer.vue` - Countdown timer for brew steps
- `InventoryBadge.vue` - Stock level indicator
- `MetricDisplay.vue` - EUR currency, metric units formatter

## API Integration Patterns

### Standard CRUD Pattern
```typescript
// Example: Recipes
const { data: recipes, loading, error } = await useRecipes().fetchAll()
const { data: recipe } = await useRecipes().fetchOne(id)
const newRecipe = await useRecipes().create(recipeData)
const updated = await useRecipes().update(id, changes)
await useRecipes().delete(id)
```

### Reactive Data Binding
```vue
<script setup>
const { recipes, loading, refresh } = useRecipes()

// Auto-refresh after create
async function createRecipe(data) {
  await useRecipes().create(data)
  await refresh()
}
</script>
```

## State Management

**No Pinia/Vuex needed initially** - use composables with reactive refs

For later (if needed):
- Shared state: active batch, current user, app settings
- Persistence: LocalStorage for preferences only
- Cache: SWR pattern in composables

## Styling Guidelines

- **Shadcn UI components** for consistency
- **Tailwind utility classes** for layout
- **Responsive first** - mobile to desktop
- **Dark mode support** (optional)
- **Brewing-specific colors:**
  - Fermentation: Blue tones
  - Brew Day: Amber/orange
  - Completed: Green
  - Alerts: Red/yellow

## Data Flow

```
User Action → Component Event → Composable API Call → Backend Endpoint
                                        ↓
                                   Update Local Ref
                                        ↓
                                 Component Re-renders
```

**Never:**
- ❌ Hardcode data in components
- ❌ Store business logic in components
- ❌ Make fetch calls directly in components
- ❌ Use commercial/sales terminology
- ❌ Use USD currency

**Always:**
- ✅ Use composables for data access
- ✅ Display loading states
- ✅ Handle errors gracefully
- ✅ Use EUR (€) for currency
- ✅ Support metric units primarily
- ✅ Focus on homebrewing workflow

## Mobile Responsiveness

- Sidebar collapses to hamburger menu on mobile
- Tables become cards on small screens
- Multi-column forms stack vertically
- Touch-friendly button sizes (min 44px)
- Swipe gestures for batch workflows

## Progressive Enhancement

### Phase 1 (MVP - Current):
- Recipe CRUD
- Batch tracking (basic)
- Inventory management
- Simple calculators

### Phase 2:
- Fermentation charts
- Brew day guide
- Recipe scaling
- BeerXML import/export

### Phase 3:
- Photo uploads (recipe/batch)
- Multi-user (family/club)
- Recipe sharing (optional)
- IoT sensor integration (Tilt, iSpindel)

## Testing Strategy

- **Unit tests:** Composables, calculators
- **Component tests:** UI interactions
- **E2E tests:** Complete brewing workflow
- **API mocking:** MSW for development

## Performance Targets

- Initial page load: < 2s
- API response time: < 500ms
- Recipe list (100 items): < 100ms render
- Batch detail page: < 1s with charts
- Mobile performance: Lighthouse score > 90

## Accessibility

- Semantic HTML
- ARIA labels for complex components
- Keyboard navigation
- Screen reader friendly
- Color contrast WCAG AA

---

## Implementation Priority

1. **Create composables** for API integration
2. **Rebuild Dashboard** - homebrewing metrics
3. **Rebuild Recipe pages** - clean, focused view
4. **Rebuild Batch pages** - workflow stages
5. **Rebuild Inventory** - stock management
6. **Add Tools page** - calculators
7. **Add Brew Day workflow** - interactive guide
8. **Add Fermentation tracking** - charts & logs
9. **Mobile optimization**
10. **Dark mode & polish**
