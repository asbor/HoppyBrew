<template>
  <div class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-card-foreground">Fermentables</h3>
      <span class="text-sm text-muted-foreground">{{ fermentables.length }} item{{ fermentables.length !== 1 ? 's' : '' }}</span>
    </div>

    <div class="space-y-3">
      <div 
        v-for="(fermentable, index) in fermentables" 
        :key="index"
        class="flex items-center justify-between p-3 bg-muted/50 rounded-lg hover:bg-muted transition-colors"
      >
        <div class="flex-1">
          <div class="flex items-center space-x-3">
            <div class="font-medium text-card-foreground">
              {{ fermentable.name || 'Unnamed Fermentable' }}
            </div>
            <div v-if="fermentable.type" class="px-2 py-1 bg-amber-100 text-amber-800 text-xs rounded-full">
              {{ fermentable.type }}
            </div>
          </div>
          
          <div class="mt-1 flex items-center space-x-4 text-sm text-muted-foreground">
            <span v-if="fermentable.origin">{{ fermentable.origin }}</span>
            <span v-if="fermentable.yield_">{{ fermentable.yield_ }}% yield</span>
            <span v-if="fermentable.color">{{ fermentable.color }} EBC</span>
          </div>
        </div>

        <div class="text-right">
          <div class="font-semibold text-card-foreground">
            {{ formatAmount(fermentable.amount, fermentable.display_amount) }}
          </div>
          <div v-if="fermentable.percentage" class="text-sm text-muted-foreground">
            {{ fermentable.percentage.toFixed(1) }}%
          </div>
        </div>
      </div>
    </div>

    <!-- Summary -->
    <div class="mt-4 pt-4 border-t border-border">
      <div class="flex justify-between text-sm">
        <span class="text-muted-foreground">Total Fermentables:</span>
        <span class="font-medium text-card-foreground">{{ totalAmount.toFixed(2) }} kg</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Fermentable {
  name?: string
  type?: string
  origin?: string
  amount?: number
  display_amount?: string
  yield_?: number
  color?: number
  percentage?: number
}

interface Props {
  fermentables: Fermentable[]
}

const props = defineProps<Props>()

// Calculate total amount
const totalAmount = computed(() => {
  return props.fermentables.reduce((total, fermentable) => {
    return total + (fermentable.amount || 0)
  }, 0)
})

// Format amount display
const formatAmount = (amount?: number, displayAmount?: string) => {
  if (displayAmount) return displayAmount
  if (amount) return `${amount.toFixed(2)} kg`
  return '0 kg'
}
</script>