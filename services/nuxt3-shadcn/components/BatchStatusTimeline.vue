<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Badge } from '~/components/ui/badge'

export interface BatchStatus {
  id: string
  name: string
  status: 'design' | 'planning' | 'brewing' | 'fermenting' | 'conditioning' | 'packaging' | 'complete'
  created_at?: string
  brew_date?: string
  og?: number
  fg?: number
  target_og?: number
  target_fg?: number
  days_in_fermentation?: number
}

const props = defineProps<{
  batch: BatchStatus
}>()

// Status workflow steps
const statusSteps = [
  { key: 'design', label: 'Design', icon: 'mdi:pencil-ruler' },
  { key: 'planning', label: 'Planning', icon: 'mdi:calendar-check' },
  { key: 'brewing', label: 'Brewing', icon: 'mdi:kettle' },
  { key: 'fermenting', label: 'Fermenting', icon: 'mdi:chart-bubble' },
  { key: 'conditioning', label: 'Conditioning', icon: 'mdi:snowflake' },
  { key: 'packaging', label: 'Packaging', icon: 'mdi:bottle-wine' },
  { key: 'complete', label: 'Complete', icon: 'mdi:check-circle' },
]

const currentStepIndex = computed(() => {
  return statusSteps.findIndex(step => step.key === props.batch.status)
})

const statusColor = computed(() => {
  const colors: Record<string, string> = {
    design: 'bg-gray-400',
    planning: 'bg-blue-400',
    brewing: 'bg-orange-500',
    fermenting: 'bg-purple-500',
    conditioning: 'bg-cyan-500',
    packaging: 'bg-green-500',
    complete: 'bg-green-700',
  }
  return colors[props.batch.status] || 'bg-gray-400'
})

const statusBadgeVariant = computed(() => {
  const variants: Record<string, 'default' | 'secondary' | 'warning' | 'outline'> = {
    design: 'outline',
    planning: 'secondary',
    brewing: 'warning',
    fermenting: 'secondary',
    conditioning: 'secondary',
    packaging: 'secondary',
    complete: 'default',
  }
  return variants[props.batch.status] || 'outline'
})

function isStepComplete(stepIndex: number): boolean {
  return stepIndex < currentStepIndex.value
}

function isStepCurrent(stepIndex: number): boolean {
  return stepIndex === currentStepIndex.value
}

function getStepClasses(index: number): string {
  if (isStepComplete(index)) {
    return `${statusColor.value} border-transparent text-white`
  }
  if (isStepCurrent(index)) {
    return `${statusColor.value} border-transparent text-white ring-4 ring-offset-2`
  }
  return 'border-gray-300 text-gray-400'
}

function getStepLabelClasses(index: number): string {
  if (isStepCurrent(index)) {
    return 'text-gray-900 font-semibold'
  }
  if (isStepComplete(index)) {
    return 'text-gray-700'
  }
  return 'text-gray-400'
}

function formatDate(dateString?: string): string {
  if (!dateString) return 'Not set'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex items-center justify-between">
        <div>
          <CardTitle>{{ batch.name }}</CardTitle>
          <CardDescription>Batch Status Timeline</CardDescription>
        </div>
        <Badge :variant="statusBadgeVariant">
          {{ batch.status.charAt(0).toUpperCase() + batch.status.slice(1) }}
        </Badge>
      </div>
    </CardHeader>
    <CardContent class="space-y-6">
      <!-- Timeline -->
      <div class="relative">
        <!-- Progress Line -->
        <div class="absolute top-6 left-0 right-0 h-0.5 bg-gray-200">
          <div 
            :class="statusColor"
            class="h-full transition-all duration-500"
            :style="{ width: `${(currentStepIndex / (statusSteps.length - 1)) * 100}%` }"
          ></div>
        </div>

        <!-- Status Steps -->
        <div class="relative grid grid-cols-7 gap-2">
          <div 
            v-for="(step, index) in statusSteps"
            :key="step.key"
            class="flex flex-col items-center"
          >
            <!-- Step Circle -->
            <div 
              :class="[
                'w-12 h-12 rounded-full flex items-center justify-center border-2 bg-white transition-all',
                getStepClasses(index)
              ]"
            >
              <Icon 
                :name="isStepComplete(index) ? 'mdi:check' : step.icon"
                :size="isStepCurrent(index) ? '28' : '24'"
              />
            </div>
            
            <!-- Step Label -->
            <span 
              :class="[
                'mt-2 text-xs text-center font-medium',
                getStepLabelClasses(index)
              ]"
            >
              {{ step.label }}
            </span>
          </div>
        </div>
      </div>

      <!-- Batch Details -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t">
        <div>
          <p class="text-sm text-muted-foreground">Created</p>
          <p class="font-medium">{{ formatDate(batch.created_at) }}</p>
        </div>
        <div>
          <p class="text-sm text-muted-foreground">Brew Date</p>
          <p class="font-medium">{{ formatDate(batch.brew_date) }}</p>
        </div>
        <div v-if="batch.og">
          <p class="text-sm text-muted-foreground">OG</p>
          <p class="font-medium">{{ batch.og.toFixed(3) }}</p>
        </div>
        <div v-if="batch.fg">
          <p class="text-sm text-muted-foreground">FG</p>
          <p class="font-medium">{{ batch.fg.toFixed(3) }}</p>
        </div>
        <div v-if="batch.days_in_fermentation">
          <p class="text-sm text-muted-foreground">Days Fermenting</p>
          <p class="font-medium">{{ batch.days_in_fermentation }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
