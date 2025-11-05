# Brewing Workflow Implementation Guide

## Overview

This document describes the implemented brewing workflow features in HoppyBrew, focusing on the comprehensive brewing lifecycle tracking system.

**Date**: November 5, 2025  
**Status**: Partial Implementation - Frontend Components Ready  
**Version**: 1.0

---

## ✅ Completed Implementations

### 1. Brewing Calculators Suite (`useCalculators` Composable)

A comprehensive calculation library for all brewing formulas, centralized for reuse across the application.

**Location**: `services/nuxt3-shadcn/composables/useCalculators.ts`

**Available Functions**:

#### Core Calculations
- `calculateABV(og, fg)` - Alcohol by Volume using standard formula
- `calculateIBU(alphaAcid, hopWeight, boilTime, batchSize, boilGravity)` - Bitterness using Tinseth formula
- `calculateSRM(grainColor, grainWeight, batchSize)` - Beer color using Morey equation
- `getSRMColor(srmValue)` - Get hex color for SRM value

#### Brewing Tools
- `calculatePrimingSugar(volume, desiredCO2, temperature, sugarType)` - Carbonation sugar needs
- `calculateStrikeWater(grainTemp, targetTemp, grainWeight, ratio)` - Mash water calculations
- `calculateDilution(currentGravity, currentVolume, targetGravity)` - Wort dilution
- `calculateYeastPitchRate(targetGravity, batchVolume, yeastType)` - Required yeast cells

#### Analysis Functions
- `calculateMashEfficiency(og, grainWeight, batchSize, potentialOG)` - Efficiency percentage
- `calculateAttenuation(og, fg)` - Fermentation attenuation
- `gravityToPlato(gravity)` - Convert gravity to Plato degrees
- `platoToGravity(plato)` - Convert Plato to gravity

**Usage Example**:
```typescript
const calculators = useCalculators()
const abv = calculators.calculateABV(1.055, 1.012)
console.log(abv.formatted) // "5.64%"
```

### 2. Enhanced Inventory Dashboard

**Location**: `services/nuxt3-shadcn/pages/inventory/index.vue`

**Features**:
- Real-time inventory statistics across all categories
- Low stock warnings with configurable thresholds
- Quick action buttons for adding new items
- Total amount displays per category
- Visual cards with hover effects

**Key Capabilities**:
- Monitors fermentables, hops, yeasts, and miscellaneous items
- Displays low stock count with warning badges
- Aggregates total amounts across inventory
- Links to detailed inventory pages

### 3. Batch Status Timeline Component

**Location**: `services/nuxt3-shadcn/components/BatchStatusTimeline.vue`

**Features**:
- Visual workflow progression through 7 brewing stages
- Interactive timeline with status indicators
- Color-coded status badges
- Batch details display (dates, gravity readings, fermentation days)

**Brewing Stages**:
1. **Design** - Recipe planning and formulation
2. **Planning** - Pre-brew preparation and ingredient allocation
3. **Brewing** - Active brew day
4. **Fermenting** - Primary and secondary fermentation
5. **Conditioning** - Cold crash and maturation
6. **Packaging** - Bottling or kegging
7. **Complete** - Finished and ready to drink

**Status Visualization**:
- Completed steps: Green checkmark
- Current step: Highlighted with ring
- Future steps: Grayed out
- Progress bar showing completion percentage

**Usage Example**:
```vue
<BatchStatusTimeline :batch="{
  id: '123',
  name: 'West Coast IPA',
  status: 'fermenting',
  og: 1.065,
  fg: 1.012,
  days_in_fermentation: 7
}" />
```

### 4. Recipe Calculator Widget

**Location**: `services/nuxt3-shadcn/components/RecipeCalculatorWidget.vue`

**Features**:
- Live calculation display based on recipe values
- Shows ABV, IBU, SRM, Attenuation
- Visual color representation for SRM
- Automatic updates when recipe changes
- Handles multiple hop additions for total IBU

**Display Metrics**:
- Alcohol by Volume (ABV%)
- Bitterness (IBU)
- Color (SRM) with visual swatch
- Attenuation percentage
- Original & Final Gravity
- Batch size

