# Batch Status Workflow System - Usage Guide

## Overview

The batch status workflow system provides a complete tracking mechanism for brewing batches through their lifecycle from planning to completion.

## Backend API Endpoints

### 1. Update Batch Status
**Endpoint**: `PUT /batches/{id}/status`

Updates the batch status with state machine validation. Only valid transitions are allowed.

**Request Body**:
```json
{
  "status": "brewing",
  "notes": "Started brew day at 8am"
}
```

**Response**: Returns the updated batch object

**Error Codes**:
- 404: Batch not found
- 400: Invalid status or invalid transition

### 2. Get Workflow History
**Endpoint**: `GET /batches/{id}/workflow`

Returns the complete workflow history for a batch in reverse chronological order.

**Response**:
```json
[
  {
    "id": 1,
    "batch_id": 11,
    "from_status": "planning",
    "to_status": "brewing",
    "changed_at": "2024-03-21T08:00:00Z",
    "notes": "Started brew day"
  }
]
```

### 3. Get Valid Transitions
**Endpoint**: `GET /batches/{id}/status/transitions`

Returns the valid status transitions for a batch's current status.

**Response**:
```json
{
  "current_status": "planning",
  "valid_transitions": ["brewing", "archived"]
}
```

## State Machine

The workflow enforces the following valid transitions:

```
Planning → Brewing, Archived
Brewing → Fermenting, Archived
Fermenting → Conditioning, Archived
Conditioning → Packaging, Archived
Packaging → Complete, Archived
Complete → Archived
Archived → (terminal state, no transitions)
```

## Frontend Components

### BatchStatusUpdate Component

A component that allows users to update the batch status with validation.

**Usage**:
```vue
<template>
  <BatchStatusUpdate 
    :batch="currentBatch" 
    @statusUpdated="handleStatusUpdate"
  />
</template>

<script setup>
const handleStatusUpdate = (updatedBatch) => {
  // Handle the updated batch
  console.log('Batch updated:', updatedBatch)
}
</script>
```

**Features**:
- Shows current status with visual indicator
- Displays only valid next statuses in dropdown
- Optional notes field for status changes
- Error and success message display
- Disabled state during updates

### BatchWorkflowTimeline Component

A component that displays the complete workflow history as a visual timeline.

**Usage**:
```vue
<template>
  <BatchWorkflowTimeline :batch-id="batchId" />
</template>
```

**Features**:
- Visual timeline with color-coded status dots
- Shows transition dates and times
- Displays transition notes
- Most recent status at the top
- Loading and error states

## Composable Usage

### useBatches Composable

```typescript
import { useBatches } from '@/composables/useBatches'

const { updateStatus, fetchWorkflowHistory, fetchValidTransitions } = useBatches()

// Update batch status
const result = await updateStatus(batchId, {
  status: 'brewing',
  notes: 'Started brew day'
})

// Get workflow history
const history = await fetchWorkflowHistory(batchId)

// Get valid transitions
const transitions = await fetchValidTransitions(batchId)
```

## Integration Examples

### Add to Batch Detail Page

```vue
<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Status Update Card -->
    <BatchStatusUpdate 
      :batch="currentBatch" 
      @statusUpdated="refreshBatch"
    />
    
    <!-- Workflow Timeline Card -->
    <BatchWorkflowTimeline :batch-id="currentBatch.id" />
  </div>
</template>

<script setup>
import BatchStatusUpdate from '@/components/batch/BatchStatusUpdate.vue'
import BatchWorkflowTimeline from '@/components/batch/BatchWorkflowTimeline.vue'

const { currentBatch, fetchOne } = useBatches()

async function refreshBatch() {
  await fetchOne(currentBatch.value.id)
}
</script>
```

### Filter Batches by Status

The batch list page has been updated with filters for all status values:
- Planning
- Brewing
- Fermenting
- Conditioning
- Packaging
- Complete
- Archived

## Database Schema

### batch_workflow_history Table

```sql
CREATE TABLE batch_workflow_history (
    id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    from_status VARCHAR(50),
    to_status VARCHAR(50) NOT NULL,
    changed_at TIMESTAMP NOT NULL,
    notes TEXT
);

CREATE INDEX ix_batch_workflow_history_batch_id ON batch_workflow_history(batch_id);
CREATE INDEX ix_batch_workflow_history_changed_at ON batch_workflow_history(changed_at);
```

## Testing

All backend functionality is covered by comprehensive tests in `services/backend/tests/test_endpoints/test_batch_workflow.py`:

- Status transition validation
- Workflow history tracking
- Valid transitions lookup
- Error handling
- Complete workflow sequences

Run tests with:
```bash
pytest services/backend/tests/test_endpoints/test_batch_workflow.py -v
```

## Migration

To apply the new database schema, run:
```bash
alembic upgrade head
```

This will create the `batch_workflow_history` table and update the batch status field.
