<template>
  <div v-if="hasFermentationData" class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-card-foreground mb-4">Fermentation Schedule</h3>
    
    <div class="space-y-4">
      <!-- Primary Fermentation -->
      <div v-if="recipe.primary_age || recipe.primary_temp" class="p-4 bg-blue-100/20 dark:bg-blue-900/20 rounded-lg">
        <div class="flex items-center justify-between mb-2">
          <h4 class="font-medium text-blue-900 dark:text-blue-200">Primary Fermentation</h4>
          <div class="text-sm text-blue-700 dark:text-blue-300">Stage 1</div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div v-if="recipe.primary_age">
            <span class="text-blue-700 dark:text-blue-300">Duration:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ recipe.primary_age }} days</span>
          </div>
          <div v-if="recipe.primary_temp || recipe.display_primary_temp">
            <span class="text-blue-700 dark:text-blue-300">Temperature:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ recipe.display_primary_temp || `${recipe.primary_temp}°C` }}</span>
          </div>
        </div>
      </div>

      <!-- Secondary Fermentation -->
      <div v-if="recipe.secondary_age || recipe.secondary_temp" class="p-4 bg-purple-100/20 dark:bg-purple-900/20 rounded-lg">
        <div class="flex items-center justify-between mb-2">
          <h4 class="font-medium text-purple-900 dark:text-purple-200">Secondary Fermentation</h4>
          <div class="text-sm text-purple-700 dark:text-purple-300">Stage 2</div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div v-if="recipe.secondary_age">
            <span class="text-purple-700 dark:text-purple-300">Duration:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ recipe.secondary_age }} days</span>
          </div>
          <div v-if="recipe.secondary_temp || recipe.display_secondary_temp">
            <span class="text-purple-700 dark:text-purple-300">Temperature:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ recipe.display_secondary_temp || `${recipe.secondary_temp}°C` }}</span>
          </div>
        </div>
      </div>

      <!-- Tertiary/Aging -->
      <div v-if="recipe.tertiary_age || recipe.age" class="p-4 bg-amber-100/20 dark:bg-amber-900/20 rounded-lg">
        <div class="flex items-center justify-between mb-2">
          <h4 class="font-medium text-amber-900 dark:text-amber-200">Conditioning/Aging</h4>
          <div class="text-sm text-amber-700 dark:text-amber-300">Final Stage</div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div v-if="recipe.tertiary_age || recipe.age">
            <span class="text-amber-700 dark:text-amber-300">Duration:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ recipe.tertiary_age || recipe.age }} days</span>
          </div>
          <div v-if="recipe.age_temp || recipe.display_age_temp || recipe.display_tertiary_temp">
            <span class="text-amber-700 dark:text-amber-300">Temperature:</span>
            <span class="ml-2 font-medium text-card-foreground">
              {{ recipe.display_tertiary_temp || recipe.display_age_temp || `${recipe.age_temp}°C` }}
            </span>
          </div>
        </div>
      </div>

      <!-- Summary -->
      <div v-if="totalDuration > 0" class="p-3 bg-muted/50 rounded-lg">
        <div class="flex justify-between text-sm">
          <span class="text-muted-foreground">Total Fermentation Time:</span>
          <span class="font-medium text-card-foreground">{{ totalDuration }} days</span>
        </div>
        <div v-if="recipe.fermentation_stages" class="flex justify-between text-sm mt-1">
          <span class="text-muted-foreground">Number of Stages:</span>
          <span class="font-medium text-card-foreground">{{ recipe.fermentation_stages }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Recipe {
  primary_age?: number
  primary_temp?: number
  display_primary_temp?: string
  secondary_age?: number
  secondary_temp?: number
  display_secondary_temp?: string
  tertiary_age?: number
  age?: number
  age_temp?: number
  display_age_temp?: string
  display_tertiary_temp?: string
  fermentation_stages?: number
}

interface Props {
  recipe: Recipe
}

const props = defineProps<Props>()

// Check if we have any fermentation data
const hasFermentationData = computed(() => {
  return props.recipe.primary_age || props.recipe.primary_temp || 
         props.recipe.secondary_age || props.recipe.secondary_temp ||
         props.recipe.tertiary_age || props.recipe.age
})

// Calculate total duration
const totalDuration = computed(() => {
  let total = 0
  if (props.recipe.primary_age) total += props.recipe.primary_age
  if (props.recipe.secondary_age) total += props.recipe.secondary_age
  if (props.recipe.tertiary_age) total += props.recipe.tertiary_age
  if (props.recipe.age && !props.recipe.tertiary_age) total += props.recipe.age
  return total
})
</script>