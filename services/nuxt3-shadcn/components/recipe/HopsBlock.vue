<template>
  <div class="bg-white rounded-lg border p-6 shadow-sm">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Hops</h3>
      <span class="text-sm text-gray-500">{{ hops.length }} addition{{ hops.length !== 1 ? 's' : '' }}</span>
    </div>

    <div class="space-y-3">
      <div 
        v-for="(hop, index) in sortedHops" 
        :key="index"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
      >
        <div class="flex-1">
          <div class="flex items-center space-x-3">
            <div class="font-medium text-gray-900">
              {{ hop.name || 'Unnamed Hop' }}
            </div>
            <div v-if="hop.type" class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
              {{ hop.type }}
            </div>
            <div v-if="hop.form" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
              {{ hop.form }}
            </div>
          </div>
          
          <div class="mt-1 flex items-center space-x-4 text-sm text-gray-500">
            <span v-if="hop.origin">{{ hop.origin }}</span>
            <span v-if="hop.alpha">{{ hop.alpha }}% α-acid</span>
            <span v-if="hop.use" class="font-medium">{{ hop.use }}</span>
            <span v-if="hop.time">{{ formatTime(hop.time, hop.display_time) }}</span>
          </div>
        </div>

        <div class="text-right">
          <div class="font-semibold text-gray-900">
            {{ formatAmount(hop.amount, hop.display_amount) }}
          </div>
          <div v-if="hop.ibu_contribution" class="text-sm text-gray-500">
            {{ hop.ibu_contribution.toFixed(1) }} IBU
          </div>
        </div>
      </div>
    </div>

    <!-- Summary -->
    <div class="mt-4 pt-4 border-t border-gray-200">
      <div class="flex justify-between text-sm">
        <span class="text-gray-500">Total Hops:</span>
        <span class="font-medium">{{ totalAmount.toFixed(1) }} g</span>
      </div>
      <div v-if="totalIbu > 0" class="flex justify-between text-sm mt-1">
        <span class="text-gray-500">Total IBU:</span>
        <span class="font-medium">{{ totalIbu.toFixed(1) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Hop {
  name?: string
  type?: string
  origin?: string
  amount?: number
  display_amount?: string
  alpha?: number
  form?: string
  use?: string
  time?: number
  display_time?: string
  ibu_contribution?: number
}

interface Props {
  hops: Hop[]
}

const props = defineProps<Props>()

// Sort hops by time (boil time descending for traditional order)
const sortedHops = computed(() => {
  return [...props.hops].sort((a, b) => {
    // Sort by time, with longer boil times first
    const timeA = a.time || 0
    const timeB = b.time || 0
    return timeB - timeA
  })
})

// Calculate total amount
const totalAmount = computed(() => {
  return props.hops.reduce((total, hop) => {
    return total + (hop.amount || 0)
  }, 0)
})

// Calculate total IBU (if provided)
const totalIbu = computed(() => {
  return props.hops.reduce((total, hop) => {
    return total + (hop.ibu_contribution || 0)
  }, 0)
})

// Format amount display
const formatAmount = (amount?: number, displayAmount?: string) => {
  if (displayAmount) return displayAmount
  if (amount) return `${amount.toFixed(1)} g`
  return '0 g'
}

// Format time display
const formatTime = (time?: number, displayTime?: string) => {
  if (displayTime) return displayTime
  if (time !== undefined) {
    if (time === 0) return 'Flameout'
    return `${time} min`
  }
  return ''
}
</script>