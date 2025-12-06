<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '~/components/ui/tabs'
import MashStepDesigner from '~/components/mash/MashStepDesigner.vue'
import MashTemplateSelector from '~/components/mash/MashTemplateSelector.vue'

const router = useRouter()

// State
const showTemplateSelector = ref(true)
const mash = ref({
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

// Handle template selection
const handleTemplateSelected = async (template: any, customName: string) => {
  try {
    isLoading.value = true
    error.value = ''
    
    // Create mash profile from template
    const response = await axios.post(
      `http://localhost:8000/mash/from-template/${template.id}`,
      null,
      { params: { custom_name: customName } }
    )
    
    if (response.data && response.data.id) {
      // Navigate to the edit page of the newly created profile
      router.push(`/profiles/mash/${response.data.id}`)
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to create profile from template'
    console.error('Error creating from template:', err)
  } finally {
    isLoading.value = false
  }
}

// Close template selector and start from scratch
const closeTemplateSelector = () => {
  showTemplateSelector.value = false
}

// Auto-update display fields
const updateDisplayFields = () => {
  mash.value.display_grain_temp = `${mash.value.grain_temp} °C`
  mash.value.display_tun_temp = `${mash.value.tun_temp} °C`
  mash.value.display_sparge_temp = `${mash.value.sparge_temp} °C`
  mash.value.display_tun_weight = `${mash.value.tun_weight} lb`
}

// Save mash profile
const saveMash = async () => {
  // Validate
  if (!mash.value.name.trim()) {
    alert('Please provide a name for the mash profile')
    return
  }

  try {
    isLoading.value = true
    error.value = ''
    
    // Update display fields
    updateDisplayFields()
    
    // Create the mash profile
    const response = await axios.post('http://localhost:8000/mash/', mash.value)
    
    if (response.data && response.data.id) {
      const profileId = response.data.id
      
      // Create mash steps if any
      if (mashSteps.value.length > 0) {
        for (const step of mashSteps.value) {
          await axios.post(`http://localhost:8000/mash/${profileId}/steps`, {
            ...step,
            version: 1,
            display_step_temp: `${step.step_temp} °C`
          })
        }
      }
      
      // Navigate back
      router.push('/profiles/mash')
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to save mash profile'
    console.error('Error saving mash profile:', err)
  } finally {
    isLoading.value = false
  }
}

// Cancel
const cancel = () => {
  router.back()
}
</script>

<template>
  <div class="container mx-auto py-6 space-y-6">
    <!-- Template selector dialog -->
    <MashTemplateSelector 
      v-if="showTemplateSelector"
      @template-selected="handleTemplateSelected"
      @close="closeTemplateSelector"
    />

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Create Mash Profile</h1>
        <p class="text-muted-foreground">Design a step-by-step mash schedule</p>
      </div>
      <Button variant="outline" @click="showTemplateSelector = true">
        Use Template
      </Button>
    </div>

    <!-- Error display -->
    <div v-if="error" class="bg-destructive/10 text-destructive border border-destructive rounded-lg p-4">
      {{ error }}
    </div>

    <!-- Main form -->
    <Tabs default-value="basic" class="w-full">
      <TabsList>
        <TabsTrigger value="basic">Basic Info</TabsTrigger>
        <TabsTrigger value="steps">Mash Steps</TabsTrigger>
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
                  v-model.number="mash.grain_temp"
                  type="number"
                  min="0"
                  max="50"
                />
              </div>

              <div class="space-y-2">
                <Label for="tun_temp">Tun Temperature (°C)</Label>
                <Input
                  id="tun_temp"
                  v-model.number="mash.tun_temp"
                  type="number"
                  min="0"
                  max="50"
                />
              </div>

              <div class="space-y-2">
                <Label for="sparge_temp">Sparge Temperature (°C)</Label>
                <Input
                  id="sparge_temp"
                  v-model.number="mash.sparge_temp"
                  type="number"
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
                  v-model.number="mash.ph"
                  type="number"
                  min="4.0"
                  max="6.0"
                  step="0.1"
                />
              </div>

              <div class="space-y-2">
                <Label for="tun_weight">Tun Weight (lb)</Label>
                <Input
                  id="tun_weight"
                  v-model.number="mash.tun_weight"
                  type="number"
                  min="0"
                />
              </div>

              <div class="space-y-2">
                <Label for="tun_specific_heat">Tun Specific Heat</Label>
                <Input
                  id="tun_specific_heat"
                  v-model.number="mash.tun_specific_heat"
                  type="number"
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
    </Tabs>

    <!-- Actions -->
    <div class="flex justify-end gap-4">
      <Button variant="outline" :disabled="isLoading" @click="cancel">
        Cancel
      </Button>
      <Button :disabled="isLoading" @click="saveMash">
        {{ isLoading ? 'Saving...' : 'Save Profile' }}
      </Button>
    </div>
  </div>
</template>
