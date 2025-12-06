# API Integration Best Practices

## Overview

This document outlines best practices for making API calls in the HoppyBrew frontend. Following these practices will prevent connectivity issues and make the application more maintainable.

## Core Principles

### 1. Never Hardcode API URLs

❌ **Never do this:**
```typescript
// Hardcoded URL - breaks in Docker, production, etc.
const response = await fetch('http://localhost:8000/recipes')
```

✅ **Always do this:**
```typescript
// Use the configuration utility
const { buildUrl } = useApiConfig()
const response = await fetch(buildUrl('/recipes'))
```

### 2. Use the Right Tool for the Job

We provide three composables for API interactions:

#### `useApiConfig()` - For Building URLs

Use when you need fine control over fetch options or need just the URL:

```typescript
const { buildUrl, apiBaseUrl } = useApiConfig()

// Simple fetch
const response = await fetch(buildUrl('/recipes'))

// Custom fetch with options
const response = await fetch(buildUrl('/recipes'), {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(recipe)
})
```

#### `useApi()` - For Standard CRUD Operations

Use for standard GET/POST/PUT/DELETE operations with built-in error handling:

```typescript
const api = useApi()

// GET request
const { data, loading, error } = await api.get('/recipes')

// POST request
const { data, loading, error } = await api.post('/recipes', newRecipe)

// PUT request
const { data, loading, error } = await api.put('/recipes/123', updatedRecipe)

// DELETE request
const { data, loading, error } = await api.delete('/recipes/123')
```

#### Domain-Specific Composables

Use for entity-specific operations with additional business logic:

```typescript
// For recipes
const { recipes, loading, error, fetchAll, create, update, remove } = useRecipes()

// For batches
const { batches, currentBatch, fetchAll, fetchOne, updateStatus } = useBatches()

// For inventory
const { items, fetchAll, addItem, updateItem } = useInventory()
```

## Migration Guide

### Migrating from Hardcoded URLs

If you find hardcoded URLs in your code, follow this process:

#### Example 1: Simple Fetch

**Before:**
```typescript
async function fetchRecipes() {
  const response = await fetch('http://localhost:8000/recipes')
  const data = await response.json()
  return data
}
```

**After:**
```typescript
async function fetchRecipes() {
  const { buildUrl } = useApiConfig()
  const response = await fetch(buildUrl('/recipes'))
  const data = await response.json()
  return data
}
```

**Even Better:**
```typescript
async function fetchRecipes() {
  const api = useApi()
  const { data, error } = await api.get('/recipes')
  if (error.value) {
    console.error('Failed to fetch recipes:', error.value)
    return null
  }
  return data.value
}
```

#### Example 2: POST Request

**Before:**
```typescript
const response = await fetch('http://localhost:8000/batches', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(batch)
})
```

**After:**
```typescript
const { buildUrl } = useApiConfig()
const response = await fetch(buildUrl('/batches'), {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(batch)
})
```

**Even Better:**
```typescript
const api = useApi()
const { data, error } = await api.post('/batches', batch)
```

#### Example 3: Using Axios

**Before:**
```typescript
import axios from 'axios'

await axios.post('http://localhost:8000/references', reference)
```

**After:**
```typescript
import axios from 'axios'

const { buildUrl } = useApiConfig()
await axios.post(buildUrl('/references'), reference)
```

**Even Better (switch to fetch):**
```typescript
const api = useApi()
const { data, error } = await api.post('/references', reference)
```

## Component Patterns

### Pattern 1: Simple Data Fetching

```vue
<script setup lang="ts">
const { data: recipes, loading, error } = await useApi().get('/recipes')
</script>

<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <div v-for="recipe in recipes" :key="recipe.id">
        {{ recipe.name }}
      </div>
    </div>
  </div>
</template>
```

### Pattern 2: CRUD Operations

```vue
<script setup lang="ts">
import { ref } from 'vue'

const { recipes, loading, error, fetchAll, create, remove } = useRecipes()

// Load data on mount
onMounted(async () => {
  await fetchAll()
})

// Create new recipe
const newRecipe = ref({ name: '', style: '' })
const createRecipe = async () => {
  await create(newRecipe.value)
  await fetchAll() // Refresh list
}

// Delete recipe
const deleteRecipe = async (id: number) => {
  await remove(id)
  await fetchAll() // Refresh list
}
</script>

<template>
  <!-- Your template here -->
</template>
```

### Pattern 3: Form Submission

```vue
<script setup lang="ts">
import { ref } from 'vue'

const formData = ref({ name: '', description: '' })
const submitting = ref(false)
const submitError = ref<string | null>(null)

const handleSubmit = async () => {
  submitting.value = true
  submitError.value = null
  
  try {
    const api = useApi()
    const { data, error } = await api.post('/recipes', formData.value)
    
    if (error.value) {
      submitError.value = error.value
      return
    }
    
    // Success! Redirect or show message
    console.log('Recipe created:', data.value)
    // navigateTo('/recipes')
  } finally {
    submitting.value = false
  }
}
</script>
```

### Pattern 4: Real-time Updates

```vue
<script setup lang="ts">
const route = useRoute()
const batchId = computed(() => route.params.id)

const { currentBatch, loading, error, fetchOne, updateStatus } = useBatches()

// Fetch initial data
onMounted(async () => {
  await fetchOne(batchId.value)
})

// Update batch status
const changeStatus = async (newStatus: string) => {
  await updateStatus(batchId.value, newStatus)
  await fetchOne(batchId.value) // Refresh to get updated data
}
</script>
```

