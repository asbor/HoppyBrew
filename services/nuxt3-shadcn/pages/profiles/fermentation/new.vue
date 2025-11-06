<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Checkbox } from '@/components/ui/checkbox'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  useFermentationProfiles,
  FERMENTATION_TEMPLATES,
  STEP_TYPES,
  type FermentationProfile,
  type FermentationStep,
} from '@/composables/useFermentationProfiles'

const router = useRouter()
const { createProfile } = useFermentationProfiles()

const profile = ref<FermentationProfile>({
  name: '',
  description: '',
  is_pressurized: false,
  is_template: false,
  steps: [],
})

const saving = ref(false)
const error = ref<string | null>(null)

function loadTemplate(templateKey: string) {
  const template = FERMENTATION_TEMPLATES[templateKey as keyof typeof FERMENTATION_TEMPLATES]
  if (template) {
    profile.value = {
      ...template,
      is_template: false, // User profiles are not templates by default
    }
  }
}

function addStep() {
  const newOrder = (profile.value.steps?.length || 0) + 1
  const newStep: FermentationStep = {
    step_order: newOrder,
    name: '',
    step_type: 'primary',
    temperature: 20,
    duration_days: 7,
    ramp_days: 0,
  }
  if (!profile.value.steps) {
    profile.value.steps = []
  }
  profile.value.steps.push(newStep)
}

function removeStep(index: number) {
  if (!profile.value.steps) return
  profile.value.steps.splice(index, 1)
  // Reorder remaining steps
  profile.value.steps.forEach((step, idx) => {
    step.step_order = idx + 1
  })
}

function moveStepUp(index: number) {
  if (!profile.value.steps || index === 0) return
  const temp = profile.value.steps[index]
  profile.value.steps[index] = profile.value.steps[index - 1]
  profile.value.steps[index - 1] = temp
  // Update step orders
  profile.value.steps.forEach((step, idx) => {
    step.step_order = idx + 1
  })
}

function moveStepDown(index: number) {
  if (!profile.value.steps || index === profile.value.steps.length - 1) return
  const temp = profile.value.steps[index]
  profile.value.steps[index] = profile.value.steps[index + 1]
  profile.value.steps[index + 1] = temp
  // Update step orders
  profile.value.steps.forEach((step, idx) => {
    step.step_order = idx + 1
  })
}

const totalDays = computed(() => {
  if (!profile.value.steps) return 0
  return profile.value.steps.reduce((sum, step) => sum + (step.duration_days || 0), 0)
})

