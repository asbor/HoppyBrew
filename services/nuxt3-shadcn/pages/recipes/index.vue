<script setup lang="ts">
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import type { Recipe } from '@/composables/useRecipes'
import type { BatchCreate } from '@/composables/useBatches'

const router = useRouter()
const { recipes, loading, error, fetchAll, remove } = useRecipes()
const { create: createBatch, loading: batchLoading } = useBatches()
const { generateBatchName } = useFormatters()

const searchQuery = ref('')
const viewMode = ref<'table' | 'cards'>('table')

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

async function deleteRecipe(id: string) {
  if (!confirm('Are you sure you want to delete this recipe?')) {
    return
  }

  const result = await remove(id)
  if (result.error) {
    alert(`Failed to delete recipe: ${result.error.value}`)
  }
}

function formatNumber(value: number | undefined | null, decimals: number = 1): string {
  if (value === undefined || value === null) return 'N/A'
  return value.toFixed(decimals)
}

function openStartBrewDialog(recipe: Recipe) {
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

async function handleStartBrew() {
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

// Load recipes on mount
onMounted(async () => {
  await fetchAll()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold">Recipes</h1>
        <p class="text-muted-foreground">Your personal brewing recipe library</p>
      </div>
      <div class="flex gap-3">
        <Button as-child variant="outline">
          <NuxtLink href="/recipes/recipeCardWindow">
            <Icon name="mdi:view-grid" class="mr-2 h-4 w-4" />
            Card View
          </NuxtLink>
        </Button>
        <Button as-child>
          <NuxtLink href="/recipes/newRecipe">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            New Recipe
          </NuxtLink>
        </Button>
      </div>
    </header>

    <!-- Search & Filters -->
    <div class="flex flex-col md:flex-row gap-4">
      <div class="flex-1">
        <Input v-model="searchQuery" placeholder="Search recipes by name, type, or brewer..." class="max-w-md">
        <template #prefix>
          <Icon name="mdi:magnify" class="h-4 w-4 text-muted-foreground" />
        </template>
        </Input>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-muted-foreground">Loading recipes...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-destructive">{{ error }}</p>
    </div>

    <!-- Empty State -->
    <Card v-else-if="recipes.length === 0" class="text-center py-12">
      <CardHeader>
        <Icon name="mdi:book-open-page-variant" class="mx-auto h-12 w-12 text-muted-foreground" />
        <CardTitle>No recipes yet</CardTitle>
        <CardDescription>
          Start building your recipe library by creating your first recipe
        </CardDescription>
      </CardHeader>
      <CardFooter class="justify-center">
        <Button as-child>
          <NuxtLink href="/recipes/newRecipe">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Create First Recipe
          </NuxtLink>
        </Button>
      </CardFooter>
    </Card>

    <!-- Recipes Table -->
    <Card v-else>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Recipe List</CardTitle>
            <CardDescription>
              {{ filteredRecipes.length }} {{ filteredRecipes.length === 1 ? 'recipe' : 'recipes' }} found
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Batch Size</TableHead>
              <TableHead>ABV</TableHead>
              <TableHead>IBU</TableHead>
              <TableHead>SRM</TableHead>
              <TableHead>Efficiency</TableHead>
              <TableHead class="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="recipe in filteredRecipes" :key="recipe.id">
              <TableCell class="font-medium">
                <NuxtLink :to="`/recipes/${recipe.id}`" class="hover:underline">
                  {{ recipe.name }}
                </NuxtLink>
              </TableCell>
              <TableCell>
                <Badge variant="outline">{{ recipe.type }}</Badge>
              </TableCell>
              <TableCell>
                {{ formatNumber(recipe.batch_size, 0) }} L
              </TableCell>
              <TableCell>
                {{ formatNumber(recipe.est_abv) }}%
              </TableCell>
              <TableCell>
                {{ formatNumber(recipe.ibu, 0) }}
              </TableCell>
              <TableCell>
                {{ formatNumber(recipe.est_color, 0) }}
              </TableCell>
              <TableCell>
                {{ formatNumber(recipe.efficiency, 0) }}%
              </TableCell>
              <TableCell class="text-right space-x-2">
                <Button
variant="default" size="sm" title="Start brewing this recipe"
                  @click="openStartBrewDialog(recipe)">
                  <Icon name="mdi:flask" class="h-4 w-4" />
                </Button>
                <Button as-child variant="ghost" size="sm">
                  <NuxtLink :to="`/recipes/${recipe.id}`">
                    <Icon name="mdi:pencil" class="h-4 w-4" />
                  </NuxtLink>
                </Button>
                <Button
variant="ghost" size="sm" class="text-destructive hover:text-destructive"
                  @click="deleteRecipe(recipe.id)">
                  <Icon name="mdi:delete" class="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>

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
            <Input id="batch_name" v-model="batchForm.batch_name" placeholder="My IPA - Batch 1" required />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="batch_number">Batch Number</Label>
              <Input id="batch_number" v-model.number="batchForm.batch_number" type="number" min="1" required />
            </div>

            <div class="space-y-2">
              <Label for="batch_size_form">Batch Size (L)</Label>
              <Input
id="batch_size_form" v-model.number="batchForm.batch_size" type="number" step="0.1" min="0"
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
          <Button type="button" :disabled="batchLoading" @click="handleStartBrew">
            <Icon v-if="batchLoading" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
            Start Brewing
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
