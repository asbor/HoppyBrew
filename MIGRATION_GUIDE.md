# Migration Guide: Fixing Hardcoded API URLs

## Status

This document tracks the migration of hardcoded `http://localhost:8000` URLs to use the centralized `useApiConfig()` composable.

**Last Updated:** 2025-11-11

## Progress

- **Total Files with Hardcoded URLs:** ~70
- **Files Fixed:** 5
- **Files Remaining:** ~65

## Files Fixed ✅

1. ✅ `services/nuxt3-shadcn/pages/batches/newBatch.vue`
2. ✅ `services/nuxt3-shadcn/pages/references/newReferences.vue`
3. ✅ `services/nuxt3-shadcn/pages/references/[id].vue`
4. ✅ `services/nuxt3-shadcn/pages/styles.vue`
5. ✅ `services/nuxt3-shadcn/composables/useApi.ts`

## Files Needing Migration 🔄

### High Priority (Core Features)

These files are used in critical user workflows and should be fixed first:

#### Inventory Management
- [ ] `pages/inventory/yeasts/index.vue` (2 occurrences)
- [ ] `pages/inventory/yeasts/newYeast.vue` (1 occurrence)
- [ ] `pages/inventory/yeasts/[id].vue` (2 occurrences)
- [ ] `pages/inventory/hops/index.vue` (2 occurrences)
- [ ] `pages/inventory/hops/newHop.vue` (1 occurrence)
- [ ] `pages/inventory/hops/[id].vue` (2 occurrences)
- [ ] `pages/inventory/miscs/index.vue` (2 occurrences)
- [ ] `pages/inventory/miscs/newMisc.vue` (1 occurrence)
- [ ] `pages/inventory/miscs/[id].vue` (2 occurrences)
- [ ] `pages/inventory/fermentables/newFermentable.vue` (1 occurrence)
- [ ] `pages/inventory/fermentables/index.vue` (2 occurrences)
- [ ] `pages/inventory/fermentables/[id].vue` (2 occurrences)

#### Recipe Management
- [ ] `pages/recipes/newRecipe.vue` (1 occurrence)

#### Profile Management
- [ ] `pages/profiles/mash/newMash.vue` (3 occurrences)
- [ ] `pages/profiles/mash/index.vue` (2 occurrences)
- [ ] `pages/profiles/mash/[id].vue` (7 occurrences)
- [ ] `pages/profiles/equipment/index.vue` (5 occurrences)
- [ ] `pages/profiles/water/index.vue` (1 occurrence)

#### Import/Export
- [ ] `pages/ImportXML.vue` (1 occurrence)
- [ ] `components/XML/ImportReferenceDialog.vue` (1 occurrence)
- [ ] `components/XML/ExportReferenceDialog.vue` (1 occurrence)

#### BeerXML Components
- [ ] `components/BeerXML/ImportMiscDialog.vue` (1 occurrence)
- [ ] `components/BeerXML/ImportHopDialog.vue` (1 occurrence)
- [ ] `components/BeerXML/ImportFermentableDialog.vue` (1 occurrence)
- [ ] `components/BeerXML/ImportYeastDialog.vue` (1 occurrence)
- [ ] `components/BeerXML/ImportRecipeDialog.vue` (2 occurrences)

#### Batch Management
- [ ] `components/batch/FermentationTracker.vue` (4 occurrences)

#### Other Components
- [ ] `components/tools/HopScheduleOptimizer.vue` (2 occurrences)
- [ ] `components/EquipmentCard.vue` (1 occurrence)
- [ ] `components/mash/MashTemplateSelector.vue` (1 occurrence)
- [ ] `components/equipment/NewDialog.vue` (2 occurrences)
- [ ] `components/equipment/EditDialog.vue` (1 occurrence)
- [ ] `components/user/NewDialog.vue` (2 occurrences)
- [ ] `components/Buttons/ScriptTrigger.vue` (1 occurrence)

## Migration Patterns

### Pattern 1: Simple Fetch in Composition API (Script Setup)

**Before:**
```vue
<script setup>
import { ref } from 'vue';

const data = ref([]);

async function fetchData() {
    const response = await fetch('http://localhost:8000/recipes');
    data.value = await response.json();
}
</script>
```

**After:**
```vue
<script setup>
import { ref } from 'vue';

const data = ref([]);
const { buildUrl } = useApiConfig();

async function fetchData() {
    const response = await fetch(buildUrl('/recipes'));
    data.value = await response.json();
}
</script>
```

### Pattern 2: Fetch with Options

**Before:**
```vue
const response = await fetch('http://localhost:8000/batches', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(batch),
});
```

**After:**
```vue
const { buildUrl } = useApiConfig();
const response = await fetch(buildUrl('/batches'), {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(batch),
});
```

### Pattern 3: Axios Calls

