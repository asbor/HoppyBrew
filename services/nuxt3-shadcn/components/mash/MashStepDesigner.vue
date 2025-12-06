<script setup lang="ts">
import { ref, computed } from 'vue'
import { TrashIcon, PlusIcon, ChevronUpIcon, ChevronDownIcon } from '@heroicons/vue/24/outline'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '~/components/ui/select'
import { Badge } from '~/components/ui/badge'
import { Alert, AlertDescription } from '~/components/ui/alert'

// Props
const props = defineProps<{
  modelValue: MashStep[]
}>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: MashStep[]]
}>()

// Types
interface MashStep {
  id?: number
  name: string
  type: string
  step_temp: number
  step_time: number
  ramp_time?: number
  description?: string
  infuse_amount?: number
  decoction_amt?: string
  water_grain_ratio?: string
}

// Local state
const steps = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:modelValue', value)
})

const editingStep = ref<MashStep | null>(null)
const showStepDialog = ref(false)

// Step types with descriptions
const stepTypes = [
  { value: 'Infusion', label: 'Infusion', description: 'Add hot water to raise temperature' },
  { value: 'Temperature', label: 'Temperature', description: 'Apply direct heat to raise temperature' },
  { value: 'Decoction', label: 'Decoction', description: 'Remove and boil portion of mash' }
]

// Validation
const validateStep = (step: MashStep) => {
  const errors: string[] = []
  
  if (!step.name || step.name.trim() === '') {
    errors.push('Step name is required')
  }
  
  if (!step.type) {
    errors.push('Step type is required')
  }
  
  if (step.step_temp < 0 || step.step_temp > 100) {
    errors.push('Temperature must be between 0°C and 100°C')
  }
  
  if (step.step_time < 0 || step.step_time > 300) {
    errors.push('Time must be between 0 and 300 minutes')
  }
  
  if (step.ramp_time && (step.ramp_time < 0 || step.ramp_time > 60)) {
    errors.push('Ramp time must be between 0 and 60 minutes')
  }
  
  return errors
}

// Calculate total mash time
const totalMashTime = computed(() => {
  return steps.value.reduce((total, step) => {
    return total + (step.step_time || 0) + (step.ramp_time || 0)
  }, 0)
})

// Add new step
const addNewStep = () => {
  editingStep.value = {
    name: '',
    type: 'Infusion',
    step_temp: 66,
    step_time: 60,
    ramp_time: 2,
    description: ''
  }
  showStepDialog.value = true
}

// Edit existing step
const editStep = (step: MashStep, index: number) => {
  editingStep.value = { ...step, index } as any
  showStepDialog.value = true
}

// Save step
const saveStep = () => {
  if (!editingStep.value) return
  
  const errors = validateStep(editingStep.value)
  if (errors.length > 0) {
    alert(errors.join('\n'))
    return
  }
  
  const index = (editingStep.value as any).index
  if (index !== undefined) {
    // Update existing step
    const newSteps = [...steps.value]
    newSteps[index] = { ...editingStep.value }
    delete (newSteps[index] as any).index
    steps.value = newSteps
  } else {
    // Add new step
    steps.value = [...steps.value, { ...editingStep.value }]
  }
  
  closeStepDialog()
}

// Delete step
const deleteStep = (index: number) => {
  if (confirm('Are you sure you want to delete this step?')) {
    steps.value = steps.value.filter((_, i) => i !== index)
  }
}

// Move step up
const moveStepUp = (index: number) => {
  if (index === 0) return
  const newSteps = [...steps.value]
  ;[newSteps[index - 1], newSteps[index]] = [newSteps[index], newSteps[index - 1]]
  steps.value = newSteps
}

// Move step down
const moveStepDown = (index: number) => {
  if (index === steps.value.length - 1) return
  const newSteps = [...steps.value]
  ;[newSteps[index], newSteps[index + 1]] = [newSteps[index + 1], newSteps[index]]
  steps.value = newSteps
}

// Close dialog
const closeStepDialog = () => {
  editingStep.value = null
  showStepDialog.value = false
}

