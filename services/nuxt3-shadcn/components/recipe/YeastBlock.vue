<template>
  <div class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-card-foreground">Yeast</h3>
      <span class="text-sm text-muted-foreground">{{ yeasts.length }} strain{{ yeasts.length !== 1 ? 's' : '' }}</span>
    </div>

    <div class="space-y-3">
      <div 
        v-for="(yeast, index) in yeasts" 
        :key="index"
        class="flex items-center justify-between p-3 bg-muted/50 rounded-lg hover:bg-muted transition-colors"
      >
        <div class="flex-1">
          <div class="flex items-center space-x-3">
            <div class="font-medium text-card-foreground">
              {{ yeast.name || 'Unnamed Yeast' }}
            </div>
            <div v-if="yeast.type" class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
              {{ yeast.type }}
            </div>
            <div v-if="yeast.form" class="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full">
              {{ yeast.form }}
            </div>
          </div>
          
          <div class="mt-1 flex items-center space-x-4 text-sm text-muted-foreground">
            <span v-if="yeast.laboratory">{{ yeast.laboratory }}</span>
            <span v-if="yeast.product_id">{{ yeast.product_id }}</span>
            <span v-if="yeast.attenuation">{{ yeast.attenuation }}% attenuation</span>
          </div>
          
          <div v-if="yeast.min_temperature || yeast.max_temperature" class="mt-1 text-sm text-muted-foreground">
            <span v-if="yeast.min_temperature && yeast.max_temperature">
              Temperature: {{ yeast.min_temperature }}°C - {{ yeast.max_temperature }}°C
            </span>
            <span v-else-if="yeast.min_temperature">
              Min temp: {{ yeast.min_temperature }}°C
            </span>
            <span v-else-if="yeast.max_temperature">
              Max temp: {{ yeast.max_temperature }}°C
            </span>
          </div>
        </div>

        <div class="text-right">
          <div class="font-semibold text-card-foreground">
            {{ formatAmount(yeast.amount, yeast.display_amount) }}
          </div>
          <div v-if="yeast.add_to_secondary" class="text-xs text-orange-600">
            Add to secondary
          </div>
        </div>
      </div>
    </div>

    <!-- Yeast Details -->
    <div class="mt-4 pt-4 border-t border-border space-y-2">
      <div v-for="yeast in yeastsWithDetails" :key="yeast.name" class="text-sm">
        <div v-if="yeast.flocculation" class="flex justify-between">
          <span class="text-muted-foreground">Flocculation:</span>
          <span class="font-medium text-card-foreground">{{ yeast.flocculation }}</span>
        </div>
        <div v-if="yeast.max_reuse" class="flex justify-between">
          <span class="text-muted-foreground">Max Reuse:</span>
          <span class="font-medium text-card-foreground">{{ yeast.max_reuse }} times</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Yeast {
  name?: string
  type?: string
  form?: string
  laboratory?: string
  product_id?: string
  amount?: number
  display_amount?: string
  min_temperature?: number
  max_temperature?: number
  attenuation?: number
  flocculation?: string
  max_reuse?: number
  add_to_secondary?: boolean
}

interface Props {
  yeasts: Yeast[]
}

const props = defineProps<Props>()

// Filter yeasts that have additional details to show
const yeastsWithDetails = computed(() => {
  return props.yeasts.filter(yeast => 
    yeast.flocculation || yeast.max_reuse
  )
})

// Format amount display
const formatAmount = (amount?: number, displayAmount?: string) => {
  if (displayAmount) return displayAmount
  if (amount) return `${amount.toFixed(2)} g`
  return '1 pkg'
}
</script>