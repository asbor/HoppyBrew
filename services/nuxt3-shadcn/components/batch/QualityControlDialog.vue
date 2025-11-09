<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>{{ isEdit ? 'Edit' : 'Add' }} Quality Control Test</DialogTitle>
        <DialogDescription>
          Record quality control measurements and tasting notes for this batch
        </DialogDescription>
      </DialogHeader>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Test Date -->
        <div class="space-y-2">
          <Label for="test-date">Test Date</Label>
          <Input
            id="test-date"
            v-model="formData.test_date"
            type="datetime-local"
            required
          />
        </div>

        <!-- Measurements Section -->
        <div class="space-y-4">
          <h3 class="font-semibold text-lg">Measurements</h3>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Final Gravity -->
            <div class="space-y-2">
              <Label for="final-gravity">Final Gravity</Label>
              <Input
                id="final-gravity"
                v-model.number="formData.final_gravity"
                type="number"
                step="0.001"
                placeholder="1.012"
              />
            </div>

            <!-- ABV Actual -->
            <div class="space-y-2">
              <Label for="abv-actual">ABV % (Actual)</Label>
              <Input
                id="abv-actual"
                v-model.number="formData.abv_actual"
                type="number"
                step="0.1"
                placeholder="5.2"
              />
            </div>

            <!-- Color -->
            <div class="space-y-2">
              <Label for="color">Color</Label>
              <Select v-model="formData.color">
                <SelectTrigger id="color">
                  <SelectValue placeholder="Select color" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Pale Straw">Pale Straw</SelectItem>
                  <SelectItem value="Straw">Straw</SelectItem>
                  <SelectItem value="Pale Gold">Pale Gold</SelectItem>
                  <SelectItem value="Deep Gold">Deep Gold</SelectItem>
                  <SelectItem value="Pale Amber">Pale Amber</SelectItem>
                  <SelectItem value="Amber">Amber</SelectItem>
                  <SelectItem value="Deep Amber">Deep Amber</SelectItem>
                  <SelectItem value="Copper">Copper</SelectItem>
                  <SelectItem value="Deep Copper">Deep Copper</SelectItem>
                  <SelectItem value="Light Brown">Light Brown</SelectItem>
                  <SelectItem value="Brown">Brown</SelectItem>
                  <SelectItem value="Dark Brown">Dark Brown</SelectItem>
                  <SelectItem value="Black">Black</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <!-- Clarity -->
            <div class="space-y-2">
              <Label for="clarity">Clarity</Label>
              <Select v-model="formData.clarity">
                <SelectTrigger id="clarity">
                  <SelectValue placeholder="Select clarity" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Brilliant">Brilliant</SelectItem>
                  <SelectItem value="Clear">Clear</SelectItem>
                  <SelectItem value="Slight Haze">Slight Haze</SelectItem>
                  <SelectItem value="Hazy">Hazy</SelectItem>
                  <SelectItem value="Cloudy">Cloudy</SelectItem>
                  <SelectItem value="Opaque">Opaque</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        <!-- BJCP Score Section -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-semibold text-lg">BJCP Score Sheet</h3>
            <Button
              type="button"
              variant="outline"
              size="sm"
              @click="showBJCPCalculator = !showBJCPCalculator"
            >
              <Icon :name="showBJCPCalculator ? 'mdi:chevron-up' : 'mdi:chevron-down'" class="mr-2 h-4 w-4" />
              {{ showBJCPCalculator ? 'Hide' : 'Show' }} Calculator
            </Button>
          </div>

          <div v-if="showBJCPCalculator" class="space-y-3 p-4 bg-muted rounded-lg">
            <div class="grid grid-cols-2 gap-3">
              <!-- Aroma -->
              <div class="space-y-2">
                <Label for="aroma">Aroma (max 12)</Label>
                <Input
                  id="aroma"
                  v-model.number="bjcpScores.aroma"
                  type="number"
                  step="0.5"
                  min="0"
                  max="12"
                  @input="calculateBJCPScore"
                />
              </div>

              <!-- Appearance -->
              <div class="space-y-2">
                <Label for="appearance">Appearance (max 3)</Label>
                <Input
                  id="appearance"
                  v-model.number="bjcpScores.appearance"
                  type="number"
                  step="0.5"
                  min="0"
                  max="3"
                  @input="calculateBJCPScore"
                />
              </div>

              <!-- Flavor -->
              <div class="space-y-2">
                <Label for="flavor">Flavor (max 20)</Label>
                <Input
                  id="flavor"
                  v-model.number="bjcpScores.flavor"
                  type="number"
                  step="0.5"
                  min="0"
                  max="20"
                  @input="calculateBJCPScore"
                />
              </div>

              <!-- Mouthfeel -->
              <div class="space-y-2">
                <Label for="mouthfeel">Mouthfeel (max 5)</Label>
                <Input
                  id="mouthfeel"
                  v-model.number="bjcpScores.mouthfeel"
                  type="number"
                  step="0.5"
                  min="0"
                  max="5"
                  @input="calculateBJCPScore"
                />
              </div>

              <!-- Overall Impression -->
              <div class="space-y-2 col-span-2">
                <Label for="overall">Overall Impression (max 10)</Label>
                <Input
                  id="overall"
                  v-model.number="bjcpScores.overall_impression"
                  type="number"
                  step="0.5"
                  min="0"
                  max="10"
                  @input="calculateBJCPScore"
                />
              </div>
            </div>

            <!-- Total Score Display -->
            <div v-if="bjcpResult" class="mt-4 p-3 bg-primary/10 rounded-md">
              <div class="flex justify-between items-center">
                <span class="font-semibold">Total Score:</span>
                <span class="text-2xl font-bold">{{ bjcpResult.total_score }} / 50</span>
              </div>
              <div class="flex justify-between items-center mt-2">
                <span class="text-sm">Rating:</span>
                <Badge :class="getBJCPRatingColor(bjcpResult.rating)">
                  {{ bjcpResult.rating }}
                </Badge>
              </div>
            </div>
          </div>

          <!-- Manual Score Entry (if calculator not used) -->
          <div v-if="!showBJCPCalculator" class="space-y-2">
            <Label for="score">Overall Score (0-50)</Label>
            <Input
              id="score"
              v-model.number="formData.score"
              type="number"
              step="0.5"
              min="0"
              max="50"
              placeholder="42.5"
            />
          </div>
        </div>

        <!-- Tasting Notes -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <Label for="taste-notes">Tasting Notes</Label>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              @click="showTemplates = !showTemplates"
            >
              <Icon name="mdi:text-box-multiple" class="mr-2 h-4 w-4" />
              Templates
            </Button>
          </div>

          <!-- Tasting Note Templates -->
          <div v-if="showTemplates" class="grid grid-cols-2 gap-2 mb-2">
            <Button
              v-for="template in tastingTemplates"
              :key="template.name"
              type="button"
              variant="outline"
              size="sm"
              @click="applyTemplate(template)"
            >
              {{ template.name }}
            </Button>
          </div>

          <Textarea
            id="taste-notes"
            v-model="formData.taste_notes"
            rows="6"
            placeholder="Describe the aroma, appearance, flavor, mouthfeel, and overall impression..."
          />
        </div>

        <!-- Photo Upload -->
        <div class="space-y-2">
          <Label for="photo">Appearance Photo</Label>
          <Input
            id="photo"
            ref="photoInput"
            type="file"
            accept="image/*"
            @change="handlePhotoChange"
          />
          <p v-if="photoPreview" class="text-sm text-muted-foreground">
            Photo selected: {{ photoFile?.name }}
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="text-sm text-red-600">
          {{ errorMessage }}
        </div>

        <!-- Actions -->
        <DialogFooter>
          <Button type="button" variant="outline" @click="$emit('update:open', false)">
            Cancel
          </Button>
          <Button type="submit" :disabled="submitting">
            <Icon v-if="submitting" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
            {{ isEdit ? 'Update' : 'Save' }} Test
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Icon } from '#components'

