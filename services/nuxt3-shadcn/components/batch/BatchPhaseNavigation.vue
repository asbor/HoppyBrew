<template>
  <div class="w-full">
    <!-- Phase Timeline -->
    <div class="relative">
      <div class="flex justify-between mb-8">
        <div
v-for="(phase, index) in phases" :key="phase.key" class="flex flex-col items-center relative z-10"
          :class="{ 'cursor-pointer': isPhaseAccessible(phase.key) }"
          @click="isPhaseAccessible(phase.key) && $emit('phase-change', phase.key)">
          <!-- Phase Icon -->
          <div
class="w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all duration-300"
            :class="getPhaseIconClass(phase.key)">
            <Icon :name="phase.icon" class="h-6 w-6" :class="getPhaseIconColor(phase.key)" />
          </div>

          <!-- Phase Label -->
          <div class="mt-2 text-center">
            <p class="text-sm font-medium transition-colors duration-300" :class="getPhaseTextClass(phase.key)">
              {{ phase.label }}
            </p>
            <p v-if="getPhaseDate(phase.key)" class="text-xs text-muted-foreground mt-1">
              {{ formatDate(getPhaseDate(phase.key)) }}
            </p>
          </div>

          <!-- Connection Line -->
          <div
v-if="index < phases.length - 1"
            class="absolute top-6 left-full w-full h-0.5 transition-colors duration-300"
            :class="getConnectionLineClass(index)" style="transform: translateX(-50%)" />
        </div>
      </div>
    </div>

    <!-- Current Phase Details -->
    <Card class="mt-6">
      <CardContent class="p-6">
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Phase Info -->
          <div>
            <h3 class="text-lg font-semibold mb-2">{{ getCurrentPhase()?.label }}</h3>
            <p class="text-muted-foreground mb-4">{{ getCurrentPhase()?.description }}</p>

            <!-- Phase Stats -->
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Days in Phase:</span>
                <span class="text-sm font-medium">{{ getDaysInCurrentPhase() }}</span>
              </div>
              <div v-if="getNextPhase()" class="flex justify-between">
                <span class="text-sm text-muted-foreground">Next Phase:</span>
                <span class="text-sm font-medium">{{ getNextPhase()?.label }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Progress:</span>
                <span class="text-sm font-medium">{{ getProgressPercentage() }}%</span>
              </div>
            </div>
          </div>

          <!-- Phase Actions -->
          <div class="space-y-3">
            <h4 class="font-medium">Available Actions</h4>

            <!-- Phase-specific action buttons -->
            <template v-if="currentPhase === 'planning'">
              <Button class="w-full" @click="$emit('phase-change', 'brewing')">
                <Icon name="mdi:fire" class="mr-2 h-4 w-4" />
                Start Brew Day
              </Button>
            </template>

            <template v-else-if="currentPhase === 'brewing'">
              <Button class="w-full" @click="$emit('phase-change', 'fermenting')">
                <Icon name="mdi:flask" class="mr-2 h-4 w-4" />
                Start Fermentation
              </Button>
            </template>

            <template v-else-if="currentPhase === 'fermenting'">
              <Button class="w-full" @click="$emit('phase-change', 'conditioning')">
                <Icon name="mdi:snowflake" class="mr-2 h-4 w-4" />
                Start Conditioning
              </Button>
            </template>

            <template v-else-if="currentPhase === 'conditioning'">
              <Button class="w-full" @click="$emit('phase-change', 'packaging')">
                <Icon name="mdi:bottle-wine" class="mr-2 h-4 w-4" />
                Package Beer
              </Button>
            </template>

            <template v-else-if="currentPhase === 'packaging'">
              <Button class="w-full" @click="$emit('phase-change', 'complete')">
                <Icon name="mdi:check-circle" class="mr-2 h-4 w-4" />
                Mark Complete
              </Button>
            </template>

            <template v-else-if="currentPhase === 'complete'">
              <Button class="w-full" variant="outline" @click="$emit('phase-change', 'archived')">
                <Icon name="mdi:archive" class="mr-2 h-4 w-4" />
                Archive Batch
              </Button>
            </template>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '#components'

const props = defineProps<{
  currentPhase: string
  batchData?: any
}>()

const emit = defineEmits<{
  'phase-change': [phase: string]
}>()

const phases = [
  {
    key: 'planning',
    label: 'Planning',
    icon: 'mdi:clipboard-list',
    description: 'Recipe planning and preparation phase. Review ingredients and prepare for brew day.'
  },
  {
    key: 'brewing',
    label: 'Brewing',
    icon: 'mdi:fire',
    description: 'Active brewing process. Mashing, boiling, and wort preparation.'
  },
  {
    key: 'fermenting',
    label: 'Fermentation',
    icon: 'mdi:flask',
    description: 'Primary fermentation phase. Yeast converts sugars to alcohol and CO2.'
  },
  {
    key: 'conditioning',
    label: 'Conditioning',
    icon: 'mdi:snowflake',
    description: 'Cold conditioning phase for clarity and flavor maturation.'
  },
  {
    key: 'packaging',
    label: 'Packaging',
    icon: 'mdi:bottle-wine',
    description: 'Beer has been packaged into bottles or kegs.'
  },
  {
    key: 'complete',
    label: 'Complete',
    icon: 'mdi:check-circle',
    description: 'Brewing process completed. Ready for consumption.'
  }
]

const getCurrentPhaseIndex = () => {
  return phases.findIndex(phase => phase.key === props.currentPhase)
}

const getCurrentPhase = () => {
  return phases.find(phase => phase.key === props.currentPhase)
}

const getNextPhase = () => {
  const currentIndex = getCurrentPhaseIndex()
  if (currentIndex >= 0 && currentIndex < phases.length - 1) {
    return phases[currentIndex + 1]
  }
  return null
}

const isPhaseCompleted = (phaseKey: string) => {
  const currentIndex = getCurrentPhaseIndex()
  const phaseIndex = phases.findIndex(phase => phase.key === phaseKey)
  return phaseIndex < currentIndex
}

const isCurrentPhase = (phaseKey: string) => {
  return phaseKey === props.currentPhase
}

const isPhaseAccessible = (phaseKey: string) => {
  // Can only access completed phases or current phase
  return isPhaseCompleted(phaseKey) || isCurrentPhase(phaseKey)
}

const getPhaseIconClass = (phaseKey: string) => {
  if (isPhaseCompleted(phaseKey)) {
    return 'bg-green-500 border-green-500 text-white'
  } else if (isCurrentPhase(phaseKey)) {
    return 'bg-amber-500 border-amber-500 text-white ring-4 ring-amber-500/20'
  } else {
    return 'bg-gray-100 border-gray-300 text-gray-400'
  }
}

const getPhaseIconColor = (phaseKey: string) => {
  if (isPhaseCompleted(phaseKey) || isCurrentPhase(phaseKey)) {
    return 'text-white'
  } else {
    return 'text-gray-400'
  }
}

const getPhaseTextClass = (phaseKey: string) => {
  if (isPhaseCompleted(phaseKey)) {
    return 'text-green-600'
  } else if (isCurrentPhase(phaseKey)) {
    return 'text-amber-600'
  } else {
    return 'text-gray-400'
  }
}

const getConnectionLineClass = (index: number) => {
  const currentIndex = getCurrentPhaseIndex()
  if (index < currentIndex) {
    return 'bg-green-500'
  } else {
    return 'bg-gray-200'
  }
}

const getPhaseDate = (phaseKey: string) => {
  // This would come from batch data in a real implementation
  // For now, return mock dates based on phase
  const phaseDates: Record<string, string | null | undefined> = {
    planning: props.batchData?.created_at,
    brewing: props.batchData?.brew_date,
    fermenting: props.batchData?.fermentation_start_date,
    conditioning: props.batchData?.conditioning_start_date,
    packaging: props.batchData?.packaging_date,
    complete: props.batchData?.completion_date,
  }
  return phaseDates[phaseKey]
}

const formatDate = (date: string | Date | null) => {
  if (!date) return null
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const getDaysInCurrentPhase = () => {
  const phaseStartDate = getPhaseDate(props.currentPhase)
  if (!phaseStartDate) return 0

  const start = new Date(phaseStartDate)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - start.getTime())
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

const getProgressPercentage = () => {
  const currentIndex = getCurrentPhaseIndex()
  const totalPhases = phases.length
  return Math.round(((currentIndex + 1) / totalPhases) * 100)
}
</script>

<style scoped>
.relative .absolute {
  z-index: 1;
}
</style>
