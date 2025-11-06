<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useBeerStyles, type BeerStyle, type StyleGuidelineSource, type StyleCategory } from '~/composables/useBeerStyles'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const props = defineProps<{
  styleId?: number
  initialData?: Partial<BeerStyle>
}>()

const emit = defineEmits<{
  saved: [style: BeerStyle]
  cancelled: []
}>()

const beerStylesApi = useBeerStyles()

// State
const loading = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)
const guidelineSources = ref<StyleGuidelineSource[]>([])
const categories = ref<StyleCategory[]>([])

// Form data
const formData = ref<Partial<BeerStyle>>({
  name: '',
  style_code: '',
  subcategory: '',
  guideline_source_id: undefined,
  category_id: undefined,
  abv_min: undefined,
  abv_max: undefined,
  og_min: undefined,
  og_max: undefined,
  fg_min: undefined,
  fg_max: undefined,
  ibu_min: undefined,
  ibu_max: undefined,
  color_min_srm: undefined,
  color_max_srm: undefined,
  color_min_ebc: undefined,
  color_max_ebc: undefined,
  description: '',
  aroma: '',
  appearance: '',
  flavor: '',
  mouthfeel: '',
  overall_impression: '',
  comments: '',
  history: '',
  ingredients: '',
  comparison: '',
  examples: '',
  ...props.initialData
})

// Validation
const isValid = computed(() => {
  return formData.value.name && formData.value.name.length > 0
})

// Fetch data
const fetchGuidelineSources = async () => {
  const response = await beerStylesApi.getGuidelineSources(true)
  if (response.data.value) {
    guidelineSources.value = response.data.value
  }
}

const fetchCategories = async (guidelineId: number) => {
  const response = await beerStylesApi.getCategories({ guideline_source_id: guidelineId })
  if (response.data.value) {
    categories.value = response.data.value
  }
}

// Load existing style if editing
const loadStyle = async () => {
  if (props.styleId) {
    loading.value = true
    const response = await beerStylesApi.getStyle(props.styleId)
    if (response.error.value) {
      error.value = response.error.value
    } else if (response.data.value) {
      formData.value = { ...response.data.value }
      if (formData.value.guideline_source_id) {
        await fetchCategories(formData.value.guideline_source_id)
      }
    }
    loading.value = false
  }
}

// Watch guideline source changes to load categories
watch(() => formData.value.guideline_source_id, (newVal) => {
  if (newVal) {
    fetchCategories(newVal)
    formData.value.category_id = undefined
  }
})

// Color conversion helpers
const convertSrmToEbc = (srm?: number) => {
  return srm ? srm * 1.97 : undefined
}

const convertEbcToSrm = (ebc?: number) => {
  return ebc ? ebc / 1.97 : undefined
}

watch(() => formData.value.color_min_srm, (newVal) => {
  formData.value.color_min_ebc = convertSrmToEbc(newVal)
})

watch(() => formData.value.color_max_srm, (newVal) => {
  formData.value.color_max_ebc = convertSrmToEbc(newVal)
})

// Save handler
const handleSave = async () => {
  if (!isValid.value) return
  
  saving.value = true
  error.value = null
  
  try {
    const response = props.styleId
      ? await beerStylesApi.updateStyle(props.styleId, formData.value)
      : await beerStylesApi.createStyle(formData.value as any)
    
    if (response.error.value) {
      error.value = response.error.value
    } else if (response.data.value) {
      emit('saved', response.data.value)
    }
  } finally {
    saving.value = false
  }
}