interface Props {
  open: boolean
  batchId: number
  existingTest?: any
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:open': [value: boolean]
  'save': []
}>()

const isEdit = computed(() => !!props.existingTest)

// Form data
const formData = ref({
  batch_id: props.batchId,
  test_date: new Date().toISOString().slice(0, 16),
  final_gravity: null as number | null,
  abv_actual: null as number | null,
  color: '',
  clarity: '',
  taste_notes: '',
  score: null as number | null,
})

// BJCP scores
const bjcpScores = ref({
  aroma: 0,
  appearance: 0,
  flavor: 0,
  mouthfeel: 0,
  overall_impression: 0,
})

const bjcpResult = ref<any>(null)
const showBJCPCalculator = ref(false)
const showTemplates = ref(false)
const submitting = ref(false)
const errorMessage = ref('')

// Photo upload
const photoInput = ref<HTMLInputElement | null>(null)
const photoFile = ref<File | null>(null)
const photoPreview = ref<string | null>(null)

// Tasting note templates
const tastingTemplates = [
  {
    name: 'Clean Lager',
    template: 'Aroma: Clean, subtle malt with hint of noble hops\nAppearance: Brilliant clarity, white foam\nFlavor: Crisp, balanced malt-hop profile\nMouthfeel: Light to medium body, high carbonation\nOverall: Refreshing and well-balanced'
  },
  {
    name: 'Hoppy IPA',
    template: 'Aroma: Strong hop aroma with citrus, pine notes\nAppearance: Golden to amber, hazy acceptable\nFlavor: Bold hop flavor, balanced bitterness\nMouthfeel: Medium body, moderate carbonation\nOverall: Hop-forward with clean finish'
  },
  {
    name: 'Rich Stout',
    template: 'Aroma: Roasted malt, coffee, chocolate notes\nAppearance: Opaque black, tan head\nFlavor: Rich roasted flavors, slight bitterness\nMouthfeel: Full body, creamy texture\nOverall: Complex and satisfying'
  },
  {
    name: 'Fruity Wheat',
    template: 'Aroma: Banana and clove esters prominent\nAppearance: Cloudy, pale to golden\nFlavor: Fruity esters balanced with wheat\nMouthfeel: Light, refreshing body\nOverall: Aromatic and refreshing'
  },
]

