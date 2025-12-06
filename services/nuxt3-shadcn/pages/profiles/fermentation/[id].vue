<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Checkbox } from '@/components/ui/checkbox'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  useFermentationProfiles,
  STEP_TYPES,
  type FermentationProfile,
  type FermentationStep,
} from '@/composables/useFermentationProfiles'

const router = useRouter()
const route = useRoute()
const { getProfile, updateProfile, addStep: apiAddStep, updateStep: apiUpdateStep, deleteStep: apiDeleteStep } = useFermentationProfiles()

const profileId = computed(() => parseInt(route.params.id as string))
const profile = ref<FermentationProfile | null>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)

async function fetchProfile() {
  loading.value = true
  error.value = null

  try {
    const response = await getProfile(profileId.value)
    if (response.error.value) {
      error.value = response.error.value
    } else {
      profile.value = response.data.value
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to fetch profile'
  } finally {
    loading.value = false
  }
}

async function addStep() {
  if (!profile.value) return

  const newOrder = (profile.value.steps?.length || 0) + 1
  const newStep: FermentationStep = {
    step_order: newOrder,
    name: '',
    step_type: 'primary',
    temperature: 20,
    duration_days: 7,
    ramp_days: 0,
  }

  try {
    const response = await apiAddStep(profileId.value, newStep)
    if (response.error.value) {
      error.value = response.error.value
    } else {
      // Refresh the profile to get the new step with ID
      await fetchProfile()
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to add step'
  }
}

async function removeStep(stepId: number, index: number) {
  if (!confirm('Are you sure you want to delete this step?')) return

  try {
    await apiDeleteStep(stepId)
    // Remove from local list
    if (profile.value?.steps) {
      profile.value.steps.splice(index, 1)
      // Reorder remaining steps
      profile.value.steps.forEach((step, idx) => {
        step.step_order = idx + 1
      })
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to delete step'
  }
}

async function saveStep(step: FermentationStep) {
  if (!step.id) return

  try {
    await apiUpdateStep(step.id, step)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to update step'
  }
}

const totalDays = computed(() => {
  if (!profile.value?.steps) return 0
  return profile.value.steps.reduce((sum, step) => sum + (step.duration_days || 0), 0)
})

async function handleSave() {
  if (!profile.value) return

  if (!profile.value.name.trim()) {
    error.value = 'Profile name is required'
    return
  }

  saving.value = true
  error.value = null

  try {
    // Update profile details
    const response = await updateProfile(profileId.value, {
      name: profile.value.name,
      description: profile.value.description,
      is_pressurized: profile.value.is_pressurized,
      is_template: profile.value.is_template,
    })

    if (response.error.value) {
      error.value = response.error.value
    } else {
      // Save all steps
      if (profile.value.steps) {
        for (const step of profile.value.steps) {
          await saveStep(step)
        }
      }
      // Navigate back to the list
      router.push('/profiles/fermentation')
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to update profile'
  } finally {
    saving.value = false
  }
}

function getStepTypeLabel(value: string): string {
  const type = STEP_TYPES.find((t) => t.value === value)
  return type?.label || value
}

onMounted(fetchProfile)
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold">Edit Fermentation Profile</h1>
      <p class="text-sm text-muted-foreground mt-1">Update your fermentation schedule</p>
    </div>

    <div v-if="error" class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div v-if="loading" class="flex items-center justify-center py-8">
      <p class="text-muted-foreground">Loading profile...</p>
    </div>

    <div v-else-if="profile">
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
            <Button variant="outline" size="sm" @click="addStep">Add Step</Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="!profile.steps || profile.steps.length === 0" class="text-center py-8 text-muted-foreground">
            No steps added yet. Click "Add Step" to create your first fermentation step.
          </div>

          <div v-else class="space-y-4">
            <Card v-for="(step, index) in profile.steps" :key="step.id || index" class="border">
              <CardContent class="pt-6">
                <div class="flex items-start gap-4">
                  <div class="flex-1 grid grid-cols-2 gap-4">
                    <!-- Step Name -->
                    <div>
                      <Label :for="`step-name-${index}`">Step Name</Label>
                      <Input
                        :id="`step-name-${index}`"
                        v-model="step.name"
                        placeholder="e.g., Primary Fermentation"
                        @blur="saveStep(step)"
                      />
                    </div>

                    <!-- Step Type -->
                    <div>
                      <Label :for="`step-type-${index}`">Step Type</Label>
                      <Select v-model="step.step_type" @update:model-value="saveStep(step)">
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
                        @blur="saveStep(step)"
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
                        @blur="saveStep(step)"
                      />
                    </div>

                    <!-- Ramp Days -->
                    <div>
                      <Label :for="`step-ramp-${index}`">Ramp Time (days)</Label>
                      <Input
                        :id="`step-ramp-${index}`"
                        v-model.number="step.ramp_days"
                        type="number"
                        placeholder="0"
                        @blur="saveStep(step)"
                      />
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
                        @blur="saveStep(step)"
                      />
                    </div>

                    <!-- Notes -->
                    <div class="col-span-2">
                      <Label :for="`step-notes-${index}`">Notes</Label>
                      <Textarea
                        :id="`step-notes-${index}`"
                        v-model="step.notes"
                        placeholder="Optional notes..."
                        rows="2"
                        @blur="saveStep(step)"
                      />
                    </div>
                  </div>

                  <!-- Step Controls -->
                  <div class="flex flex-col gap-2">
                    <Button
                      variant="destructive"
                      size="icon"
                      title="Remove step"
                      :disabled="!step.id"
                      @click="step.id && removeStep(step.id, index)"
                    >
                      ✕
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      <!-- Actions -->
      <div class="flex justify-between">
        <Button variant="outline" @click="router.push('/profiles/fermentation')">Back to List</Button>
        <Button :disabled="saving" @click="handleSave">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </Button>
      </div>
    </div>
  </div>
</template>
