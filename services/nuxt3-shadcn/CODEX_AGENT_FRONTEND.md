# Frontend Component Analysis Agent Context

## Agent Mission
Analyze Vue.js components in the Nuxt3 frontend for better reusability, performance, and maintainability.

## Current Status
- ACTIVE: Analyzing components/ directory structure
- PHASE: Component reusability and performance analysis

## Key Findings So Far
- Code duplication in import dialog components
- Inconsistent prop usage patterns
- Missing composable utilities
- Hardcoded API URLs in components
- Repeated styling patterns that could be abstracted
- Batch detail cards duplicate form markup and rely on mutating object props
- DataTable component exposes undefined `columns` reference during empty states
- Database connection indicator hardcodes polling logic without lifecycle cleanup

## Directory Structure Analyzed
- ✅ components/ (top-level components)
- ✅ components/BeerXML/ - XML import/export functionality
- ✅ components/Buttons/ - Action buttons
- ✅ components/DropDown/ - Dropdown menus
- ✅ components/Sidebar/ - Navigation components
- ✅ components/Tabs/ - Tab interfaces
- ✅ components/UserAccount/ - User management
- ✅ components/XML/ - XML processing
- ✅ components/equipment/ - Equipment management
- ✅ components/ui/ - UI component library (shadcn)
- ✅ components/Batch* detail cards
- ✅ components/InventoryDetails.vue
- ✅ components/checkDatabaseConnection.vue

## Component Issues Identified
1. **Duplication**: Multiple import dialog components with similar structure
2. **Props**: Inconsistent prop definitions and validation
3. **API Calls**: Hardcoded localhost URLs
4. **Styling**: Repeated Tailwind class combinations
5. **State Management**: Local state that could be global
6. **Performance**: Missing lazy loading and memoization
7. **Prop Mutation**: Batch-related forms mutate nested object props rather than emitting updates
8. **Table Config**: DataTable relies on missing `columns` binding inside template, breaking empty state rendering
9. **Connectivity Polling**: checkDatabaseConnection.vue fetches `http://localhost:8000` without lifecycle cleanup or runtime config

## TODO Tasks
- [ ] Create reusable dialog component template
- [ ] Abstract API URL configuration
- [ ] Implement global state management
- [ ] Create utility composables for common functionality
- [ ] Optimize component rendering performance
- [ ] Standardize prop interfaces
- [ ] Implement proper error handling patterns
- [ ] Introduce field-definition driven detail cards for batches/notes/water
- [ ] Normalize child component updates to use emits/defineModel instead of deep prop mutation
- [ ] Fix DataTable prop exposure to leverage `props.columns` and memoized getters
- [ ] Move connectivity polling into reusable composable with runtime-configured base URL
- [ ] Add typed props + fallback rendering to cards (BeerCard, ReferenceCard, StyleCard)

## Recommendations in Progress
1. Create generic ImportDialog.vue template
2. Implement useAPI composable for consistent API calls
3. Extract common styling into utility classes
4. Add prop validation and TypeScript interfaces
5. Implement lazy loading for heavy components
6. Build `DetailsCard` wrapper + schema-driven input renderer for Batch/Water/Notes blocks
7. Refactor InventoryDetails to iterate over typed ingredient descriptors instead of repeated templates
8. Replace ad-hoc connectivity checks with `useConnectionStatus` composable using `$fetch` and interval management
9. Expose typed column definitions via composable helper for DataTable

## Latest Component Review Notes
- `components/BatchDetails.vue`: Four nearly identical input blocks; relies on mutating `batch` prop. Recommend schema-driven renderer, `defineProps` typings, and emitting `update:batch` payloads.
- `components/NotesDetails.vue` & `components/WaterDetails.vue`: Share layout with BatchDetails; good candidates for new `DetailsCard` + shared textarea/input field component.
- `components/InventoryDetails.vue`: Repeats `<template v-for>` groups per ingredient type. Suggest mapping ingredient descriptors and a single row renderer; consider virtual scrolling for large inventories.
- `components/DataTable.vue`: Template references `columns.length` without exposing `columns`; destructure via `const columns = computed(() => props.columns)` or access through `table.getAllColumns()`.
- `components/checkDatabaseConnection.vue`: Hardcoded fetch, missing interval cleanup. Replace with composable using runtime config (`useRuntimeConfig().public.apiBase`) and `onMounted/onUnmounted` for polling.
- `components/StyleCard.vue` & `components/BeerCard.vue`: Lacking prop typing/validation; repeated label-value flex rows could be abstracted into reusable `KeyValueList` component.

## Agent Log
- Started component structure analysis
- Identified code duplication patterns
- Currently reviewing component architecture
- Reviewed BatchDetails*, NotesDetails, WaterDetails, InventoryDetails, DataTable, and checkDatabaseConnection for reuse/perf gaps