// Calculate BJCP score
const calculateBJCPScore = async () => {
  try {
    const response = await $fetch('/api/bjcp-score', {
      method: 'POST',
      body: bjcpScores.value,
    })
    bjcpResult.value = response
    formData.value.score = response.total_score
  } catch (error) {
    console.error('Error calculating BJCP score:', error)
  }
}

// Apply template
const applyTemplate = (template: any) => {
  formData.value.taste_notes = template.template
  showTemplates.value = false
}

// Handle photo change
const handlePhotoChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    photoFile.value = file
    photoPreview.value = URL.createObjectURL(file)
  }
}

// Get BJCP rating color
const getBJCPRatingColor = (rating: string) => {
  const colors: Record<string, string> = {
    'Outstanding': 'bg-green-600',
    'Excellent': 'bg-green-500',
    'Very Good': 'bg-blue-500',
    'Good': 'bg-blue-400',
    'Fair': 'bg-yellow-500',
    'Problematic': 'bg-orange-500',
    'Flawed': 'bg-red-500',
  }
  return colors[rating] || 'bg-gray-500'
}

// Submit form
const handleSubmit = async () => {
  submitting.value = true
  errorMessage.value = ''

  try {
    // Create or update QC test
    const method = isEdit.value ? 'PUT' : 'POST'
    const url = isEdit.value
      ? `/api/quality-control-tests/${props.existingTest.id}`
      : '/api/quality-control-tests'

    const qcTest = await $fetch(url, {
      method,
      body: formData.value,
    })

    // Upload photo if selected
    if (photoFile.value && qcTest.id) {
      const photoFormData = new FormData()
      photoFormData.append('file', photoFile.value)

      await $fetch(`/api/quality-control-tests/${qcTest.id}/upload-photo`, {
        method: 'POST',
        body: photoFormData,
      })
    }

    emit('save')
    emit('update:open', false)
  } catch (error: any) {
    console.error('Error saving QC test:', error)
    errorMessage.value = error.data?.detail || 'Failed to save quality control test'
  } finally {
    submitting.value = false
  }
}

// Watch for existing test data
watch(() => props.existingTest, (newTest) => {
  if (newTest) {
    formData.value = {
      batch_id: newTest.batch_id,
      test_date: newTest.test_date.slice(0, 16),
      final_gravity: newTest.final_gravity,
      abv_actual: newTest.abv_actual,
      color: newTest.color || '',
      clarity: newTest.clarity || '',
      taste_notes: newTest.taste_notes || '',
      score: newTest.score,
    }
  }
}, { immediate: true })

// Reset form when dialog closes
watch(() => props.open, (isOpen) => {
  if (!isOpen) {
    // Reset form
    formData.value = {
      batch_id: props.batchId,
      test_date: new Date().toISOString().slice(0, 16),
      final_gravity: null,
      abv_actual: null,
      color: '',
      clarity: '',
      taste_notes: '',
      score: null,
    }
    bjcpScores.value = {
      aroma: 0,
      appearance: 0,
      flavor: 0,
      mouthfeel: 0,
      overall_impression: 0,
    }
    bjcpResult.value = null
    photoFile.value = null
    photoPreview.value = null
    errorMessage.value = ''
  }
})
</script>