// Initialize
onMounted(async () => {
  await fetchGuidelineSources()
  if (props.styleId) {
    await loadStyle()
  }
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h2 class="text-2xl font-bold tracking-tight">
        {{ styleId ? 'Edit' : 'Create' }} Beer Style
      </h2>
      <p class="text-muted-foreground">
        {{ styleId ? 'Modify your custom beer style' : 'Create a new custom beer style' }}
      </p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="bg-destructive/15 text-destructive px-4 py-3 rounded-md">
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-muted-foreground">Loading style...</p>
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="handleSave" class="space-y-6">
      <Tabs default-value="basic">
        <TabsList class="grid w-full grid-cols-3">
          <TabsTrigger value="basic">Basic Info</TabsTrigger>
          <TabsTrigger value="parameters">Parameters</TabsTrigger>
          <TabsTrigger value="details">Details</TabsTrigger>
        </TabsList>

        <!-- Basic Information Tab -->
        <TabsContent value="basic" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <!-- Name -->
              <div class="space-y-2">
                <Label for="name">Style Name *</Label>
                <Input
                  id="name"
                  v-model="formData.name"
                  placeholder="e.g., American IPA"
                  required
                />
              </div>

              <!-- Style Code -->
              <div class="space-y-2">
                <Label for="style_code">Style Code</Label>
                <Input
                  id="style_code"
                  v-model="formData.style_code"
                  placeholder="e.g., 21A"
                />
              </div>

              <!-- Subcategory -->
              <div class="space-y-2">
                <Label for="subcategory">Subcategory</Label>
                <Input
                  id="subcategory"
                  v-model="formData.subcategory"
                  placeholder="e.g., West Coast IPA"
                />
              </div>

              <!-- Guideline Source -->
              <div class="space-y-2">
                <Label for="guideline_source">Guideline Source</Label>
                <Select v-model="formData.guideline_source_id">
                  <SelectTrigger>
                    <SelectValue placeholder="Select a guideline" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem 
                      v-for="source in guidelineSources" 
                      :key="source.id"
                      :value="source.id"
                    >
                      {{ source.name }} ({{ source.year }})
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <!-- Category -->
              <div v-if="formData.guideline_source_id" class="space-y-2">
                <Label for="category">Category</Label>
                <Select v-model="formData.category_id">
                  <SelectTrigger>
                    <SelectValue placeholder="Select a category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem 
                      v-for="category in categories" 
                      :key="category.id"
                      :value="category.id"
                    >
                      {{ category.code }} - {{ category.name }}
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Parameters Tab -->
        <TabsContent value="parameters" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Vital Statistics</CardTitle>
              <CardDescription>Define the characteristic ranges for this style</CardDescription>
            </CardHeader>
            <CardContent class="space-y-6">
              <!-- ABV -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="abv_min">ABV Min (%)</Label>
                  <Input
                    id="abv_min"
                    type="number"
                    step="0.1"
                    v-model.number="formData.abv_min"
                    placeholder="5.5"
                  />
                </div>
                <div class="space-y-2">
                  <Label for="abv_max">ABV Max (%)</Label>
                  <Input
                    id="abv_max"
                    type="number"
                    step="0.1"
                    v-model.number="formData.abv_max"
                    placeholder="7.5"
                  />
                </div>
              </div>

              <!-- OG -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="og_min">OG Min</Label>
                  <Input
                    id="og_min"
                    type="number"
                    step="0.001"
                    v-model.number="formData.og_min"
                    placeholder="1.056"
                  />
                </div>
                <div class="space-y-2">
                  <Label for="og_max">OG Max</Label>
                  <Input
                    id="og_max"
                    type="number"
                    step="0.001"
                    v-model.number="formData.og_max"
                    placeholder="1.070"
                  />
                </div>
              </div>

              <!-- FG -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="fg_min">FG Min</Label>
                  <Input
                    id="fg_min"
                    type="number"
                    step="0.001"
                    v-model.number="formData.fg_min"
                    placeholder="1.008"
                  />
                </div>
                <div class="space-y-2">
                  <Label for="fg_max">FG Max</Label>
                  <Input
                    id="fg_max"
                    type="number"
                    step="0.001"
                    v-model.number="formData.fg_max"
                    placeholder="1.014"
                  />
                </div>
              </div>

              <!-- IBU -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="ibu_min">IBU Min</Label>
                  <Input
                    id="ibu_min"
                    type="number"
                    v-model.number="formData.ibu_min"
                    placeholder="40"
                  />
                </div>
                <div class="space-y-2">
                  <Label for="ibu_max">IBU Max</Label>
                  <Input
                    id="ibu_max"
                    type="number"
                    v-model.number="formData.ibu_max"
                    placeholder="70"
                  />
                </div>
              </div>

              <!-- Color (SRM) -->
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <Label for="color_min_srm">Color Min (SRM)</Label>
                  <Input
                    id="color_min_srm"
                    type="number"
                    step="0.1"
                    v-model.number="formData.color_min_srm"
                    placeholder="6"
                  />
                  <p class="text-xs text-muted-foreground">
                    EBC: {{ convertSrmToEbc(formData.color_min_srm)?.toFixed(1) || 'N/A' }}
                  </p>
                </div>
                <div class="space-y-2">
                  <Label for="color_max_srm">Color Max (SRM)</Label>
                  <Input
                    id="color_max_srm"
                    type="number"
                    step="0.1"
                    v-model.number="formData.color_max_srm"
                    placeholder="14"
                  />
                  <p class="text-xs text-muted-foreground">
                    EBC: {{ convertSrmToEbc(formData.color_max_srm)?.toFixed(1) || 'N/A' }}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <!-- Details Tab -->
        <TabsContent value="details" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Style Characteristics</CardTitle>
              <CardDescription>Detailed descriptions of the style</CardDescription>
            </CardHeader>
            <CardContent class="space-y-4">
              <!-- Description -->
              <div class="space-y-2">
                <Label for="description">Overall Description</Label>
                <Textarea
                  id="description"
                  v-model="formData.description"
                  placeholder="General description of the style..."
                  rows="3"
                />
              </div>

              <!-- Aroma -->
              <div class="space-y-2">
                <Label for="aroma">Aroma</Label>
                <Textarea
                  id="aroma"
                  v-model="formData.aroma"
                  placeholder="Describe the aroma characteristics..."
                  rows="2"
                />
              </div>

              <!-- Appearance -->
              <div class="space-y-2">
                <Label for="appearance">Appearance</Label>
                <Textarea
                  id="appearance"
                  v-model="formData.appearance"
                  placeholder="Describe the visual characteristics..."
                  rows="2"
                />
              </div>

              <!-- Flavor -->
              <div class="space-y-2">
                <Label for="flavor">Flavor</Label>
                <Textarea
                  id="flavor"
                  v-model="formData.flavor"
                  placeholder="Describe the flavor profile..."
                  rows="2"
                />
              </div>

              <!-- Mouthfeel -->
              <div class="space-y-2">
                <Label for="mouthfeel">Mouthfeel</Label>
                <Textarea
                  id="mouthfeel"
                  v-model="formData.mouthfeel"
                  placeholder="Describe the mouthfeel and body..."
                  rows="2"
                />
              </div>

              <!-- Overall Impression -->
              <div class="space-y-2">
                <Label for="overall_impression">Overall Impression</Label>
                <Textarea
                  id="overall_impression"
                  v-model="formData.overall_impression"
                  placeholder="What makes this style unique..."
                  rows="2"
                />
              </div>

              <!-- Comments -->
              <div class="space-y-2">
                <Label for="comments">Comments</Label>
                <Textarea
                  id="comments"
                  v-model="formData.comments"
                  placeholder="Additional notes or comments..."
                  rows="2"
                />
              </div>

              <!-- History -->
              <div class="space-y-2">
                <Label for="history">History</Label>
                <Textarea
                  id="history"
                  v-model="formData.history"
                  placeholder="Historical background of the style..."
                  rows="2"
                />
              </div>

              <!-- Ingredients -->
              <div class="space-y-2">
                <Label for="ingredients">Characteristic Ingredients</Label>
                <Textarea
                  id="ingredients"
                  v-model="formData.ingredients"
                  placeholder="Typical ingredients used in this style..."
                  rows="2"
                />
              </div>

              <!-- Examples -->
              <div class="space-y-2">
                <Label for="examples">Commercial Examples</Label>
                <Textarea
                  id="examples"
                  v-model="formData.examples"
                  placeholder="Comma-separated list of commercial examples..."
                  rows="2"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <!-- Action Buttons -->
      <Card>
        <CardFooter class="flex justify-between pt-6">
          <Button 
            type="button" 
            variant="outline"
            @click="emit('cancelled')"
            :disabled="saving"
          >
            Cancel
          </Button>
          <Button 
            type="submit"
            :disabled="!isValid || saving"
          >
            {{ saving ? 'Saving...' : (styleId ? 'Update Style' : 'Create Style') }}
          </Button>
        </CardFooter>
      </Card>
    </form>
  </div>
</template>
