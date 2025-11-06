# Frontend API URL Migration Guide

## Problem
Currently, many frontend pages have hard-coded API URLs like `http://localhost:8000/recipes`. This creates issues when:
- Deploying to different environments (dev, staging, production)
- Running in Docker with service networking
- Testing with different backend configurations

## Solution
Use the centralized runtime configuration and new `useApiUrl()` composable.

## Migration Steps

### Before (❌ Don't do this)
```typescript
// Hard-coded URL
const response = await fetch('http://localhost:8000/recipes', {
  method: 'GET',
  headers: { 'Accept': 'application/json' }
})
```

### After (✅ Do this)
```typescript
// Option 1: Using useApiUrl composable
const { url } = useApiUrl()
const response = await fetch(url('/recipes'), {
  method: 'GET',
  headers: { 'Accept': 'application/json' }
})

// Option 2: Using useApi composable (recommended)
const api = useApi()
const { data, loading, error } = await api.get('/recipes')
```

## Affected Files
The following files need to be migrated to use `useApiUrl()` or `useApi()`:

### Batch Pages
- [ ] `pages/batches/newBatch.vue` (2 URLs)
- [ ] `pages/batches/[id].vue` (2 URLs)

### Recipe Pages
- [ ] `pages/recipes/recipeCardWindow.vue` (2 URLs)
- [ ] `pages/recipes/newRecipe.vue` (1 URL)
- [ ] `pages/recipes/[id].vue` (2 URLs)

### Reference Pages
- [ ] `pages/references/index.vue` (2 URLs)
- [ ] `pages/references/newReferences.vue` (1 URL)
- [ ] `pages/references/[id].vue` (2 URLs)

### Inventory Pages
- [ ] `pages/inventory/yeasts/index.vue` (2 URLs)
- [ ] `pages/inventory/yeasts/newYeast.vue` (1 URL)
- [ ] `pages/inventory/yeasts/[id].vue` (2 URLs)
- [ ] Similar patterns in other inventory types (hops, fermentables, miscs)

### Other Pages
- [ ] `pages/log.vue` (1 URL)
- [ ] `pages/ImportXML.vue` (1 URL)

## Example Migration

### Example 1: Simple GET request
```vue
<script setup lang="ts">
// Before
const fetchRecipes = async () => {
  const response = await fetch('http://localhost:8000/recipes')
  recipes.value = await response.json()
}

// After (Option 1: Manual)
const { url } = useApiUrl()
const fetchRecipes = async () => {
  const response = await fetch(url('/recipes'))
  recipes.value = await response.json()
}

// After (Option 2: Using useApi - Recommended)
const api = useApi()
const fetchRecipes = async () => {
  const { data, error } = await api.get('/recipes')
  if (error.value) {
    console.error('Failed to fetch recipes:', error.value)
    return
  }
  recipes.value = data.value
}
</script>
```

### Example 2: POST request
```vue
<script setup lang="ts">
// Before
const createRecipe = async (recipe: Recipe) => {
  const response = await fetch('http://localhost:8000/recipes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(recipe)
  })
  return await response.json()
}

// After (Using useApi - Recommended)
const api = useApi()
const createRecipe = async (recipe: Recipe) => {
  const { data, error } = await api.post('/recipes', recipe)
  if (error.value) {
    console.error('Failed to create recipe:', error.value)
    throw new Error(error.value)
  }
  return data.value
}
</script>
```

### Example 3: Axios migration
```vue
<script setup lang="ts">
import axios from 'axios'

// Before
const updateRecipe = async (id: number, recipe: Recipe) => {
  await axios.put(`http://localhost:8000/recipes/${id}`, recipe)
}

// After (Using useApi - Recommended)
const api = useApi()
const updateRecipe = async (id: number, recipe: Recipe) => {
  const { error } = await api.put(`/recipes/${id}`, recipe)
  if (error.value) {
    console.error('Failed to update recipe:', error.value)
    throw new Error(error.value)
  }
}
</script>
```

## Benefits of Migration

1. **Environment Flexibility**: Single configuration point in `nuxt.config.ts`
2. **Consistent Error Handling**: `useApi()` provides built-in error handling
3. **Loading States**: Automatic loading state management
4. **Type Safety**: Better TypeScript support
5. **Maintainability**: Easier to update API behavior globally
6. **Docker Support**: Works seamlessly with Docker service names

## Configuration

The API URL is configured in `nuxt.config.ts`:

```typescript
runtimeConfig: {
  public: {
    API_URL: process.env.API_BASE_URL || "http://localhost:8000/",
  }
}
```

And can be set via environment variables:
- Development: `.env` file
- Docker: `docker-compose.yml` environment section
- Production: Server environment variables

## Testing

After migration, test each page:
1. In local development (`http://localhost:3000`)
2. With Docker Compose (`docker-compose up`)
3. Verify API calls in browser DevTools Network tab

## Timeline

**Recommended Approach**: Migrate pages incrementally during feature work rather than all at once. This reduces risk and allows for thorough testing.

**Priority Order**:
1. High-traffic pages (recipes, batches)
2. New features being developed
3. Low-traffic pages (logs, imports)

## Related Files
- `composables/useApi.ts` - Core API client
- `composables/useApiUrl.ts` - URL builder helper
- `composables/useRecipes.ts` - Example of proper API usage
- `composables/useBatches.ts` - Example of proper API usage
- `nuxt.config.ts` - Runtime configuration
