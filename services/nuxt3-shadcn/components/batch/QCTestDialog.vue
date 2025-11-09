<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-4xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>{{ isEdit ? 'Edit Quality Control Test' : 'New Quality Control Test' }}</DialogTitle>
        <DialogDescription>
          Record quality control test results and BJCP tasting notes
        </DialogDescription>
      </DialogHeader>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Test Information -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">Test Information</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label for="test_date">Test Date *</Label>
              <Input
                id="test_date"
                v-model="formData.test_date"
                type="datetime-local"
                required
              />
            </div>
            <div>
              <Label for="tester_name">Tester Name</Label>
              <Input
                id="tester_name"
                v-model="formData.tester_name"
                type="text"
                placeholder="Who conducted the test?"
              />
            </div>
          </div>
        </div>

        <!-- Measured Values -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">Measured Values</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <Label for="final_gravity">Final Gravity (SG)</Label>
              <Input
                id="final_gravity"
                v-model.number="formData.final_gravity"
                type="number"
                step="0.001"
                min="0.990"
                max="1.200"
                placeholder="1.010"
              />
            </div>
            <div>
              <Label for="abv_actual">Actual ABV (%)</Label>
              <Input
                id="abv_actual"
                v-model.number="formData.abv_actual"
                type="number"
                step="0.1"
                min="0"
                max="20"
                placeholder="5.5"
              />
            </div>
            <div>
              <Label for="color">Color (SRM)</Label>
              <Input
                id="color"
                v-model="formData.color"
                type="text"
                placeholder="8 (Light Amber)"
              />
            </div>
            <div>
              <Label for="clarity">Clarity</Label>
              <Select v-model="formData.clarity">
                <SelectTrigger>
                  <SelectValue placeholder="Select clarity" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Brilliant">Brilliant</SelectItem>
                  <SelectItem value="Clear">Clear</SelectItem>
                  <SelectItem value="Slight Haze">Slight Haze</SelectItem>
                  <SelectItem value="Hazy">Hazy</SelectItem>
                  <SelectItem value="Opaque">Opaque</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        <!-- BJCP Scores -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">BJCP Scores</h3>
            <Button 
              type="button" 
              variant="outline" 
              size="sm"
              @click="useTemplate"
            >
              <Icon name="mdi:clipboard-text" class="mr-2 h-4 w-4" />
              Use Template
            </Button>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div>
              <Label for="aroma_score">Aroma (0-12)</Label>
              <Input
                id="aroma_score"
                v-model.number="formData.aroma_score"
                type="number"
                step="0.5"
                min="0"
                max="12"
                @input="calculateTotalScore"
              />
            </div>
            <div>
              <Label for="appearance_score">Appearance (0-3)</Label>
              <Input
                id="appearance_score"
                v-model.number="formData.appearance_score"
                type="number"
                step="0.5"
                min="0"
                max="3"
                @input="calculateTotalScore"
              />
            </div>
            <div>
              <Label for="flavor_score">Flavor (0-20)</Label>
              <Input
                id="flavor_score"
                v-model.number="formData.flavor_score"
                type="number"
                step="0.5"
                min="0"
                max="20"
                @input="calculateTotalScore"
              />
            </div>
            <div>
              <Label for="mouthfeel_score">Mouthfeel (0-5)</Label>
              <Input
                id="mouthfeel_score"
                v-model.number="formData.mouthfeel_score"
                type="number"
                step="0.5"
                min="0"
                max="5"
                @input="calculateTotalScore"
              />
            </div>
            <div>
              <Label for="overall_impression_score">Overall (0-10)</Label>
              <Input
                id="overall_impression_score"
                v-model.number="formData.overall_impression_score"
                type="number"
                step="0.5"
                min="0"
                max="10"
                @input="calculateTotalScore"
              />
            </div>
            <div>
              <Label for="score">Total Score</Label>
              <Input
                id="score"
                v-model.number="formData.score"
                type="number"
                step="0.5"
                min="0"
                max="50"
                readonly
                class="font-bold"
              />
              <p v-if="scoreCategory" class="text-xs text-muted-foreground mt-1">
                {{ scoreCategory }}
              </p>
            </div>
          </div>
        </div>

        <!-- Tasting Notes -->
        <Tabs default-value="aroma" class="w-full">
          <TabsList class="grid w-full grid-cols-5">
            <TabsTrigger value="aroma">Aroma</TabsTrigger>
            <TabsTrigger value="appearance">Appearance</TabsTrigger>
            <TabsTrigger value="flavor">Flavor</TabsTrigger>
            <TabsTrigger value="mouthfeel">Mouthfeel</TabsTrigger>
            <TabsTrigger value="overall">Overall</TabsTrigger>
          </TabsList>

          <TabsContent value="aroma" class="space-y-2">
            <Label for="aroma_notes">Aroma Notes</Label>
            <Textarea
              id="aroma_notes"
              v-model="formData.aroma_notes"
              placeholder="Malt character, hop aroma, fermentation character, other aromatics..."
              rows="4"
            />
          </TabsContent>

          <TabsContent value="appearance" class="space-y-2">
            <Label for="appearance_notes">Appearance Notes</Label>
            <Textarea
              id="appearance_notes"
              v-model="formData.appearance_notes"
              placeholder="Color, clarity, head formation, retention, texture..."
              rows="4"
            />
          </TabsContent>

          <TabsContent value="flavor" class="space-y-2">
            <Label for="flavor_notes">Flavor Notes</Label>
            <Textarea
              id="flavor_notes"
              v-model="formData.flavor_notes"
              placeholder="Malt flavor, hop flavor, bitterness, balance, finish, fermentation character..."
              rows="4"
            />
          </TabsContent>

          <TabsContent value="mouthfeel" class="space-y-2">
            <Label for="mouthfeel_notes">Mouthfeel Notes</Label>
            <Textarea
              id="mouthfeel_notes"
              v-model="formData.mouthfeel_notes"
              placeholder="Body, carbonation, warmth, creaminess, astringency..."
              rows="4"
            />
          </TabsContent>

          <TabsContent value="overall" class="space-y-2">
            <Label for="taste_notes">Overall Impression</Label>
            <Textarea
              id="taste_notes"
              v-model="formData.taste_notes"
              placeholder="Harmony, balance, drinkability, style accuracy, overall impression..."
              rows="4"
            />
          </TabsContent>
        </Tabs>

        <!-- Additional Notes -->
        <div>
          <Label for="notes">Additional Notes</Label>
          <Textarea
            id="notes"
            v-model="formData.notes"
            placeholder="Any additional observations or notes..."
            rows="3"
          />
        </div>

        <!-- Actions -->
        <DialogFooter>
          <Button type="button" variant="outline" @click="close">
            Cancel
          </Button>
          <Button type="submit" :disabled="saving">
            <Icon v-if="saving" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
            {{ saving ? 'Saving...' : (isEdit ? 'Update Test' : 'Create Test') }}
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Icon } from '#components'

