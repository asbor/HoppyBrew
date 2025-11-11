# ISSUE-006: Batch Status Alignment Between Frontend and Backend

## Status: PARTIALLY RESOLVED
**Priority:** P1-High  
**Created:** 2025-11-11  
**Last Updated:** 2025-11-11

## Problem Description

The frontend and backend use different batch status values, causing validation errors when the backend tries to process status updates from the frontend.

### Error Example
```
Invalid status 'brew_day'. Valid statuses: planning, brewing, fermenting, conditioning, packaging, complete, archived
```

## Root Cause

The backend uses a simplified 7-state workflow model defined in `Database/enums.py`:
- `planning`, `brewing`, `fermenting`, `conditioning`, `packaging`, `complete`, `archived`

The frontend uses a more granular workflow with additional states:
- `planning`, `brewing`, `primary_fermentation`, `secondary_fermentation`, `conditioning`, `packaged`, `completed`, `archived`

## Resolution Status

### ✅ Fixed (2025-11-11)
1. **Invalid `brew_day` status** → Changed to `brewing`
   - Backend: `services/backend/Database/Schemas/batches.py`
   - Frontend: 
     - `pages/batches/[id].vue`
     - `pages/batches/[id]/index.vue`
     - `components/batch/BatchPhaseNavigation.vue`
     - `composables/useStatusColors.ts`
   - Tool: `services/backend/fix_batch_statuses.py` (migration script)

### ⚠️ Remaining Mismatches
These statuses still differ between frontend and backend:

| Frontend Status | Backend Status | Impact |
|-----------------|----------------|--------|
| `primary_fermentation` | `fermenting` | Frontend cannot update to this status |
| `secondary_fermentation` | `fermenting` | Frontend cannot update to this status |
| `packaged` | `packaging` | Frontend cannot update to this status |
| `completed` | `complete` | Frontend cannot update to this status |

## Impact Assessment

**Current Impact:**
- ✅ Batches can now move from `planning` → `brewing` without error
- ❌ Batches cannot transition to fermentation states (primary/secondary)
- ❌ Batches cannot transition to packaging/packaged state
- ❌ Batches cannot be marked as completed/complete

**Workaround:**
Users can manually update batch status via API using correct backend status values.

## Recommended Solutions

### Option 1: Simplify Frontend (Recommended)
**Pros:**
- Aligns with backend state machine
- Simpler maintenance
- Clear state transitions

**Cons:**
- Less UI granularity
- Changes required in multiple frontend components

**Changes Required:**
```javascript
// Replace all frontend status references:
'primary_fermentation' → 'fermenting'
'secondary_fermentation' → 'fermenting'  // Remove or handle as UI state only
'packaged' → 'packaging'
'completed' → 'complete'
```

### Option 2: Extend Backend States
**Pros:**
- Maintains frontend granularity
- No frontend changes needed

**Cons:**
- More complex state machine
- Backend changes required
- Need to update state transitions

**Changes Required:**
```python
# In Database/enums.py:
class BatchStatus(str, Enum):
    PLANNING = "planning"
    BREWING = "brewing"
    PRIMARY_FERMENTATION = "primary_fermentation"
    SECONDARY_FERMENTATION = "secondary_fermentation"
    CONDITIONING = "conditioning"
    PACKAGING = "packaging"
    PACKAGED = "packaged"
    COMPLETE = "complete"
    ARCHIVED = "archived"

# Update BATCH_STATUS_TRANSITIONS accordingly
```

### Option 3: Hybrid Approach (Best Long-term)
**Backend:** Keep simple 7-state model  
**Frontend:** Map granular UI states to backend states

**Implementation:**
```typescript
// In frontend composable:
const FRONTEND_TO_BACKEND_STATUS_MAP = {
  'planning': 'planning',
  'brewing': 'brewing',
  'primary_fermentation': 'fermenting',
  'secondary_fermentation': 'fermenting',
  'conditioning': 'conditioning',
  'packaged': 'packaging',
  'completed': 'complete',
  'archived': 'archived',
}

function mapStatusForBackend(frontendStatus: string): string {
  return FRONTEND_TO_BACKEND_STATUS_MAP[frontendStatus] || frontendStatus
}
```

## Files Affected

### Backend
- `services/backend/Database/enums.py` - Status enum definition
- `services/backend/Database/Models/batches.py` - Batch model
- `services/backend/Database/Schemas/batches.py` - Pydantic schemas
- `services/backend/api/endpoints/batches.py` - Status update endpoint
- `services/backend/api/state_machine.py` - State transition validation
- `services/backend/fix_batch_statuses.py` - Migration script (new)

### Frontend
- `pages/batches/[id].vue` - Batch detail page
- `pages/batches/[id]/index.vue` - Batch detail index
- `components/batch/BatchPhaseNavigation.vue` - Phase navigation UI
- `components/batch/BatchPlanningPhase.vue`
- `components/batch/BatchBrewingPhase.vue`
- `components/batch/BatchFermentationPhase.vue`
- `components/batch/BatchConditioningPhase.vue`
- `components/batch/BatchPackagedPhase.vue`
- `components/batch/BatchCompletedPhase.vue`
- `composables/useBatches.ts` - Batch API calls
- `composables/useStatusColors.ts` - Status color mapping
- `tests/e2e/specs/batch-workflow.spec.ts` - E2E tests
- `test/components/BatchCard.spec.ts` - Unit tests

## Next Steps

1. **Immediate:** Test the `brew_day` → `brewing` fix in production
2. **Short-term:** Implement Option 3 (Hybrid Approach) 
   - Add status mapping function in `useBatches` composable
   - Update all `updateStatus` calls to use mapping
3. **Medium-term:** Refactor frontend to align with backend states
4. **Long-term:** Consider if frontend needs true multi-state fermentation tracking

## Testing Checklist

- [ ] Create new batch in planning state
- [ ] Move batch from planning → brewing
- [ ] Move batch from brewing → fermenting (primary)
- [ ] Move batch from fermenting → conditioning
- [ ] Move batch from conditioning → packaging
- [ ] Move batch from packaging → complete
- [ ] Move batch from complete → archived
- [ ] Verify all state transitions in workflow history
- [ ] Check batch status colors display correctly
- [ ] Verify phase navigation UI matches current status

## References

- Backend State Machine: `services/backend/api/state_machine.py`
- Backend Enum: `services/backend/Database/enums.py`
- Frontend Status Logic: `services/nuxt3-shadcn/composables/useBatches.ts`
- Fix Script: `services/backend/fix_batch_statuses.py`

## Related Issues

- None currently

## Notes

The `brew_day` status was likely a legacy naming convention that wasn't properly updated when the backend enum was standardized. The broader status misalignment suggests the frontend was developed with a different workflow model than ultimately implemented in the backend.

Consider documenting the intended batch workflow in a separate architecture document to prevent future misalignments.
