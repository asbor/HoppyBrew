<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle 
} from '@/components/ui/dialog'
import type { Recipe } from '@/composables/useRecipes'
import type { BatchCreate } from '@/composables/useBatches'

const route = useRoute()
const router = useRouter()
const { fetchOne, update, loading: recipeLoading, error: recipeError } = useRecipes()
const { create: createBatch, loading: batchLoading } = useBatches()
const { generateBatchName } = useFormatters()

const recipeId = route.params.id as string
const recipe = ref<Recipe | null>(null)
const isLoading = computed(() => recipeLoading.value || batchLoading.value)

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
  try {
    const result = await fetchOne(recipeId)
    if (result.data.value) {
      recipe.value = result.data.value
      // Pre-fill batch form with recipe defaults
      batchForm.value.batch_name = generateBatchName(recipe.value.name)
      batchForm.value.batch_size = recipe.value.batch_size
      batchForm.value.brewer = recipe.value.brewer || ''
    }
    // If there's an error, it will be in result.error and handled by the template
  } catch (e) {
    // Catch any unexpected errors
    console.error('Error loading recipe:', e)
  }
})

async function handleUpdateRecipe() {
  if (!recipe.value) return
  
  const result = await update(recipeId, recipe.value)
  if (!result.error.value) {
    router.back()
  } else {
    alert(`Failed to update recipe: ${result.error.value}`)
  }
}

