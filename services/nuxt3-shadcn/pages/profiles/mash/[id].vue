<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '~/components/ui/tabs'
import MashStepDesigner from '~/components/mash/MashStepDesigner.vue'
import BrewDayTimer from '~/components/mash/BrewDayTimer.vue'

const route = useRoute()
const router = useRouter()

const mash = ref({
  id: '',
  name: '',
  version: 1,
  grain_temp: 20,
  tun_temp: 20,
  sparge_temp: 76,
  ph: 5.4,
  tun_weight: 15,
  tun_specific_heat: 3,
  notes: '',
  display_grain_temp: '20 °C',
  display_tun_temp: '20 °C',
  display_sparge_temp: '76 °C',
  display_tun_weight: '15 lb',
})

const mashSteps = ref<any[]>([])
const isLoading = ref(false)
const error = ref('')
const showTimer = ref(false)

// Fetch mash profile
const getMashProfile = async (id: string) => {
  try {
    isLoading.value = true
    error.value = ''
    
    const response = await axios.get(`http://localhost:8000/mash/${id}`)
    mash.value = response.data
    
    // Fetch mash steps
    const stepsResponse = await axios.get(`http://localhost:8000/mash/${id}/steps`)
    mashSteps.value = stepsResponse.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load mash profile'
    console.error('Error loading mash profile:', err)
  } finally {
    isLoading.value = false
  }
}

// Auto-update display fields
const updateDisplayFields = () => {
  mash.value.display_grain_temp = `${mash.value.grain_temp} °C`
  mash.value.display_tun_temp = `${mash.value.tun_temp} °C`
  mash.value.display_sparge_temp = `${mash.value.sparge_temp} °C`
  mash.value.display_tun_weight = `${mash.value.tun_weight} lb`
}

// Update mash profile
const updateMash = async () => {
  if (!mash.value.name.trim()) {
    alert('Please provide a name for the mash profile')
    return
  }

  try {
    isLoading.value = true
    error.value = ''
    
    updateDisplayFields()
    
    // Update the mash profile
    await axios.put(`http://localhost:8000/mash/${mash.value.id}`, mash.value)
    
    // Get existing steps
    const existingStepsResponse = await axios.get(`http://localhost:8000/mash/${mash.value.id}/steps`)
    const existingSteps = existingStepsResponse.data
    
    // Delete steps that were removed
    for (const existingStep of existingSteps) {
      const stillExists = mashSteps.value.find(s => s.id === existingStep.id)
      if (!stillExists) {
        await axios.delete(`http://localhost:8000/mash/steps/${existingStep.id}`)
      }
    }
    
    // Update or create steps
    for (const step of mashSteps.value) {
      const stepData = {
        ...step,
        version: 1,
        display_step_temp: `${step.step_temp} °C`
      }
      
      if (step.id) {
        // Update existing step
        await axios.put(`http://localhost:8000/mash/steps/${step.id}`, stepData)
      } else {
        // Create new step
        await axios.post(`http://localhost:8000/mash/${mash.value.id}/steps`, stepData)
      }
    }
    
    // Navigate back
    router.push('/profiles/mash')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to update mash profile'
    console.error('Error updating mash profile:', err)
  } finally {
    isLoading.value = false
  }
}

// Cancel
const cancel = () => {
  router.back()
}

onMounted(() => {
  const id = route.params.id as string
  if (id) {
    getMashProfile(id)
  }
})
</script>

<template>
  <div class="container mx-auto py-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Edit Mash Profile</h1>
        <p class="text-muted-foreground">Modify your mash schedule</p>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading && !mash.id" class="text-center py-12">
      <p class="text-muted-foreground">Loading mash profile...</p>
    </div>

    <!-- Error display -->
    <div v-if="error" class="bg-destructive/10 text-destructive border border-destructive rounded-lg p-4">
      {{ error }}
    </div>

    <!-- Main form -->
    <Tabs v-if="mash.id" default-value="basic" class="w-full">
      <TabsList>
        <TabsTrigger value="basic">Basic Info</TabsTrigger>
        <TabsTrigger value="steps">Mash Steps</TabsTrigger>
        <TabsTrigger value="timer" :disabled="mashSteps.length === 0">
          Brew Day Timer
        </TabsTrigger>
      </TabsList>

      <!-- Basic Info Tab -->
      <TabsContent value="basic" class="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Profile Information</CardTitle>
            <CardDescription>Basic mash profile settings</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="space-y-2">
              <Label for="name">Profile Name *</Label>
              <Input
                id="name"
                v-model="mash.name"
                placeholder="e.g., Single Infusion - Medium Body"
                required
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="space-y-2">
                <Label for="grain_temp">Grain Temperature (°C)</Label>
                <Input
                  id="grain_temp"
                  type="number"
                  v-model.number="mash.grain_temp"
                  min="0"
                  max="50"
                />
              </div>

              <div class="space-y-2">
                <Label for="tun_temp">Tun Temperature (°C)</Label>
                <Input
                  id="tun_temp"
                  type="number"
                  v-model.number="mash.tun_temp"
                  min="0"
                  max="50"
                />
              </div>

              <div class="space-y-2">
                <Label for="sparge_temp">Sparge Temperature (°C)</Label>
                <Input
                  id="sparge_temp"
                  type="number"
                  v-model.number="mash.sparge_temp"
                  min="60"
                  max="85"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="space-y-2">
                <Label for="ph">Target pH</Label>
                <Input
                  id="ph"
                  type="number"
                  v-model.number="mash.ph"
                  min="4.0"
                  max="6.0"
                  step="0.1"
                />
              </div>

              <div class="space-y-2">
                <Label for="tun_weight">Tun Weight (lb)</Label>
                <Input
                  id="tun_weight"
                  type="number"
                  v-model.number="mash.tun_weight"
                  min="0"
                />
              </div>

              <div class="space-y-2">
                <Label for="tun_specific_heat">Tun Specific Heat</Label>
                <Input
                  id="tun_specific_heat"
                  type="number"
                  v-model.number="mash.tun_specific_heat"
                  min="0"
                  step="0.1"
                />
              </div>
            </div>

            <div class="space-y-2">
              <Label for="notes">Notes</Label>
              <textarea
                id="notes"
                v-model="mash.notes"
                class="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                placeholder="Add any additional notes about this mash profile..."
              />
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Mash Steps Tab -->
      <TabsContent value="steps" class="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Mash Schedule</CardTitle>
            <CardDescription>Define the step-by-step mash process</CardDescription>
          </CardHeader>
          <CardContent>
            <MashStepDesigner v-model="mashSteps" />
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Brew Day Timer Tab -->
      <TabsContent value="timer" class="space-y-4">
        <BrewDayTimer 
          v-if="mashSteps.length > 0"
          :steps="mashSteps"
          :profile-name="mash.name"
        />
        <Card v-else>
          <CardContent class="py-12 text-center">
            <p class="text-muted-foreground">
              Add mash steps to enable the brew day timer
            </p>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>

    <!-- Actions -->
    <div class="flex justify-end gap-4">
      <Button @click="cancel" variant="outline" :disabled="isLoading">
        Cancel
      </Button>
      <Button @click="updateMash" :disabled="isLoading || !mash.id">
        {{ isLoading ? 'Saving...' : 'Update Profile' }}
      </Button>
    </div>
  </div>
</template>