<template>
  <div class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <h2 class="text-xl font-semibold text-card-foreground mb-4">Recipe Overview</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Basic Information -->
      <div class="space-y-3">
        <h3 class="text-sm font-medium text-card-foreground uppercase tracking-wide">Basic Info</h3>
        <div class="space-y-2">
          <div v-if="recipe.brewer">
            <span class="text-sm text-muted-foreground">Brewer:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.brewer }}</span>
          </div>
          <div v-if="recipe.asst_brewer">
            <span class="text-sm text-muted-foreground">Assistant Brewer:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.asst_brewer }}</span>
          </div>
          <div v-if="recipe.version">
            <span class="text-sm text-muted-foreground">Version:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.version }}</span>
          </div>
        </div>
      </div>

      <!-- Batch Information -->
      <div class="space-y-3">
        <h3 class="text-sm font-medium text-card-foreground uppercase tracking-wide">Batch Info</h3>
        <div class="space-y-2">
          <div v-if="recipe.batch_size">
            <span class="text-sm text-muted-foreground">Batch Size:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">
              {{ recipe.display_batch_size || `${recipe.batch_size} L` }}
            </span>
          </div>
          <div v-if="recipe.boil_size">
            <span class="text-sm text-muted-foreground">Boil Size:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">
              {{ recipe.display_boil_size || `${recipe.boil_size} L` }}
            </span>
          </div>
          <div v-if="recipe.boil_time">
            <span class="text-sm text-muted-foreground">Boil Time:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.boil_time }} min</span>
          </div>
          <div v-if="recipe.efficiency">
            <span class="text-sm text-muted-foreground">Efficiency:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.efficiency }}%</span>
          </div>
        </div>
      </div>

      <!-- Calculated Values -->
      <div class="space-y-3">
        <h3 class="text-sm font-medium text-card-foreground uppercase tracking-wide">Calculated</h3>
        <div class="space-y-2">
          <div v-if="recipe.est_abv || recipe.abv">
            <span class="text-sm text-muted-foreground">ABV:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">
              {{ (recipe.abv || recipe.est_abv)?.toFixed(1) }}%
            </span>
          </div>
          <div v-if="recipe.ibu">
            <span class="text-sm text-muted-foreground">IBU:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.ibu.toFixed(0) }}</span>
          </div>
          <div v-if="recipe.est_color">
            <span class="text-sm text-muted-foreground">Color:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.est_color.toFixed(0) }} SRM</span>
          </div>
          <div v-if="recipe.calories">
            <span class="text-sm text-muted-foreground">Calories:</span>
            <span class="ml-2 text-sm font-medium text-card-foreground">{{ recipe.calories.toFixed(0) }} per L</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Description/Notes Preview -->
    <div v-if="recipe.notes" class="mt-6 pt-4 border-t border-border">
      <h3 class="text-sm font-medium text-card-foreground uppercase tracking-wide mb-2">Description</h3>
      <p class="text-sm text-muted-foreground leading-relaxed">{{ recipe.notes }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Recipe } from '@/composables/useRecipes'

interface Props {
  recipe: Recipe
}

defineProps<Props>()
</script>