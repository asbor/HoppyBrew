<script setup lang="ts">
import { ChevronLeft, Edit, Copy, Play } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import type { Recipe } from '@/composables/useRecipes'
import type { BatchCreate } from '@/composables/useBatches'

const route = useRoute()
const router = useRouter()
const { fetchOne, loading: recipeLoading, error: recipeError } = useRecipes()
const { create: createBatch, loading: batchLoading } = useBatches()
const { generateBatchName } = useFormatters()

const recipeId = route.params.id as string
const recipe = ref<Recipe | null>(null)
const isLoading = computed(() => recipeLoading.value)

// Start Brew Dialog state
const showStartBrewDialog = ref(false)
const batchForm = ref<Partial<BatchCreate>>({
  batch_name: '',
  batch_number: 1,
  batch_size: 0,
  brewer: '',
  brew_date: new Date().toISOString().split('T')[0]
})

// Load recipe on mount
onMounted(async () => {
  const result = await fetchOne(recipeId)
  if (result.data.value) {
    recipe.value = result.data.value
    // Pre-fill batch form with recipe defaults
    batchForm.value.batch_name = generateBatchName(recipe.value.name)
    batchForm.value.batch_size = recipe.value.batch_size
    batchForm.value.brewer = recipe.value.brewer || ''
  } else if (result.error.value) {
    // Handle error - recipe not found or API error
    console.error('Failed to load recipe:', result.error.value)
  }
})

// Set page title
useHead({
  title: computed(() => recipe.value ? `${recipe.value.name} - Recipe` : 'Recipe Details')
})

// Action handlers
const editRecipe = () => {
  router.push(`/recipes/${recipeId}/edit`)
}

const cloneRecipe = () => {
  // TODO: Implement clone functionality
  console.log('Clone recipe:', recipeId)
}

function openStartBrewDialog() {
  if (recipe.value) {
    // Refresh batch form with latest recipe data
    batchForm.value.batch_name = generateBatchName(recipe.value.name)
    batchForm.value.batch_size = recipe.value.batch_size
    batchForm.value.brewer = recipe.value.brewer || ''
  }
  showStartBrewDialog.value = true
}

async function handleStartBrew() {
  if (!recipe.value) return

  const batchData: BatchCreate = {
    recipe_id: recipeId,
    batch_name: batchForm.value.batch_name || `${recipe.value.name} Batch`,
    batch_number: batchForm.value.batch_number || 1,
    batch_size: batchForm.value.batch_size || recipe.value.batch_size,
    brewer: batchForm.value.brewer || recipe.value.brewer || 'Unknown',
    brew_date: batchForm.value.brew_date || new Date().toISOString()
  }

  const result = await createBatch(batchData)

  if (!result.error.value && result.data.value) {
    showStartBrewDialog.value = false
    // Navigate to the new batch detail page
    router.push(`/batches/${result.data.value.id}`)
  } else {
    alert(`Failed to create batch: ${result.error.value}`)
  }
}
</script>

