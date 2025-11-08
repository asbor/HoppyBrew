# Inventory Management Integration

This document describes the inventory management integration implemented for HoppyBrew Issue #3.

## Overview

The inventory management system tracks ingredient consumption for batches, maintains an audit trail of all inventory changes, and provides real-time availability warnings during batch creation.

## Backend Implementation

### Database Models

#### BatchIngredient
Tracks ingredient consumption for each batch.

**Fields:**
- `id`: Primary key
- `batch_id`: Foreign key to batches table
- `inventory_item_id`: ID of the inventory item consumed
- `inventory_item_type`: Type of ingredient ('hop', 'fermentable', 'yeast', 'misc')
- `quantity_used`: Amount consumed
- `unit`: Unit of measurement (kg, g, L, ml, etc.)
- `created_at`: Timestamp of consumption

#### InventoryTransaction
Provides complete audit trail for all inventory changes.

**Fields:**
- `id`: Primary key
- `inventory_item_id`: ID of the inventory item
- `inventory_item_type`: Type of ingredient
- `transaction_type`: Type of transaction ('addition', 'consumption', 'adjustment')
- `quantity_change`: Amount changed (positive for addition, negative for consumption)
- `quantity_before`: Stock level before transaction
- `quantity_after`: Stock level after transaction
- `unit`: Unit of measurement
- `reference_type`: Type of related entity (e.g., 'batch', 'manual')
- `reference_id`: ID of related entity
- `notes`: Optional notes about the transaction
- `created_at`: Timestamp of transaction
- `created_by`: User who performed the transaction (optional)

### API Endpoints

#### POST /batches/{batch_id}/consume-ingredients
Deducts ingredients from inventory for a batch.

**Request Body:**
```json
{
  "ingredients": [
    {
      "batch_id": 1,
      "inventory_item_id": 5,
      "inventory_item_type": "hop",
      "quantity_used": 0.5,
      "unit": "kg"
    }
  ]
}
```

**Response:**
```json
{
  "message": "Ingredients consumed successfully",
  "batch_id": 1,
  "consumed_count": 1,
  "transactions_created": 1
}
```

**Validation:**
- Verifies batch exists
- Checks inventory item exists
- Validates sufficient stock is available
- Creates batch_ingredient records
- Updates inventory stock levels
- Creates transaction records for audit trail

#### GET /batches/{batch_id}/ingredient-tracking
Retrieves ingredient consumption tracking for a batch.

**Response:**
```json
{
  "batch_id": 1,
  "batch_name": "Test Batch",
  "consumed_ingredients": [
    {
      "id": 1,
      "batch_id": 1,
      "inventory_item_id": 5,
      "inventory_item_type": "hop",
      "quantity_used": 0.5,
      "unit": "kg",
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "transactions": [
    {
      "id": 1,
      "inventory_item_id": 5,
      "inventory_item_type": "hop",
      "transaction_type": "consumption",
      "quantity_change": -0.5,
      "quantity_before": 10.0,
      "quantity_after": 9.5,
      "unit": "kg",
      "reference_type": "batch",
      "reference_id": 1,
      "notes": "Consumed for batch Test Batch",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

#### GET /batches/check-inventory-availability/{recipe_id}
Checks inventory availability for a recipe's ingredients.

**Response:**
```json
[
  {
    "inventory_item_id": 5,
    "inventory_item_type": "hop",
    "name": "Cascade",
    "available_quantity": 10.0,
    "required_quantity": 0.5,
    "unit": "kg",
    "is_available": true,
    "warning_level": null
  },
  {
    "inventory_item_id": 12,
    "inventory_item_type": "fermentable",
    "name": "Pale Malt",
    "available_quantity": 0.2,
    "required_quantity": 5.0,
    "unit": "kg",
    "is_available": false,
    "warning_level": "out_of_stock"
  }
]
```

**Warning Levels:**
- `null`: Sufficient stock available
- `"low_stock"`: Less than 1.5x required quantity available
- `"out_of_stock"`: Insufficient stock to fulfill recipe requirements

## Frontend Implementation

### Composables

#### useInventory Extension
Extended the existing `useInventory` composable with three new functions:

```typescript
// Check inventory availability for a recipe
const { data, error } = await checkInventoryAvailability(recipeId)

