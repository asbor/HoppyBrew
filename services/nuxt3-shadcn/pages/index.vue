<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const { recipes, loading: recipesLoading, fetchAll: fetchRecipes } = useRecipes()
const { batches, loading: batchesLoading, fetchAll: fetchBatches, getActiveBatches } = useBatches()
const { 
  hops, fermentables, yeasts, miscs,
  fetchHops, fetchFermentables, fetchYeasts, fetchMiscs,
  getLowStockItems 
} = useInventory()

const loading = ref(true)
const error = ref<string | null>(null)

// Dashboard stats
const stats = computed(() => {
  const activeBatches = getActiveBatches()
  const lowStock = getLowStockItems(50) // threshold: 50g/ml
  
  return {
    totalRecipes: recipes.value.length,
    activeBatches: activeBatches.length,
    totalInventoryItems: hops.value.length + fermentables.value.length + yeasts.value.length + miscs.value.length,
    lowStockCount: lowStock.total,
    lastBrewDate: batches.value.length > 0 
      ? batches.value.sort((a, b) => new Date(b.brew_date || b.created_at).getTime() - new Date(a.brew_date || a.created_at).getTime())[0].brew_date 
      : null,
  }
})

// Recent batches (last 5)
const recentBatches = computed(() => {
  return batches.value
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5)
})

// Recent recipes (last 5)
const recentRecipes = computed(() => {
  return recipes.value
    .sort((a, b) => new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime())
    .slice(0, 5)
})

// Low stock items
const lowStockItems = computed(() => {
  const items = getLowStockItems(50)
  return [
    ...items.hops.map(h => ({ name: h.name, amount: h.amount, unit: h.unit, type: 'Hop' })),
    ...items.fermentables.map(f => ({ name: f.name, amount: f.amount, unit: f.unit, type: 'Fermentable' })),
    ...items.yeasts.map(y => ({ name: y.name, amount: y.amount, unit: y.unit, type: 'Yeast' })),
    ...items.miscs.map(m => ({ name: m.name, amount: m.amount, unit: m.unit, type: 'Misc' })),
  ].slice(0, 5)
})

// Status badge color helper - matching Home Assistant design system
function getBatchStatusColor(status: string) {
  const colors: Record<string, string> = {
    planning: 'bg-slate-500',        // Gray for planning/inactive
    brew_day: 'bg-amber-500',        // Amber for warning/in-progress
    primary_fermentation: 'bg-sky-500',     // Blue for active states
    secondary_fermentation: 'bg-blue-500',  // Deeper blue for secondary fermentation
    conditioning: 'bg-purple-500',   // Purple for special states
    packaged: 'bg-emerald-500',      // Green for success/completed
    completed: 'bg-green-600',       // Darker green for final completion
    archived: 'bg-gray-400',         // Light gray for archived
  }
  return colors[status] || 'bg-slate-500'
}

function formatDate(dateString: string | undefined) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-GB', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric' 
  })
}