// Get step type color
const getStepTypeColor = (type: string) => {
  switch (type) {
    case 'Infusion':
      return 'bg-blue-100 text-blue-800 border-blue-300'
    case 'Temperature':
      return 'bg-orange-100 text-orange-800 border-orange-300'
    case 'Decoction':
      return 'bg-purple-100 text-purple-800 border-purple-300'
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300'
  }
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header with summary -->
    <div class="flex justify-between items-center">
      <div>
        <h3 class="text-lg font-semibold">Mash Steps</h3>
        <p class="text-sm text-muted-foreground">
          {{ steps.length }} step{{ steps.length !== 1 ? 's' : '' }} • Total time: {{ totalMashTime }} minutes
        </p>
      </div>
      <Button size="sm" @click="addNewStep">
        <PlusIcon class="h-4 w-4 mr-2" />
        Add Step
      </Button>
    </div>

    <!-- Steps list -->
    <div v-if="steps.length === 0" class="text-center py-8 border-2 border-dashed rounded-lg">
      <p class="text-muted-foreground mb-4">No mash steps defined yet</p>
      <Button variant="outline" @click="addNewStep">
        <PlusIcon class="h-4 w-4 mr-2" />
        Add First Step
      </Button>
    </div>

    <div v-else class="space-y-3">
      <Card v-for="(step, index) in steps" :key="index" class="relative">
        <CardContent class="pt-6">
          <div class="flex items-start gap-4">
            <!-- Step number badge -->
            <div class="flex-shrink-0">
              <div class="w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-semibold">
                {{ index + 1 }}
              </div>
            </div>

            <!-- Step details -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between mb-2">
                <div>
                  <h4 class="font-semibold text-lg">{{ step.name }}</h4>
                  <Badge :class="getStepTypeColor(step.type)" class="mt-1">
                    {{ step.type }}
                  </Badge>
                </div>
              </div>

              <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3 text-sm">
                <div>
                  <span class="text-muted-foreground">Temperature:</span>
                  <span class="font-semibold ml-1">{{ step.step_temp }}°C</span>
                </div>
                <div>
                  <span class="text-muted-foreground">Duration:</span>
                  <span class="font-semibold ml-1">{{ step.step_time }} min</span>
                </div>
                <div v-if="step.ramp_time">
                  <span class="text-muted-foreground">Ramp Time:</span>
                  <span class="font-semibold ml-1">{{ step.ramp_time }} min</span>
                </div>
                <div v-if="step.decoction_amt">
                  <span class="text-muted-foreground">Decoction:</span>
                  <span class="font-semibold ml-1">{{ step.decoction_amt }}</span>
                </div>
              </div>

              <p v-if="step.description" class="text-sm text-muted-foreground mt-2">
                {{ step.description }}
              </p>
            </div>

            <!-- Actions -->
            <div class="flex-shrink-0 flex flex-col gap-1">
              <Button
                variant="ghost"
                size="sm"
                :disabled="index === 0"
                class="h-8 w-8 p-0"
                @click="moveStepUp(index)"
              >
                <ChevronUpIcon class="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                :disabled="index === steps.length - 1"
                class="h-8 w-8 p-0"
                @click="moveStepDown(index)"
              >
                <ChevronDownIcon class="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                class="h-8 w-8 p-0"
                @click="editStep(step, index)"
              >
                <span class="text-xs">✏️</span>
              </Button>
              <Button
                variant="ghost"
                size="sm"
                class="h-8 w-8 p-0 text-destructive"
                @click="deleteStep(index)"
              >
                <TrashIcon class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Step Edit Dialog -->
    <div v-if="showStepDialog" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card class="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <CardHeader>
          <CardTitle>{{ (editingStep as any)?.index !== undefined ? 'Edit' : 'Add' }} Mash Step</CardTitle>
          <CardDescription>Configure the mash step parameters</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="space-y-2">
            <Label for="stepName">Step Name *</Label>
            <Input
              id="stepName"
              v-model="editingStep!.name"
              placeholder="e.g., Saccharification Rest"
            />
          </div>

          <div class="space-y-2">
            <Label for="stepType">Step Type *</Label>
            <select
              id="stepType"
              v-model="editingStep!.type"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              <option v-for="type in stepTypes" :key="type.value" :value="type.value">
                {{ type.label }} - {{ type.description }}
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="stepTemp">Temperature (°C) *</Label>
              <Input
                id="stepTemp"
                v-model.number="editingStep!.step_temp"
                type="number"
                min="0"
                max="100"
                step="0.5"
              />
            </div>

            <div class="space-y-2">
              <Label for="stepTime">Duration (minutes) *</Label>
              <Input
                id="stepTime"
                v-model.number="editingStep!.step_time"
                type="number"
                min="0"
                max="300"
                step="5"
              />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="rampTime">Ramp Time (minutes)</Label>
            <Input
              id="rampTime"
              v-model.number="editingStep!.ramp_time"
              type="number"
              min="0"
              max="60"
              step="1"
            />
            <p class="text-xs text-muted-foreground">Time to reach target temperature</p>
          </div>

          <div v-if="editingStep!.type === 'Decoction'" class="space-y-2">
            <Label for="decoctionAmt">Decoction Amount</Label>
            <Input
              id="decoctionAmt"
              v-model="editingStep!.decoction_amt"
              placeholder="e.g., 30%"
            />
          </div>

          <div class="space-y-2">
            <Label for="stepDescription">Description</Label>
            <textarea
              id="stepDescription"
              v-model="editingStep!.description"
              class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              placeholder="Additional notes about this step..."
            />
          </div>

          <Alert>
            <AlertDescription>
              <strong>Validation:</strong>
              <ul class="list-disc list-inside text-sm mt-1">
                <li>Temperature: 0-100°C</li>
                <li>Duration: 0-300 minutes</li>
                <li>Ramp time: 0-60 minutes</li>
              </ul>
            </AlertDescription>
          </Alert>

          <div class="flex justify-end gap-2">
            <Button variant="outline" @click="closeStepDialog">Cancel</Button>
            <Button @click="saveStep">Save Step</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
