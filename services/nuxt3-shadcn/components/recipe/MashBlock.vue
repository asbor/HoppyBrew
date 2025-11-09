<template>
  <div v-if="mash" class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-card-foreground mb-4">Mash Profile</h3>
    
    <div class="p-4 bg-orange-100/20 dark:bg-orange-900/20 rounded-lg">
      <h4 class="font-medium text-orange-900 dark:text-orange-200 mb-3">{{ mash.name || 'Mash Schedule' }}</h4>
      
      <!-- Mash Steps -->
      <div v-if="mash.steps && mash.steps.length > 0" class="space-y-3">
        <div 
          v-for="(step, index) in mash.steps" 
          :key="index"
          class="flex items-center justify-between p-3 bg-card rounded border border-border"
        >
          <div class="flex-1">
            <div class="flex items-center space-x-3">
              <div class="text-sm font-medium text-orange-800 dark:text-orange-300">
                Step {{ index + 1 }}: {{ step.name || step.type || 'Mash Step' }}
              </div>
              <div v-if="step.type" class="px-2 py-1 bg-orange-100 dark:bg-orange-900 text-orange-700 dark:text-orange-300 text-xs rounded">
                {{ step.type }}
              </div>
            </div>
            
            <div class="mt-1 flex items-center space-x-4 text-sm text-muted-foreground">
              <span v-if="step.step_temp">{{ step.step_temp }}°C</span>
              <span v-if="step.step_time">{{ step.step_time }} min</span>
              <span v-if="step.infuse_amount">{{ step.infuse_amount }}L infusion</span>
            </div>
          </div>

          <div v-if="step.description" class="text-xs text-muted-foreground ml-4 max-w-xs">
            {{ step.description }}
          </div>
        </div>
      </div>

      <!-- Mash Summary -->
      <div v-else class="text-sm text-muted-foreground">
        <div v-if="mash.grain_temp">
          <span class="font-medium text-card-foreground">Grain Temperature:</span> {{ mash.grain_temp }}°C
        </div>
        <div v-if="mash.mash_ph">
          <span class="font-medium text-card-foreground">Mash pH:</span> {{ mash.mash_ph.toFixed(2) }}
        </div>
        <div v-if="mash.sparge_temp">
          <span class="font-medium text-card-foreground">Sparge Temperature:</span> {{ mash.sparge_temp }}°C
        </div>
      </div>

      <!-- Mash Notes -->
      <div v-if="mash.notes" class="mt-4 pt-3 border-t border-orange-200 dark:border-orange-800">
        <span class="text-orange-700 dark:text-orange-300 font-medium">Notes:</span>
        <p class="mt-1 text-muted-foreground text-sm leading-relaxed">{{ mash.notes }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface MashStep {
  name?: string
  type?: string
  step_temp?: number
  step_time?: number
  infuse_amount?: number
  description?: string
}

interface MashProfile {
  name?: string
  grain_temp?: number
  mash_ph?: number
  sparge_temp?: number
  notes?: string
  steps?: MashStep[]
}

interface Props {
  mash: MashProfile
}

defineProps<Props>()
</script>