interface QCTest {
  id?: number
  batch_id?: number
  test_date: string
  final_gravity?: number | null
  abv_actual?: number | null
  color?: string | null
  clarity?: string | null
  taste_notes?: string | null
  aroma_notes?: string | null
  appearance_notes?: string | null
  flavor_notes?: string | null
  mouthfeel_notes?: string | null
  score?: number | null
  aroma_score?: number | null
  appearance_score?: number | null
  flavor_score?: number | null
  mouthfeel_score?: number | null
  overall_impression_score?: number | null
  tester_name?: string | null
  notes?: string | null
}

const props = defineProps<{
  open: boolean
  batchId: number
  test?: QCTest | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'saved': [test: QCTest]
}>()

const isOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value)
})

const isEdit = computed(() => !!props.test?.id)
const saving = ref(false)

const formData = ref<QCTest>({
  test_date: new Date().toISOString().slice(0, 16),
  final_gravity: null,
  abv_actual: null,
  color: null,
  clarity: null,
  taste_notes: null,
  aroma_notes: null,
  appearance_notes: null,
  flavor_notes: null,
  mouthfeel_notes: null,
  score: null,
  aroma_score: null,
  appearance_score: null,
  flavor_score: null,
  mouthfeel_score: null,
  overall_impression_score: null,
  tester_name: null,
  notes: null,
})

// Watch for test prop changes to populate form
watch(() => props.test, (test) => {
  if (test) {
    formData.value = { ...test }
  } else {
    // Reset form
    formData.value = {
      test_date: new Date().toISOString().slice(0, 16),
      final_gravity: null,
      abv_actual: null,
      color: null,
      clarity: null,
      taste_notes: null,
      aroma_notes: null,
      appearance_notes: null,
      flavor_notes: null,
      mouthfeel_notes: null,
      score: null,
      aroma_score: null,
      appearance_score: null,
      flavor_score: null,
      mouthfeel_score: null,
      overall_impression_score: null,
      tester_name: null,
      notes: null,
    }
  }
}, { immediate: true })

const scoreCategory = computed(() => {
  const score = formData.value.score
  if (!score) return ''
  if (score >= 45) return 'Outstanding'
  if (score >= 38) return 'Excellent'
  if (score >= 30) return 'Very Good'
  if (score >= 21) return 'Good'
  if (score >= 14) return 'Fair'
  return 'Problematic'
})

const calculateTotalScore = () => {
  const {
    aroma_score,
    appearance_score,
    flavor_score,
    mouthfeel_score,
    overall_impression_score
  } = formData.value

  if (aroma_score !== null && 
      appearance_score !== null && 
      flavor_score !== null && 
      mouthfeel_score !== null && 
      overall_impression_score !== null) {
    formData.value.score = aroma_score + appearance_score + flavor_score + mouthfeel_score + overall_impression_score
  }
}

const useTemplate = () => {
  // Use BJCP standard template prompts
  formData.value.aroma_notes = 'Malt character:\nHop aroma:\nFermentation character:\nOther aromatics:'
  formData.value.appearance_notes = 'Color:\nClarity:\nHead (size, retention, texture):'
  formData.value.flavor_notes = 'Malt flavor:\nHop flavor:\nBitterness:\nBalance:\nFinish and aftertaste:\nFermentation character:'
  formData.value.mouthfeel_notes = 'Body:\nCarbonation:\nWarmth (alcohol):\nOther sensations:'
  formData.value.taste_notes = 'Harmony and balance:\nDrinkability:\nStyle accuracy:\nOverall impression:'
}

const handleSubmit = async () => {
  saving.value = true
  try {
    const apiUrl = useApiUrl()
    const url = isEdit.value 
      ? `${apiUrl}/qc-tests/${props.test?.id}`
      : `${apiUrl}/batches/${props.batchId}/qc-tests`
    
    const method = isEdit.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...formData.value,
        batch_id: props.batchId,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to save QC test')
    }

    const savedTest = await response.json()
    emit('saved', savedTest)
    close()
  } catch (error: any) {
    console.error('Error saving QC test:', error)
    alert(`Failed to save QC test: ${error.message}`)
  } finally {
    saving.value = false
  }
}

const close = () => {
  isOpen.value = false
}
</script>