// Consume ingredients for a batch
const { data, error } = await consumeIngredients(batchId, ingredients)

// Get ingredient tracking for a batch
const { data, error } = await getIngredientTracking(batchId)
```

### Components

#### InventoryAvailabilityCheck
Displays real-time inventory availability during batch creation.

**Features:**
- Automatically checks availability when recipe is selected
- Color-coded warnings:
  - Green: Sufficient stock
  - Yellow: Low stock warning
  - Red: Out of stock
- Shows required vs available quantities for each ingredient
- Displays warning banner if any ingredients are out of stock

**Usage:**
```vue
<InventoryAvailabilityCheck :recipe-id="selectedRecipeId" />
```

#### IngredientConsumptionTracking
Shows ingredient consumption history and transaction log for a batch.

**Features:**
- Lists all consumed ingredients with quantities and timestamps
- Displays complete transaction history
- Color-coded transaction types:
  - Red: Consumption
  - Green: Addition
  - Blue: Adjustment
- Shows before/after stock levels for each transaction

**Usage:**
```vue
<IngredientConsumptionTracking :batch-id="batchId" />
```

## Testing

### Backend Tests
9 comprehensive tests covering:
- ✅ Successful ingredient consumption
- ✅ Insufficient stock validation
- ✅ Invalid batch handling
- ✅ Ingredient tracking retrieval
- ✅ Empty batch tracking
- ✅ Invalid batch tracking
- ✅ Inventory availability checking
- ✅ Invalid recipe availability check
- ✅ Batch deletion cascade (removes batch_ingredients)

All tests pass with 100% success rate.

### Running Tests
```bash
cd services/backend
python -m pytest tests/test_endpoints/test_inventory_management.py -v
```

## Database Migration

A migration file has been created to add the new tables:

**File:** `services/backend/migrations/versions/0007_add_inventory_tracking.py`

**Tables Created:**
- `batch_ingredients` with indexes on batch_id and inventory_item_id
- `inventory_transactions` with indexes on item_id, created_at, and transaction_type

**To Apply Migration:**
```bash
cd services/backend
alembic upgrade head
```

## Usage Examples

### Backend: Consuming Ingredients
```python
# Example: Consume ingredients for a batch
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Schemas as schemas

consume_request = schemas.ConsumeIngredientsRequest(
    ingredients=[
        schemas.BatchIngredientCreate(
            batch_id=1,
            inventory_item_id=5,
            inventory_item_type="hop",
            quantity_used=0.5,
            unit="kg"
        )
    ]
)

# POST to /batches/1/consume-ingredients
```

### Frontend: Checking Availability
```vue
<template>
  <div>
    <select v-model="selectedRecipe">
      <option v-for="recipe in recipes" :value="recipe.id">
        {{ recipe.name }}
      </option>
    </select>
    
    <!-- Automatically shows availability when recipe is selected -->
    <InventoryAvailabilityCheck 
      v-if="selectedRecipe" 
      :recipe-id="selectedRecipe" 
    />
  </div>
</template>
```

### Frontend: Viewing Consumption History
```vue
<template>
  <div>
    <!-- In batch detail page -->
    <IngredientConsumptionTracking :batch-id="batchId" />
  </div>
</template>
```

## Future Enhancements

Potential improvements for future iterations:

1. **Automatic Consumption**: Automatically consume ingredients when batch status changes
2. **Inventory Forecasting**: Predict when ingredients will run out based on usage patterns
3. **Substitution Suggestions**: Suggest alternative ingredients when stock is low
4. **Bulk Operations**: Support consuming ingredients for multiple batches at once
5. **Export Reports**: Generate inventory usage reports for accounting
6. **Real-time Notifications**: Alert users when ingredients reach low stock threshold
7. **Master Inventory System**: Create separate master inventory tables independent of batches

## Security Considerations

- All endpoints validate batch and inventory item existence
- Stock level validation prevents over-consumption
- Transaction logging provides complete audit trail
- No security vulnerabilities detected by CodeQL analysis

## Related Issues

- Implements: #3 - Inventory Management Integration
- Depends on: #1 - Batch Status (already implemented)
- Blocks: #8 (not specified in this implementation)