## Error Handling

### Always Handle Errors

```typescript
const api = useApi()
const { data, error } = await api.get('/recipes')

if (error.value) {
  // Log for debugging
  console.error('Failed to fetch recipes:', error.value)
  
  // Show user-friendly message
  toast.error('Failed to load recipes. Please try again.')
  
  // Or set local state
  errorMessage.value = 'Failed to load recipes'
}
```

### Network Error Detection

```typescript
const { checkHealth } = useApiConfig()

const isHealthy = await checkHealth()
if (!isHealthy) {
  console.error('Backend is not responding')
  toast.error('Cannot connect to server. Please check your connection.')
}
```

## Testing Your Changes

### Local Testing (Outside Docker)

1. Ensure backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check frontend configuration:
   ```javascript
   // In browser console
   const { logConfig } = useApiConfig()
   logConfig()
   ```

3. Test API calls in browser console:
   ```javascript
   const { buildUrl } = useApiConfig()
   console.log(buildUrl('/recipes'))
   // Should output: http://localhost:8000/recipes
   
   // Test actual request
   const response = await fetch(buildUrl('/recipes'))
   console.log(await response.json())
   ```

### Docker Testing

1. Start services:
   ```bash
   docker-compose up -d
   ```

2. Check container logs:
   ```bash
   docker logs hoppybrew-frontend-1 -f
   docker logs hoppybrew-backend-1 -f
   ```

3. Test from browser (same as local testing)

4. Test container-to-container:
   ```bash
   docker exec hoppybrew-frontend-1 curl http://hoppybrew-backend-1:8000/health
   ```

## Debugging Checklist

When experiencing API connectivity issues:

- [ ] Check backend is running: `curl http://localhost:8000/health`
- [ ] Check browser console for errors (F12)
- [ ] Check Network tab for failed requests
- [ ] Verify API URL configuration: `useApiConfig().logConfig()`
- [ ] Look for hardcoded `http://localhost:8000` in your code
- [ ] Check CORS errors in console
- [ ] Verify environment variables are set correctly
- [ ] Test with curl or Postman first
- [ ] Check backend logs for errors

See [DEBUGGING_GUIDE.md](./DEBUGGING_GUIDE.md) for detailed troubleshooting steps.

## Common Mistakes to Avoid

### 1. Using Different URL Patterns

❌ **Don't mix patterns:**
```typescript
// Some components use localhost
const response1 = await fetch('http://localhost:8000/recipes')

// Others use config
const { buildUrl } = useApiConfig()
const response2 = await fetch(buildUrl('/batches'))
```

✅ **Be consistent:**
```typescript
// Always use config
const { buildUrl } = useApiConfig()
const response1 = await fetch(buildUrl('/recipes'))
const response2 = await fetch(buildUrl('/batches'))
```

### 2. Not Handling Loading States

❌ **Don't forget loading states:**
```typescript
const recipes = ref([])
const fetchRecipes = async () => {
  const { data } = await useApi().get('/recipes')
  recipes.value = data.value
}
```

✅ **Show loading state:**
```typescript
const recipes = ref([])
const loading = ref(false)

const fetchRecipes = async () => {
  loading.value = true
  try {
    const { data } = await useApi().get('/recipes')
    recipes.value = data.value
  } finally {
    loading.value = false
  }
}
```

### 3. Not Using TypeScript Types

❌ **Untyped responses:**
```typescript
const { data } = await useApi().get('/recipes')
```

✅ **Type your responses:**
```typescript
interface Recipe {
  id: number
  name: string
  style: string
}

const { data } = await useApi().get<Recipe[]>('/recipes')
// Now data.value is typed as Recipe[] | null
```

### 4. Forgetting Error Handling

❌ **Ignoring errors:**
```typescript
const { data } = await useApi().post('/recipes', newRecipe)
navigateTo('/recipes')
```

✅ **Handle errors:**
```typescript
const { data, error } = await useApi().post('/recipes', newRecipe)
if (error.value) {
  toast.error('Failed to create recipe')
  return
}
navigateTo('/recipes')
```

## Quick Reference

### Import Statements

```typescript
// For URL building
import { useApiConfig } from '~/composables/useApiConfig'

// For API calls
import { useApi } from '~/composables/useApi'

// For domain operations
import { useRecipes } from '~/composables/useRecipes'
import { useBatches } from '~/composables/useBatches'
import { useInventory } from '~/composables/useInventory'
```

### Common Operations

```typescript
// Build URL
const { buildUrl } = useApiConfig()
const url = buildUrl('/recipes')

// GET
const { data, loading, error } = await useApi().get('/recipes')

// POST
const { data, loading, error } = await useApi().post('/recipes', newRecipe)

// PUT
const { data, loading, error } = await useApi().put('/recipes/123', updated)

// DELETE
const { data, loading, error } = await useApi().delete('/recipes/123')

// Health check
const { checkHealth } = useApiConfig()
const healthy = await checkHealth()
```

## Summary

1. **Never hardcode URLs** - Always use `useApiConfig()` or higher-level composables
2. **Choose the right tool** - `useApiConfig()` for URLs, `useApi()` for CRUD, domain composables for business logic
3. **Handle errors gracefully** - Always check for errors and provide feedback
4. **Show loading states** - Keep users informed during async operations
5. **Test thoroughly** - Test in both local and Docker environments
6. **Use TypeScript** - Type your API responses for better DX

Following these practices will make your code more maintainable, testable, and resilient to configuration changes.
