# Frontend Component Guide

The Nuxt 3 + shadcn-vue app (located in `services/nuxt3-shadcn`) is a thin presentation layer. Business rules live in the backend; the UI simply orchestrates workflows.

## Guard Rails

1. **Backend-driven data** – Components never hardcode inventory, recipes, or reference values. Use composables (`useRecipes`, `useBatches`, `useInventory`, `useProfiles`, `useCalculators`) exclusively.
2. **Metric-first UI** – Display SI units (liters, grams, °C) with optional imperial toggles. Currency defaults to EUR.
3. **Homebrewer focus** – No commercial/point-of-sale widgets. Dashboards highlight brew health, not revenue.
4. **Mobile-first** – Tables collapse into cards, nav bar shrinks to a drawer, and timers/badges meet the 44 px touch target.

## Project Layout

| Path | Description |
| --- | --- |
| `app.vue`, `layouts/` | Shell chrome, sidebar, and responsive layout primitives |
| `components/` | Presentational blocks (RecipeCard, BatchStatusBadge, IngredientList, BrewTimer, GravityChart, MetricDisplay) |
| `composables/` | API-focused hooks returning `{ data, loading, error, create, update, remove }` |
| `pages/` | Route-driven views (Dashboard, Recipes, Batches, Inventory, Tools, Settings) |
| `plugins/` | Axios client, dayjs filters, i18n stubs |
| `assets/` | Tailwind tokens, color system, dark-mode overrides |
| `tests/` | Vitest + Playwright specs covering workflows end-to-end |

## Data Access Patterns

```ts
// Example: using composables inside a page
const { recipes, fetchAll, create } = useRecipes()
onMounted(fetchAll)

async function duplicateRecipe(recipeId: string) {
  const draft = await useRecipes().fetchOne(recipeId)
  draft.name += ' (Copy)'
  await create(draft)
  await fetchAll()
}
```

- Centralize HTTP concerns (error normalization, retry, toast hooks) in `lib/api.ts` or the shared `useApi` composable.
- Keep derived state local—e.g., `const showBrewDayCTA = computed(() => batch.status === 'BREW_DAY')` inside components.
- Use [HomeAssistant integration docs](documents/features/HOMEASSISTANT_INTEGRATION.md) when exposing toggles or dashboards tied to sensors.

## UI Patterns by Surface

| Route | Highlights |
| --- | --- |
| `/` Dashboard | Cards for total recipes, active batches, low inventory, and fermenter timeline. Embed `GravityChart` + `BatchStatusBadge`. |
| `/recipes` | List + card views, filters (style, ABV range, last brewed), clone button, import BeerXML. Detail view shows ingredients, mash schedule, hop timeline, fermentation profile, and action to start batch. |
| `/batches` | Kanban by state (Planning → Brew Day → Fermentation → Conditioning → Packaged → Completed). Each card shows stage timers, fermentation logs, and direct links to record gravity readings. |
| `/inventory` | Tabs for fermentables/hops/yeast/misc. Provide low-stock badges, unit conversions, and quick adjust modals. |
| `/tools` | Calculators (ABV, IBU, SRM, strike water, priming sugar, dilution, yeast starter, water chemistry). Keep formulas in `lib/calculators.ts`. |

## Testing & Quality Gates

- **Unit tests** – composables and utility libs (`vitest`).
- **Component tests** – mount recipe/batch cards with mocked composables.
- **E2E** – Playwright specs cover “design recipe → schedule batch → record fermentation → mark packaged”. Launch with `yarn test:e2e`.
- **Linting** – `yarn lint` (ESLint + stylelint). Tailwind class sorting enforced via configured plugin.
- **Accessibility** – Run `npx @axe-core/playwright` during CI to keep contrast, ARIA, and tab order compliant.

## Working Agreement

1. Update `FRONTEND_ARCHITECTURE.md` when altering layout strategy, navigation, or design system foundations.
2. Add PlantUML diagrams when building new flows (e.g., Brew Day wizard) so backend/frontend teams share the same mental model.
3. Keep environment-specific configuration in `.env` files consumed by Nuxt runtime config (`API_BASE_URL`, measurement preferences, feature flags).
4. Coordinate schema changes with backend owners; composables should not fork contract logic.