**Usage Example**:
```vue
<RecipeCalculatorWidget 
  :og="1.055"
  :fg="1.012"
  :batch-size="20"
  :grain-weight="5.0"
  :grain-color="8"
  :boil-gravity="1.055"
  :hop-additions="[
    { alphaAcid: 12, weight: 30, boilTime: 60 },
    { alphaAcid: 8, weight: 20, boilTime: 15 }
  ]"
/>
```

### 5. UI Components

#### Alert Component
**Location**: `services/nuxt3-shadcn/components/ui/alert/`

Notification component with support for:
- Default alerts
- Destructive alerts (errors)
- Warning alerts (yellow theme)

**Usage**:
```vue
<Alert variant="warning">
  <AlertDescription>
    Low stock warning: 3 items running low
  </AlertDescription>
</Alert>
```

#### Enhanced Badge Component
**Location**: `services/nuxt3-shadcn/components/ui/badge/`

Added `warning` variant for low stock indicators.

**Variants**:
- `default` - Primary color
- `secondary` - Secondary color
- `destructive` - Red
- `outline` - Border only
- `warning` - Yellow (NEW)

---

## 📋 Workflow Integration Points

### Recipe Design Flow
1. User creates/edits recipe in recipe editor
2. `RecipeCalculatorWidget` shows live calculations
3. Calculator values update as user inputs change
4. `useCalculators` composable provides all formulas
5. Recipe saved with calculated values

### Inventory Management Flow
1. Dashboard shows current stock levels
2. Low stock items flagged with warnings
3. User can quickly add new items
4. Inventory tracked across all categories
5. Integration ready for batch deduction (backend needed)

### Batch Tracking Flow
1. Batch created from recipe
2. `BatchStatusTimeline` shows current stage
3. User progresses through brewing stages
4. Status updated manually or automatically (backend needed)
5. Fermentation tracking integrated (backend needed)

---

## 🚧 Backend Requirements (Not Yet Implemented)

### Database Schema Changes Needed

#### 1. Batch Status Enum
```sql
ALTER TABLE batches 
ADD COLUMN status VARCHAR(20) DEFAULT 'design'
CHECK (status IN ('design', 'planning', 'brewing', 'fermenting', 'conditioning', 'packaging', 'complete'));
```

