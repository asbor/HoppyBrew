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

const { recipes, loading, error, fetchAll, remove } = useRecipes()

const searchQuery = ref('')
const viewMode = ref<'table' | 'cards'>('table')

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
        <Button asChild variant="outline">
          <NuxtLink href="/recipes/recipeCardWindow">
            <Icon name="mdi:view-grid" class="mr-2 h-4 w-4" />
            Card View
          </NuxtLink>
        </Button>
        <Button asChild>
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
        <Input
          v-model="searchQuery"
          placeholder="Search recipes by name, type, or brewer..."
          class="max-w-md"
        >
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
        <Button asChild>
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
                <NuxtLink :href="`/recipes/${recipe.id}`" class="hover:underline">
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
                <Button asChild variant="ghost" size="sm">
                  <NuxtLink :href="`/recipes/${recipe.id}`">
                    <Icon name="mdi:pencil" class="h-4 w-4" />
                  </NuxtLink>
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  @click="deleteRecipe(recipe.id)"
                  class="text-destructive hover:text-destructive"
                >
                  <Icon name="mdi:delete" class="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </div>
</template>