async function handleSave() {
  if (!profile.value.name.trim()) {
    error.value = 'Profile name is required'
    return
  }

  saving.value = true
  error.value = null

  try {
    const response = await createProfile(profile.value)
    if (response.error.value) {
      error.value = response.error.value
    } else {
      // Navigate back to the list
      router.push('/profiles/fermentation')
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to create profile'
  } finally {
    saving.value = false
  }
}

function getStepTypeLabel(value: string): string {
  const type = STEP_TYPES.find((t) => t.value === value)
  return type?.label || value
}
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold">New Fermentation Profile</h1>
      <p class="text-sm text-muted-foreground mt-1">Create a fermentation schedule for your beer</p>
    </div>

    <div v-if="error" class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Template Selection -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Start from Template</CardTitle>
        <CardDescription>Choose a template to get started quickly</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="flex gap-2">
          <Button @click="loadTemplate('ale')" variant="outline">Standard Ale</Button>
          <Button @click="loadTemplate('lager')" variant="outline">Lager</Button>
          <Button @click="loadTemplate('neipa')" variant="outline">NEIPA</Button>
        </div>
      </CardContent>
    </Card>

    <!-- Profile Details -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Profile Details</CardTitle>
      </CardHeader>
      <CardContent class="space-y-4">
        <div>
          <Label for="name">Profile Name *</Label>
          <Input id="name" v-model="profile.name" placeholder="e.g., My Custom Ale Profile" />
        </div>

        <div>
          <Label for="description">Description</Label>
          <Textarea
            id="description"
            v-model="profile.description"
            placeholder="Describe this fermentation profile..."
            rows="3"
          />
        </div>

        <div class="flex items-center space-x-2">
          <Checkbox id="pressurized" v-model:checked="profile.is_pressurized" />
          <Label for="pressurized" class="cursor-pointer">Use pressurized fermentation</Label>
        </div>

        <div class="flex items-center space-x-2">
          <Checkbox id="template" v-model:checked="profile.is_template" />
          <Label for="template" class="cursor-pointer">Save as template</Label>
        </div>
      </CardContent>
    </Card>

    <!-- Fermentation Steps -->
    <Card class="mb-6">
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Fermentation Steps</CardTitle>
            <CardDescription>
              Total duration: {{ totalDays }} days
            </CardDescription>
          </div>
          <Button @click="addStep" variant="outline" size="sm">Add Step</Button>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="!profile.steps || profile.steps.length === 0" class="text-center py-8 text-muted-foreground">
          No steps added yet. Click "Add Step" to create your first fermentation step.
        </div>

        <div v-else class="space-y-4">
          <Card v-for="(step, index) in profile.steps" :key="index" class="border">
            <CardContent class="pt-6">
              <div class="flex items-start gap-4">
                <div class="flex-1 grid grid-cols-2 gap-4">
                  <!-- Step Name -->
                  <div>
                    <Label :for="`step-name-${index}`">Step Name</Label>
                    <Input :id="`step-name-${index}`" v-model="step.name" placeholder="e.g., Primary Fermentation" />
                  </div>

                  <!-- Step Type -->
                  <div>
                    <Label :for="`step-type-${index}`">Step Type</Label>
                    <Select v-model="step.step_type">
                      <SelectTrigger :id="`step-type-${index}`">
                        <SelectValue>{{ getStepTypeLabel(step.step_type) }}</SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem v-for="type in STEP_TYPES" :key="type.value" :value="type.value">
                          {{ type.label }}
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <!-- Temperature -->
                  <div>
                    <Label :for="`step-temp-${index}`">Temperature (°C)</Label>
                    <Input
                      :id="`step-temp-${index}`"
                      v-model.number="step.temperature"
                      type="number"
                      step="0.5"
                      placeholder="20"
                    />
                  </div>

                  <!-- Duration -->
                  <div>
                    <Label :for="`step-duration-${index}`">Duration (days)</Label>
                    <Input
                      :id="`step-duration-${index}`"
                      v-model.number="step.duration_days"
                      type="number"
                      placeholder="7"
                    />
                  </div>

                  <!-- Ramp Days -->
                  <div>
                    <Label :for="`step-ramp-${index}`">Ramp Time (days)</Label>
                    <Input :id="`step-ramp-${index}`" v-model.number="step.ramp_days" type="number" placeholder="0" />
                  </div>

                  <!-- Pressure (if pressurized) -->
                  <div v-if="profile.is_pressurized">
                    <Label :for="`step-pressure-${index}`">Pressure (PSI)</Label>
                    <Input
                      :id="`step-pressure-${index}`"
                      v-model.number="step.pressure_psi"
                      type="number"
                      step="0.5"
                      placeholder="15"
                    />
                  </div>

                  <!-- Notes -->
                  <div class="col-span-2">
                    <Label :for="`step-notes-${index}`">Notes</Label>
                    <Textarea :id="`step-notes-${index}`" v-model="step.notes" placeholder="Optional notes..." rows="2" />
                  </div>
                </div>

                <!-- Step Controls -->
                <div class="flex flex-col gap-2">
                  <Button
                    @click="moveStepUp(index)"
                    variant="outline"
                    size="icon"
                    :disabled="index === 0"
                    title="Move up"
                  >
                    ↑
                  </Button>
                  <Button
                    @click="moveStepDown(index)"
                    variant="outline"
                    size="icon"
                    :disabled="index === profile.steps!.length - 1"
                    title="Move down"
                  >
                    ↓
                  </Button>
                  <Button @click="removeStep(index)" variant="destructive" size="icon" title="Remove step"> ✕ </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>

    <!-- Actions -->
    <div class="flex justify-between">
      <Button @click="router.push('/profiles/fermentation')" variant="outline">Cancel</Button>
      <Button @click="handleSave" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save Profile' }}
      </Button>
    </div>
  </div>
</template>