**Before:**
```vue
await axios.post('http://localhost:8000/references', reference.value);
await axios.get(`http://localhost:8000/references/${id}`);
await axios.put(`http://localhost:8000/references/${id}`, data);
await axios.delete(`http://localhost:8000/references/${id}`);
```

**After:**
```vue
const { buildUrl } = useApiConfig();
await axios.post(buildUrl('/references'), reference.value);
await axios.get(buildUrl(`/references/${id}`));
await axios.put(buildUrl(`/references/${id}`), data);
await axios.delete(buildUrl(`/references/${id}`));
```

### Pattern 4: Options API (Vue 2 Style)

**Before:**
```vue
<script>
export default {
    methods: {
        async fetchData() {
            const response = await fetch('http://localhost:8000/recipes');
            this.recipes = await response.json();
        }
    }
}
</script>
```

**After:**
```vue
<script>
export default {
    setup() {
        const { buildUrl } = useApiConfig();
        return { buildUrl };
    },
    methods: {
        async fetchData() {
            const response = await fetch(this.buildUrl('/recipes'));
            this.recipes = await response.json();
        }
    }
}
</script>
```

### Pattern 5: Multiple Calls in Same Function

**Before:**
```vue
async function saveProfile() {
    await axios.put(`http://localhost:8000/mash/${id}`, mash);
    const steps = await axios.get(`http://localhost:8000/mash/${id}/steps`);
    for (const step of steps) {
        await axios.delete(`http://localhost:8000/mash/steps/${step.id}`);
    }
}
```

**After:**
```vue
const { buildUrl } = useApiConfig();

async function saveProfile() {
    await axios.put(buildUrl(`/mash/${id}`), mash);
    const steps = await axios.get(buildUrl(`/mash/${id}/steps`));
    for (const step of steps) {
        await axios.delete(buildUrl(`/mash/steps/${step.id}`));
    }
}
```

## Migration Checklist for Each File

When migrating a file, follow these steps:

1. **Import/Declare `useApiConfig()`**
   - For `<script setup>`: Add `const { buildUrl } = useApiConfig();` near the top
   - For Options API: Add it in the `setup()` method

2. **Find all `http://localhost:8000` strings**
   - Use your editor's find function (Ctrl+F or Cmd+F)
   - Look for: `http://localhost:8000`

3. **Replace each occurrence**
   - `'http://localhost:8000/path'` → `buildUrl('/path')`
   - ``http://localhost:8000/${var}`` → `buildUrl(\`/${var}\`)`
   - `"http://localhost:8000/path"` → `buildUrl("/path")`

4. **Test the changes**
   - Ensure the page still loads
   - Test all API calls on that page
   - Check browser console for errors

5. **Mark file as complete**
   - Update this document
   - Check the box in the "Files Needing Migration" section

## Testing After Migration

### Local Development Test
```bash
# Start backend
cd services/backend
uvicorn main:app --reload

# Start frontend
cd services/nuxt3-shadcn
yarn dev

# Open browser and test the migrated pages
```

### Docker Test
```bash
# Start services
docker-compose up -d

# Check logs
docker logs hoppybrew-frontend-1 -f
docker logs hoppybrew-backend-1 -f

# Test in browser at http://localhost:3000
```

### Verification Script
```bash
# Run the URL finder script to check remaining hardcoded URLs
./scripts/find_hardcoded_urls.sh
```

## Tips

1. **Use Search & Replace Carefully**
   - Don't do global search & replace without reviewing each change
   - Some files (like tests or configs) might legitimately have localhost URLs

2. **Test Incrementally**
   - Fix and test a few files at a time
   - Don't fix all files and then test - you'll have trouble finding issues

3. **Handle Template Literals**
   - Pay special attention to template literals with variables
   - ``http://localhost:8000/${id}`` becomes `buildUrl(\`/${id}\`)`

4. **Watch for String Concatenation**
   - `'http://localhost:8000' + '/path'` becomes `buildUrl('/path')`
   - `'http://localhost:8000/path/' + id` becomes `buildUrl(\`/path/${id}\`)`

5. **Check for Different Quote Styles**
   - Single quotes: `'http://localhost:8000/path'`
   - Double quotes: `"http://localhost:8000/path"`
   - Template literals: `` `http://localhost:8000/path` ``

## Common Issues

### Issue 1: `buildUrl is not defined`

**Cause:** Forgot to import/declare `useApiConfig()`

**Solution:** Add `const { buildUrl } = useApiConfig();` at the top of `<script setup>`

### Issue 2: TypeScript errors

**Cause:** TypeScript might not recognize the imported function

**Solution:** Ensure composables are properly exported and TypeScript can find them

### Issue 3: Options API not working

**Cause:** Options API needs special setup

**Solution:** Use the Pattern 4 example above, return `buildUrl` from `setup()`

## Next Steps

1. Fix high-priority inventory management pages first (most used feature)
2. Fix profile management pages
3. Fix import/export components
4. Fix remaining components
5. Run comprehensive tests
6. Update this document as files are completed
7. Remove all `.backup` files created during migration
8. Run `./scripts/find_hardcoded_urls.sh` to verify all files are fixed

## Questions or Issues?

If you encounter any issues during migration:

1. Review the [API_BEST_PRACTICES.md](./API_BEST_PRACTICES.md) document
2. Review the [DEBUGGING_GUIDE.md](./DEBUGGING_GUIDE.md) document
3. Check the already-migrated files for reference examples
4. Ask for help if you're stuck

## Summary

This migration is critical for:
- ✅ Making the app work in Docker environments
- ✅ Supporting different deployment environments (dev, staging, prod)
- ✅ Preventing connectivity issues
- ✅ Making the codebase more maintainable

**Remember:** The goal is to eliminate all hardcoded `http://localhost:8000` URLs from Vue components, replacing them with `useApiConfig().buildUrl()` calls.
