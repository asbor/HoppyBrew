<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
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

const router = useRouter()
const { recipes, loading, error, fetchAll, remove } = useRecipes()
const { create: createBatch, loading: batchLoading } = useBatches()
const { generateBatchName } = useFormatters()

const searchQuery = ref('')

// Start Brew Dialog state
const showStartBrewDialog = ref(false)
const selectedRecipe = ref<Recipe | null>(null)
const batchForm = ref<Partial<BatchCreate>>({
  batch_name: '',
  batch_number: 1,
  batch_size: 0,
  brewer: '',
  brew_date: new Date().toISOString().split('T')[0]
})

// Filtered recipes based on search
const filteredRecipes = computed(() => {
  if (!searchQuery.value) return recipes.value
  
  const query = searchQuery.value.toLowerCase()
  return recipes.value.filter(recipe =>
    recipe.name.toLowerCase().includes(query) ||
    recipe.type.toLowerCase().includes(query) ||
    recipe.brewer?.toLowerCase().includes(query)
  )
})

function handleStartBrew(recipe: Recipe) {
  selectedRecipe.value = recipe
  batchForm.value = {
    batch_name: generateBatchName(recipe.name),
    batch_number: 1,
    batch_size: recipe.batch_size,
    brewer: recipe.brewer || '',
    brew_date: new Date().toISOString().split('T')[0]
  }
  showStartBrewDialog.value = true
}

function handleEdit(recipe: Recipe) {
  router.push(`/recipes/${recipe.id}`)
}

async function handleDelete(recipe: Recipe) {
  if (!confirm(`Are you sure you want to delete "${recipe.name}"?`)) {
    return
  }

  const result = await remove(recipe.id)
  if (result.error) {
    alert(`Failed to delete recipe: ${result.error.value}`)
  }
}

async function confirmStartBrew() {
  if (!selectedRecipe.value) return
  
  const batchData: BatchCreate = {
    recipe_id: selectedRecipe.value.id,
    batch_name: batchForm.value.batch_name || `${selectedRecipe.value.name} Batch`,
    batch_number: batchForm.value.batch_number || 1,
    batch_size: batchForm.value.batch_size || selectedRecipe.value.batch_size,
    brewer: batchForm.value.brewer || selectedRecipe.value.brewer || 'Unknown',
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

onMounted(async () => {
  await fetchAll()
})
</script>

<template>
    <div class="space-y-6">
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <h1 class="text-3xl font-bold">Recipes</h1>
                <p class="text-muted-foreground">Your personal brewing recipe library</p>
            </div>
            <div class="flex gap-3">
                <Button asChild variant="outline">
                    <NuxtLink href="/recipes">
                        <Icon name="mdi:table" class="mr-2 h-4 w-4" />
                        Table View
                    </NuxtLink>
                </Button>
                <ProductNewDialog />
                <BeerXMLImportRecipeDialog />
            </div>
        </header>
        
        <main class="space-y-4">
            <!-- Search Bar -->
            <div>
                <Input 
                    v-model="searchQuery"
                    type="text" 
                    placeholder="Search for recipe by name, type, or brewer..."
                    class="max-w-md"
                >
                    <template #prefix>
                        <Icon name="mdi:magnify" class="h-4 w-4 text-muted-foreground" />
                    </template>
                </Input>
            </div>
            
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-12">
                <p class="text-muted-foreground">Loading recipes...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="text-center py-12">
                <p class="text-destructive">Error loading recipes: {{ error }}</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="filteredRecipes.length === 0" class="text-center py-12">
                <Icon name="mdi:book-open-page-variant" class="mx-auto h-12 w-12 text-muted-foreground" />
                <h3 class="mt-4 text-lg font-semibold">No recipes found</h3>
                <p class="text-muted-foreground">
                    {{ searchQuery ? 'Try a different search term' : 'Start building your recipe library' }}
                </p>
            </div>

            <!-- Recipe Cards Grid -->
            <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <BeerCard 
                    v-for="recipe in filteredRecipes" 
                    :card="recipe" 
                    :key="recipe.id"
                    @start-brew="handleStartBrew"
                    @edit="handleEdit"
                    @delete="handleDelete"
                />
            </div>
        </main>

        <!-- Start Brew Dialog -->
        <Dialog v-model:open="showStartBrewDialog">
            <DialogContent class="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Start New Brew Batch</DialogTitle>
                    <DialogDescription>
                        Create a new batch from "{{ selectedRecipe?.name }}" and begin brewing
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
                        @click="confirmStartBrew"
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