// Load data on mount
onMounted(async () => {
  try {
    loading.value = true
    await Promise.all([
      fetchRecipes(),
      fetchBatches(),
      fetchHops(),
      fetchFermentables(),
      fetchYeasts(),
      fetchMiscs(),
    ])
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load dashboard data'
    console.error('Dashboard load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="grid w-full gap-6">
    <!-- Header -->
    <header class="flex items-start justify-between">
      <div class="grow">
        <p class="text-muted-foreground">Welcome back to HoppyBrew!</p>
        <h1 class="text-3xl font-bold">Dashboard</h1>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-muted-foreground">Loading dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-destructive">{{ error }}</p>
    </div>

    <!-- Main Content -->
    <main v-else class="grid w-full gap-6">
      <!-- Stats Cards -->
      <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Total Recipes</CardTitle>
            <Icon name="mdi:book-open-page-variant" class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ stats.totalRecipes }}</div>
            <p class="text-xs text-muted-foreground">
              Your recipe library
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Active Batches</CardTitle>
            <Icon name="mdi:beer" class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ stats.activeBatches }}</div>
            <p class="text-xs text-muted-foreground">
              Currently fermenting
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Inventory Items</CardTitle>
            <Icon name="mdi:package-variant" class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ stats.totalInventoryItems }}</div>
            <p class="text-xs text-muted-foreground">
              Total ingredients
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Low Stock Items</CardTitle>
            <Icon name="mdi:alert-circle" class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold" :class="stats.lowStockCount > 0 ? 'text-orange-500' : ''">
              {{ stats.lowStockCount }}
            </div>
            <p class="text-xs text-muted-foreground">
              Need restocking
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- Two Column Layout -->
      <div class="grid gap-6 md:grid-cols-2">
        <!-- Recent Batches -->
        <Card>
          <CardHeader>
            <CardTitle>Recent Batches</CardTitle>
            <CardDescription>Your latest brewing activity</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="recentBatches.length === 0" class="text-center py-8 text-muted-foreground">
              No batches yet. Start your first brew!
            </div>
            <div v-else class="space-y-4">
              <div v-for="batch in recentBatches" :key="batch.id" class="flex items-center justify-between">
                <div class="flex-1">
                  <NuxtLink :href="`/batches/${batch.id}`" class="font-medium hover:underline">
                    {{ batch.batch_name }}
                  </NuxtLink>
                  <p class="text-sm text-muted-foreground">{{ formatDate(batch.brew_date || batch.created_at) }}</p>
                </div>
                <Badge :class="getBatchStatusColor(batch.status)" class="text-white">
                  {{ batch.status.replace(/_/g, ' ') }}
                </Badge>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t">
              <Button asChild variant="outline" class="w-full">
                <NuxtLink href="/batches">View All Batches</NuxtLink>
              </Button>
            </div>
          </CardContent>
        </Card>

        <!-- Recent Recipes -->
        <Card>
          <CardHeader>
            <CardTitle>Recent Recipes</CardTitle>
            <CardDescription>Your latest recipe designs</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="recentRecipes.length === 0" class="text-center py-8 text-muted-foreground">
              No recipes yet. Create your first recipe!
            </div>
            <div v-else class="space-y-4">
              <div v-for="recipe in recentRecipes" :key="recipe.id" class="flex items-center justify-between">
                <div class="flex-1">
                  <NuxtLink :href="`/recipes/${recipe.id}`" class="font-medium hover:underline">
                    {{ recipe.name }}
                  </NuxtLink>
                  <p class="text-sm text-muted-foreground">
                    {{ recipe.type }} • {{ recipe.est_abv?.toFixed(1) }}% ABV • {{ recipe.ibu?.toFixed(0) }} IBU
                  </p>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t">
              <Button asChild variant="outline" class="w-full">
                <NuxtLink href="/recipes">View All Recipes</NuxtLink>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Low Stock Alert -->
      <Card v-if="lowStockItems.length > 0">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:alert-circle" class="h-5 w-5 text-orange-500" />
            Low Stock Alert
          </CardTitle>
          <CardDescription>These items need restocking soon</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <div v-for="(item, index) in lowStockItems" :key="index" class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <Badge variant="outline">{{ item.type }}</Badge>
                <span class="font-medium">{{ item.name }}</span>
              </div>
              <span class="text-sm text-muted-foreground">{{ item.amount }} {{ item.unit }}</span>
            </div>
          </div>
          <div class="mt-4 pt-4 border-t">
            <Button asChild variant="outline" class="w-full">
              <NuxtLink href="/inventory">Manage Inventory</NuxtLink>
            </Button>
          </div>
        </CardContent>
      </Card>

      <!-- Quick Actions -->
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common brewing tasks</CardDescription>
        </CardHeader>
        <CardContent class="grid gap-3 md:grid-cols-4">
          <Button asChild variant="default">
            <NuxtLink href="/recipes/newRecipe">
              <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
              New Recipe
            </NuxtLink>
          </Button>
          <Button asChild variant="default">
            <NuxtLink href="/batches/newBatch">
              <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
              New Batch
            </NuxtLink>
          </Button>
          <Button asChild variant="outline">
            <NuxtLink href="/tools">
              <Icon name="mdi:calculator" class="mr-2 h-4 w-4" />
              Calculators
            </NuxtLink>
          </Button>
          <Button asChild variant="outline">
            <NuxtLink href="/library">
              <Icon name="mdi:library" class="mr-2 h-4 w-4" />
              Recipe Library
            </NuxtLink>
          </Button>
        </CardContent>
      </Card>
    </main>
  </div>
</template>