function handleCancel() {
  router.back()
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
  <div class="space-y-6">
    <!-- Header -->
    <header class="flex justify-between items-start">
      <div>
        <h1 class="text-3xl font-bold">Edit Recipe</h1>
        <p v-if="recipe" class="text-muted-foreground">{{ recipe.name }}</p>
      </div>
      <div class="flex gap-3">
        <Button @click="openStartBrewDialog" variant="default" :disabled="isLoading || !recipe">
          <Icon name="mdi:flask" class="mr-2 h-4 w-4" />
          Start Brew
        </Button>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading && !recipe" class="text-center py-12">
      <p class="text-muted-foreground">Loading recipe...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="recipeError" class="text-center py-12">
      <Card>
        <CardHeader>
          <CardTitle class="text-destructive">Error Loading Recipe</CardTitle>
          <CardDescription>{{ recipeError }}</CardDescription>
        </CardHeader>
        <CardFooter class="justify-center gap-2">
          <Button @click="router.back()" variant="outline">
            Go Back
          </Button>
          <Button @click="router.push('/recipes')">
            Back to Recipes
          </Button>
        </CardFooter>
      </Card>
    </div>

    <!-- Recipe Edit Form -->
    <form v-else-if="recipe" @submit.prevent="handleUpdateRecipe" class="space-y-6">
      <!-- Three columns -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Recipe Info</h3>
          <div class="space-y-3">
            <div>
              <Label for="name">Name</Label>
              <Input type="text" id="name" v-model="recipe.name" required />
            </div>
            <div>
              <Label for="brewer">Brewer</Label>
              <Input type="text" id="brewer" v-model="recipe.brewer" />
            </div>
            <div>
              <Label for="type">Type</Label>
              <Input type="text" id="type" v-model="recipe.type" required />
            </div>
          </div>
        </div>

        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Equipment</h3>
          <div class="space-y-3">
            <div>
              <Label for="batch_size">Batch Size (L)</Label>
              <Input type="number" step="0.1" id="batch_size" v-model.number="recipe.batch_size" required />
            </div>
            <div>
              <Label for="boil_size">Boil Size (L)</Label>
              <Input type="number" step="0.1" id="boil_size" v-model.number="recipe.boil_size" required />
            </div>
            <div>
              <Label for="boil_time">Boil Time (min)</Label>
              <Input type="number" id="boil_time" v-model.number="recipe.boil_time" required />
            </div>
            <div>
              <Label for="efficiency">Efficiency (%)</Label>
              <Input type="number" step="0.1" id="efficiency" v-model.number="recipe.efficiency" required />
            </div>
          </div>
        </div>

        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Style</h3>
          <div class="space-y-3">
            <div>
              <Label for="abv">ABV (%)</Label>
              <Input type="number" step="0.1" id="abv" v-model.number="recipe.abv" />
            </div>
            <div>
              <Label for="og">OG</Label>
              <Input type="number" step="0.001" id="og" v-model.number="recipe.og" />
            </div>
            <div>
              <Label for="fg">FG</Label>
              <Input type="number" step="0.001" id="fg" v-model.number="recipe.fg" />
            </div>
            <div>
              <Label for="ibu">IBU</Label>
              <Input type="number" step="0.1" id="ibu" v-model.number="recipe.ibu" />
            </div>
            <div>
              <Label for="est_color">EBC</Label>
              <Input type="number" step="0.1" id="est_color" v-model.number="recipe.est_color" />
            </div>
          </div>
        </div>
      </div>

      <!-- Ingredients Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Fermentables</h3>
          <div v-if="recipe.fermentables && recipe.fermentables.length > 0" class="space-y-2">
            <div v-for="(fermentable, index) in recipe.fermentables" :key="index" class="text-sm">
              {{ fermentable.name || 'Unnamed' }}
            </div>
          </div>
          <p v-else class="text-sm text-muted-foreground">No fermentables added</p>
        </div>

        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Hops</h3>
          <div v-if="recipe.hops && recipe.hops.length > 0" class="space-y-2">
            <div v-for="(hop, index) in recipe.hops" :key="index" class="text-sm">
              {{ hop.name || 'Unnamed' }}
            </div>
          </div>
          <p v-else class="text-sm text-muted-foreground">No hops added</p>
        </div>

        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Miscs</h3>
          <div v-if="recipe.miscs && recipe.miscs.length > 0" class="space-y-2">
            <div v-for="(misc, index) in recipe.miscs" :key="index" class="text-sm">
              {{ misc.name || 'Unnamed' }}
            </div>
          </div>
          <p v-else class="text-sm text-muted-foreground">No miscs added</p>
        </div>

        <div class="border-2 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-3">Yeasts</h3>
          <div v-if="recipe.yeasts && recipe.yeasts.length > 0" class="space-y-2">
            <div v-for="(yeast, index) in recipe.yeasts" :key="index" class="text-sm">
              {{ yeast.name || 'Unnamed' }}
            </div>
          </div>
          <p v-else class="text-sm text-muted-foreground">No yeasts added</p>
        </div>
      </div>

      <!-- Notes Section -->
      <div class="border-2 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3">Notes</h3>
        <textarea 
          id="notes" 
          v-model="recipe.notes" 
          rows="4"
          class="w-full border border-input rounded-lg p-2 bg-background"
          placeholder="Add brewing notes..."
        ></textarea>
      </div>

      <!-- Footer Actions -->
      <div class="flex justify-end gap-3">
        <Button type="button" variant="outline" @click="handleCancel">
          Cancel
        </Button>
        <Button type="submit" :disabled="isLoading">
          Save Changes
        </Button>
      </div>
    </form>

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
            <Input 
              id="batch_name" 
              v-model="batchForm.batch_name" 
              placeholder="My IPA - Batch 1"
              required
            />
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="batch_number">Batch Number</Label>
              <Input 
                id="batch_number" 
                v-model.number="batchForm.batch_number" 
                type="number"
                min="1"
                required
              />
            </div>
            
            <div class="space-y-2">
              <Label for="batch_size_form">Batch Size (L)</Label>
              <Input 
                id="batch_size_form" 
                v-model.number="batchForm.batch_size" 
                type="number"
                step="0.1"
                min="0"
                required
              />
            </div>
          </div>
          
          <div class="space-y-2">
            <Label for="batch_brewer">Brewer</Label>
            <Input 
              id="batch_brewer" 
              v-model="batchForm.brewer" 
              placeholder="Brewer name"
              required
            />
          </div>
          
          <div class="space-y-2">
            <Label for="brew_date">Brew Date</Label>
            <Input 
              id="brew_date" 
              v-model="batchForm.brew_date" 
              type="date"
              required
            />
          </div>
        </div>
        
        <DialogFooter>
          <Button 
            type="button" 
            variant="outline" 
            @click="showStartBrewDialog = false"
          >
            Cancel
          </Button>
          <Button 
            type="button" 
            @click="handleStartBrew"
            :disabled="batchLoading"
          >
            <Icon v-if="batchLoading" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
            Start Brewing
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
