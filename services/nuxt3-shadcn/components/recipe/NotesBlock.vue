<template>
  <div class="bg-white rounded-lg border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Notes & Information</h3>
    
    <div class="space-y-6">
      <!-- Main Notes -->
      <div v-if="recipe.notes">
        <h4 class="text-sm font-medium text-gray-700 uppercase tracking-wide mb-2">Brewing Notes</h4>
        <div class="p-4 bg-gray-50 rounded-lg">
          <p class="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">{{ recipe.notes }}</p>
        </div>
      </div>

      <!-- Taste Notes -->
      <div v-if="recipe.taste_notes">
        <h4 class="text-sm font-medium text-gray-700 uppercase tracking-wide mb-2">Tasting Notes</h4>
        <div class="p-4 bg-amber-50 rounded-lg">
          <p class="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">{{ recipe.taste_notes }}</p>
          <div v-if="recipe.taste_rating" class="mt-2 flex items-center">
            <span class="text-sm text-gray-500 mr-2">Rating:</span>
            <div class="flex items-center">
              <div class="flex">
                <Star 
                  v-for="i in 5" 
                  :key="i"
                  class="h-4 w-4"
                  :class="i <= (recipe.taste_rating || 0) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                />
              </div>
              <span class="ml-2 text-sm font-medium">{{ recipe.taste_rating }}/5</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Carbonation Information -->
      <div v-if="recipe.carbonation_used">
        <h4 class="text-sm font-medium text-gray-700 uppercase tracking-wide mb-2">Carbonation</h4>
        <div class="p-3 bg-blue-50 rounded-lg">
          <p class="text-sm text-gray-700">{{ recipe.carbonation_used }}</p>
        </div>
      </div>

      <!-- Recipe Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Gravity Information -->
        <div v-if="hasGravityInfo" class="space-y-2">
          <h4 class="text-sm font-medium text-gray-700 uppercase tracking-wide">Gravity</h4>
          <div class="p-3 bg-green-50 rounded-lg space-y-1">
            <div v-if="recipe.est_og || recipe.og" class="flex justify-between text-sm">
              <span class="text-gray-600">Original Gravity:</span>
              <span class="font-medium">
                {{ recipe.display_og || formatGravity(recipe.og || recipe.est_og) }}
              </span>
            </div>
            <div v-if="recipe.est_fg || recipe.fg" class="flex justify-between text-sm">
              <span class="text-gray-600">Final Gravity:</span>
              <span class="font-medium">
                {{ recipe.display_fg || formatGravity(recipe.fg || recipe.est_fg) }}
              </span>
            </div>
            <div v-if="attenuation" class="flex justify-between text-sm">
              <span class="text-gray-600">Attenuation:</span>
              <span class="font-medium">{{ attenuation.toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <!-- Fermentation Information -->
        <div v-if="hasFermentationInfo" class="space-y-2">
          <h4 class="text-sm font-medium text-gray-700 uppercase tracking-wide">Fermentation</h4>
          <div class="p-3 bg-purple-50 rounded-lg space-y-1">
            <div v-if="recipe.fermentation_stages" class="flex justify-between text-sm">
              <span class="text-gray-600">Stages:</span>
              <span class="font-medium">{{ recipe.fermentation_stages }}</span>
            </div>
            <div v-if="recipe.primary_age" class="flex justify-between text-sm">
              <span class="text-gray-600">Primary:</span>
              <span class="font-medium">
                {{ recipe.primary_age }} days
                <span v-if="recipe.primary_temp || recipe.display_primary_temp">
                  @ {{ recipe.display_primary_temp || `${recipe.primary_temp}°C` }}
                </span>
              </span>
            </div>
            <div v-if="recipe.secondary_age" class="flex justify-between text-sm">
              <span class="text-gray-600">Secondary:</span>
              <span class="font-medium">
                {{ recipe.secondary_age }} days
                <span v-if="recipe.secondary_temp || recipe.display_secondary_temp">
                  @ {{ recipe.display_secondary_temp || `${recipe.secondary_temp}°C` }}
                </span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Star } from 'lucide-vue-next'

interface Recipe {
  notes?: string
  taste_notes?: string
  taste_rating?: number
  carbonation_used?: string
  est_og?: number
  og?: number
  est_fg?: number
  fg?: number
  display_og?: string
  display_fg?: string
  fermentation_stages?: number
  primary_age?: number
  primary_temp?: number
  display_primary_temp?: string
  secondary_age?: number
  secondary_temp?: number
  display_secondary_temp?: string
}

interface Props {
  recipe: Recipe
}

const props = defineProps<Props>()

// Check if we have gravity information
const hasGravityInfo = computed(() => {
  return props.recipe.est_og || props.recipe.og || props.recipe.est_fg || props.recipe.fg
})

// Check if we have fermentation information
const hasFermentationInfo = computed(() => {
  return props.recipe.fermentation_stages || props.recipe.primary_age || props.recipe.secondary_age
})

// Calculate apparent attenuation
const attenuation = computed(() => {
  const og = props.recipe.og || props.recipe.est_og
  const fg = props.recipe.fg || props.recipe.est_fg
  
  if (og && fg && og > fg) {
    return ((og - fg) / (og - 1.000)) * 100
  }
  return null
})

// Format gravity values
const formatGravity = (gravity?: number) => {
  if (!gravity) return ''
  return gravity.toFixed(3)
}
</script>