#### 2. Fermentation Readings Table
```sql
CREATE TABLE fermentation_readings (
  id UUID PRIMARY KEY,
  batch_id UUID REFERENCES batches(id),
  reading_date TIMESTAMP,
  gravity DECIMAL(5,3),
  temperature DECIMAL(4,1),
  ph DECIMAL(3,1),
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### 3. Batch State Transitions Table
```sql
CREATE TABLE batch_state_history (
  id UUID PRIMARY KEY,
  batch_id UUID REFERENCES batches(id),
  from_status VARCHAR(20),
  to_status VARCHAR(20),
  transitioned_at TIMESTAMP DEFAULT NOW(),
  notes TEXT
);
```

### API Endpoints Needed

#### Batch Status Management
- `PUT /batches/{id}/status` - Update batch status with validation
- `GET /batches/{id}/history` - Get status transition history
- `POST /batches/{id}/advance` - Auto-advance to next stage

#### Fermentation Tracking
- `POST /batches/{id}/readings` - Add fermentation reading
- `GET /batches/{id}/readings` - List all readings
- `GET /batches/{id}/fermentation-chart` - Get chart data
- `DELETE /readings/{id}` - Remove reading

#### Inventory Integration
- `POST /batches/{id}/allocate-inventory` - Reserve ingredients
- `POST /batches/{id}/consume-inventory` - Deduct from stock
- `GET /recipes/{id}/availability` - Check ingredient availability
- `POST /batches/{id}/rollback-inventory` - Undo deduction

### Business Logic Required

#### State Machine
```typescript
const stateTransitions = {
  design: ['planning'],
  planning: ['brewing', 'design'],
  brewing: ['fermenting'],
  fermenting: ['conditioning', 'packaging'],
  conditioning: ['packaging'],
  packaging: ['complete'],
  complete: []
}
```

#### Auto-Progression Rules
- Fermenting → Conditioning: When gravity stable for 3 days
- Conditioning → Packaging: After minimum conditioning days
- Packaging → Complete: After packaging date + carbonation days

---

## 📊 Implementation Status

### Frontend (75% Complete)
- ✅ Calculator composable
- ✅ Inventory dashboard
- ✅ Batch status timeline (UI only)
- ✅ Recipe calculator widget
- ✅ Alert & Badge components
- ⚠️ Recipe editor (needs enhancement)
- ❌ Fermentation chart visualization
- ❌ Inventory allocation UI

### Backend (10% Complete)
- ✅ Basic batch CRUD
- ✅ Recipe CRUD
- ✅ Inventory CRUD
- ❌ Batch status workflow
- ❌ Fermentation tracking
- ❌ Inventory integration
- ❌ State machine logic
- ❌ Auto-progression

### Integration (5% Complete)
- ⚠️ Components use mock data
- ❌ No real-time updates
- ❌ No state persistence
- ❌ No inventory deduction

---

## 🎯 Next Steps

### Immediate (Can Do Without Backend)
1. ✅ Create calculator composable (DONE)
2. ✅ Build inventory dashboard (DONE)
3. ✅ Create batch timeline component (DONE)
4. ✅ Build recipe calculator widget (DONE)
5. ⏭️ Enhance recipe editor with live calculations
6. ⏭️ Add cost tracking to inventory UI
7. ⏭️ Create fermentation chart placeholder

### Short Term (Requires Backend)
1. Implement batch status endpoints
2. Add fermentation readings table
3. Create state machine logic
4. Build inventory allocation system
5. Add automatic state transitions

### Medium Term
1. Fermentation monitoring with charts
2. Packaging workflow
3. Quality control forms
4. Analytics dashboard
5. Recipe scaling tools

---

## 💡 Usage Guide

### For Developers

#### Adding a New Calculator
```typescript
// In useCalculators.ts
function calculateNewMetric(param1: number, param2: number) {
  const result = // calculation logic
  return {
    value: result,
    formatted: `${result.toFixed(2)} units`
  }
}
```

#### Using Batch Timeline
```vue
<script setup>
const batch = ref({
  id: '1',
  name: 'My IPA',
  status: 'fermenting', // design|planning|brewing|fermenting|conditioning|packaging|complete
  og: 1.060,
  fg: 1.012,
  days_in_fermentation: 7
})
</script>

<template>
  <BatchStatusTimeline :batch="batch" />
</template>
```

#### Integrating Calculator Widget
```vue
<script setup>
const recipe = ref({
  og: 1.055,
  fg: 1.012,
  batchSize: 20,
  grainWeight: 5.5,
  grainColor: 10,
  hopAdditions: [
    { alphaAcid: 12, weight: 30, boilTime: 60 }
  ],
  boilGravity: 1.055
})
</script>

<template>
  <RecipeCalculatorWidget v-bind="recipe" />
</template>
```

### For Brewers

#### Planning a Brew Day
1. Navigate to Tools → Calculators
2. Use Strike Water calculator for mash
3. Use IBU calculator for hop additions
4. Use Yeast Pitch Rate for proper pitching

#### Tracking a Batch
1. Create batch from recipe
2. Status automatically starts at "Design"
3. Progress through stages manually
4. Monitor timeline on batch detail page
5. View calculated stats in real-time

#### Managing Inventory
1. Check dashboard for low stock warnings
2. Use quick actions to add ingredients
3. View total stock across categories
4. Track amounts and costs (when implemented)

---

## 🔗 Related Documentation

- [COMPREHENSIVE_BREWING_TRACKER_ANALYSIS.md](../../documents/issues/COMPREHENSIVE_BREWING_TRACKER_ANALYSIS.md) - Full feature analysis
- [GITHUB_ISSUES_COMPREHENSIVE.md](../../documents/issues/GITHUB_ISSUES_COMPREHENSIVE.md) - Detailed issue list
- [IMPLEMENTATION_STATUS.md](../../IMPLEMENTATION_STATUS.md) - Overall project status

---

## 📝 Version History

- **1.0** (Nov 5, 2025) - Initial implementation
  - Calculator composable created
  - Inventory dashboard enhanced
  - Batch timeline component added
  - Recipe calculator widget created
  - Alert & Badge components added

---

**Status**: Frontend components ready, awaiting backend implementation for full workflow integration.
