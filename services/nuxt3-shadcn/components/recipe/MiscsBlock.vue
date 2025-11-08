<template>
  <div class="bg-white rounded-lg border p-6 shadow-sm">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Miscellaneous</h3>
      <span class="text-sm text-gray-500">{{ miscs.length }} item{{ miscs.length !== 1 ? 's' : '' }}</span>
    </div>

    <div class="space-y-3">
      <div 
        v-for="(misc, index) in sortedMiscs" 
        :key="index"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
      >
        <div class="flex-1">
          <div class="flex items-center space-x-3">
            <div class="font-medium text-gray-900">
              {{ misc.name || 'Unnamed Addition' }}
            </div>
            <div v-if="misc.type" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
              {{ misc.type }}
            </div>
          </div>
          
          <div class="mt-1 flex items-center space-x-4 text-sm text-gray-500">
            <span v-if="misc.use" class="font-medium">{{ misc.use }}</span>
            <span v-if="misc.time">{{ formatTime(misc.time, misc.display_time) }}</span>
            <span v-if="misc.amount_is_weight === false">Volume</span>
            <span v-else-if="misc.amount_is_weight === true">Weight</span>
          </div>
          
          <div v-if="misc.use_for" class="mt-1 text-sm text-gray-600">
            {{ misc.use_for }}
          </div>
        </div>

        <div class="text-right">
          <div class="font-semibold text-gray-900">
            {{ formatAmount(misc.amount, misc.display_amount, misc.amount_is_weight) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Notes for miscs with descriptions -->
    <div v-if="miscsWithNotes.length > 0" class="mt-4 pt-4 border-t border-gray-200 space-y-2">
      <div v-for="misc in miscsWithNotes" :key="misc.name" class="text-sm">
        <div class="font-medium text-gray-700">{{ misc.name }}:</div>
        <div class="text-gray-600 ml-2">{{ misc.notes || misc.use_for }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Misc {
  name?: string
  type?: string
  use?: string
  time?: number
  display_time?: string
  amount?: number
  display_amount?: string
  amount_is_weight?: boolean
  use_for?: string
  notes?: string
}

interface Props {
  miscs: Misc[]
}

const props = defineProps<Props>()

// Sort miscs by use and time
const sortedMiscs = computed(() => {
  return [...props.miscs].sort((a, b) => {
    // Sort by use first (Boil, Fermentation, etc.), then by time
    const useOrder = { 'Boil': 1, 'Mash': 0, 'Fermentation': 2, 'Primary': 3, 'Secondary': 4 }
    const useA = useOrder[a.use as keyof typeof useOrder] ?? 5
    const useB = useOrder[b.use as keyof typeof useOrder] ?? 5
    
    if (useA !== useB) return useA - useB
    
    // Then by time (longer times first for boil additions)
    const timeA = a.time || 0
    const timeB = b.time || 0
    return timeB - timeA
  })
})

// Filter miscs that have notes or use descriptions
const miscsWithNotes = computed(() => {
  return props.miscs.filter(misc => misc.notes || misc.use_for)
})

// Format amount display
const formatAmount = (amount?: number, displayAmount?: string, isWeight?: boolean) => {
  if (displayAmount) return displayAmount
  if (amount) {
    const unit = isWeight ? 'g' : 'ml'
    return `${amount.toFixed(isWeight ? 1 : 0)} ${unit}`
  }
  return '1 item'
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