<template>
  <div class="container mx-auto p-6">
    <!-- Loading State -->
    <div v-if="isLoading && !recipe" class="flex justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
        <p class="mt-4 text-gray-600">Loading recipe...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="recipeError" class="text-center">
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <strong class="font-bold">Error!</strong>
        <span class="block sm:inline">{{ recipeError }}</span>
      </div>
      <nuxt-link to="/recipes" class="mt-4 inline-block text-blue-600 hover:text-blue-800">
        ← Back to Recipes
      </nuxt-link>
    </div>

    <!-- Recipe Detail View -->
    <div v-else-if="recipe" class="space-y-6">
      <!-- Header with Recipe Actions -->
      <div class="flex justify-between items-start">
        <div>
          <div class="flex items-center space-x-4 mb-2">
            <nuxt-link to="/recipes" class="text-blue-600 hover:text-blue-800 flex items-center">
              <ChevronLeft class="h-4 w-4 mr-1" />
              Back to Recipes
            </nuxt-link>
          </div>
          <h1 class="text-3xl font-bold text-gray-900">{{ recipe.name }}</h1>
          <p v-if="recipe.type" class="text-lg text-gray-600 mt-1">{{ recipe.type }}</p>
        </div>

        <div class="flex space-x-2">
          <Button variant="outline" @click="editRecipe">
            <Edit class="h-4 w-4 mr-2" />
            Edit
          </Button>
          <Button variant="outline" @click="cloneRecipe">
            <Copy class="h-4 w-4 mr-2" />
            Clone
          </Button>
          <Button @click="openStartBrewDialog" class="bg-green-600 hover:bg-green-700">
            <Play class="h-4 w-4 mr-2" />
            Start Batch
          </Button>
        </div>
      </div>

      <!-- Recipe Overview Block -->
      <RecipeBlock v-if="recipe" :recipe="recipe" />

      <!-- Recipe Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg border p-4 text-center">
          <div class="text-2xl font-bold text-blue-600">
            {{ recipe.abv?.toFixed(1) || recipe.est_abv?.toFixed(1) || '--' }}%
          </div>
          <div class="text-sm text-gray-600">ABV</div>
        </div>
        <div class="bg-white rounded-lg border p-4 text-center">
          <div class="text-2xl font-bold text-amber-600">
            {{ recipe.ibu?.toFixed(0) || '--' }}
          </div>
          <div class="text-sm text-gray-600">IBU</div>
        </div>
        <div class="bg-white rounded-lg border p-4 text-center">
          <div class="text-2xl font-bold text-orange-600">
            {{ recipe.est_color?.toFixed(0) || '--' }}
          </div>
          <div class="text-sm text-gray-600">SRM</div>
        </div>
        <div class="bg-white rounded-lg border p-4 text-center">
          <div class="text-2xl font-bold text-green-600">
            {{ recipe.og?.toFixed(3) || recipe.est_og?.toFixed(3) || '--' }}
          </div>
          <div class="text-sm text-gray-600">OG</div>
        </div>
      </div>

      <!-- Ingredients Sections -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Fermentables -->
        <FermentablesBlock v-if="recipe.fermentables && recipe.fermentables.length > 0"
          :fermentables="recipe.fermentables" />

        <!-- Hops -->
        <HopsBlock v-if="recipe.hops && recipe.hops.length > 0" :hops="recipe.hops" />

        <!-- Yeasts -->
        <YeastBlock v-if="recipe.yeasts && recipe.yeasts.length > 0" :yeasts="recipe.yeasts" />

        <!-- Miscs -->
        <MiscsBlock v-if="recipe.miscs && recipe.miscs.length > 0" :miscs="recipe.miscs" />
      </div>

      <!-- Additional Information Blocks -->
      <div class="space-y-6">
        <EquipmentBlock v-if="recipe.equipment_profiles" :equipment="recipe.equipment_profiles" />
        <StyleBlock v-if="recipe.style_profile || recipe.style_guideline" :style-profile="recipe.style_profile"
          :style-guideline="recipe.style_guideline" />
        <WaterBlock v-if="recipe.water_profiles" :water="recipe.water_profiles" />
        <MashBlock v-if="recipe.mash_profile" :mash="recipe.mash_profile" />
        <FermentationBlock :recipe="recipe" />
        <NotesBlock :recipe="recipe" />
      </div>
    </div>

    <!-- Start Brew Dialog -->
    <Dialog v-model:open="showStartBrewDialog">
      <DialogContent class="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Start New Brew Batch</DialogTitle>
          <DialogDescription>
            Create a new batch from this recipe and begin brewing
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="batch_name">Batch Name</Label>
            <Input id="batch_name" v-model="batchForm.batch_name" placeholder="My IPA - Batch 1" required />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="batch_number">Batch Number</Label>
              <Input id="batch_number" v-model.number="batchForm.batch_number" type="number" min="1" required />
            </div>

            <div class="space-y-2">
              <Label for="batch_size_form">Batch Size (L)</Label>
              <Input id="batch_size_form" v-model.number="batchForm.batch_size" type="number" step="0.1" min="0"
                required />
            </div>
          </div>

          <div class="space-y-2">
            <Label for="batch_brewer">Brewer</Label>
            <Input id="batch_brewer" v-model="batchForm.brewer" placeholder="Brewer name" required />
          </div>

          <div class="space-y-2">
            <Label for="brew_date">Brew Date</Label>
            <Input id="brew_date" v-model="batchForm.brew_date" type="date" required />
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" @click="showStartBrewDialog = false">
            Cancel
          </Button>
          <Button type="button" @click="handleStartBrew" :disabled="batchLoading">
            <Icon v-if="batchLoading" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
            Start Brewing
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
