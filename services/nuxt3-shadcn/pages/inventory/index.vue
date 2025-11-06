<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Badge } from '~/components/ui/badge'
import { Button } from '~/components/ui/button'
import { Alert, AlertDescription } from '~/components/ui/alert'

const inventory = useInventory()

// Fetch all inventory on mount
onMounted(async () => {
  await Promise.all([
    inventory.fetchFermentables(),
    inventory.fetchHops(),
    inventory.fetchYeasts(),
    inventory.fetchMiscs(),
  ])
})

// Low stock threshold - TODO: Make this configurable via app settings
// Different ingredient types may require different thresholds
const LOW_STOCK_THRESHOLD = {
  fermentables: 1000, // grams
  hops: 100,         // grams
  yeasts: 1,         // packages
  miscs: 100,        // grams
}

// Computed stats
const inventoryStats = computed(() => ({
  fermentables: {
    total: inventory.fermentables.value.length,
    lowStock: inventory.fermentables.value.filter(f => f.amount < LOW_STOCK_THRESHOLD.fermentables).length,
    totalAmount: inventory.fermentables.value.reduce((sum, f) => sum + f.amount, 0),
  },
  hops: {
    total: inventory.hops.value.length,
    lowStock: inventory.hops.value.filter(h => h.amount < LOW_STOCK_THRESHOLD.hops).length,
    totalAmount: inventory.hops.value.reduce((sum, h) => sum + h.amount, 0),
  },
  yeasts: {
    total: inventory.yeasts.value.length,
    lowStock: inventory.yeasts.value.filter(y => y.amount < LOW_STOCK_THRESHOLD.yeasts).length,
    totalAmount: inventory.yeasts.value.reduce((sum, y) => sum + y.amount, 0),
  },
  miscs: {
    total: inventory.miscs.value.length,
    lowStock: inventory.miscs.value.filter(m => m.amount < LOW_STOCK_THRESHOLD.miscs).length,
    totalAmount: inventory.miscs.value.reduce((sum, m) => sum + m.amount, 0),
  },
}))

const totalLowStock = computed(() => 
  inventoryStats.value.fermentables.lowStock +
  inventoryStats.value.hops.lowStock +
  inventoryStats.value.yeasts.lowStock +
  inventoryStats.value.miscs.lowStock
)
</script>

<template>
  <div class="container mx-auto py-6 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Inventory Management</h1>
        <p class="text-muted-foreground">Track and manage your brewing ingredients</p>
      </div>
    </div>

    <!-- Low Stock Alert -->
    <Alert v-if="totalLowStock > 0" variant="warning" class="border-yellow-600">
      <AlertDescription>
        <strong>Low Stock Warning:</strong> {{ totalLowStock }} item(s) running low. 
        Check individual categories for details.
      </AlertDescription>
    </Alert>

    <!-- Inventory Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Fermentables Card -->
      <Card class="hover:shadow-lg transition-shadow cursor-pointer">
        <NuxtLink href="/inventory/fermentables" class="block">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Fermentables</CardTitle>
            <Icon size="24" name="mdi:wheat" class="text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ inventoryStats.fermentables.total }}</div>
            <p class="text-xs text-muted-foreground">
              {{ inventoryStats.fermentables.totalAmount.toFixed(0) }}g total stock
            </p>
            <Badge v-if="inventoryStats.fermentables.lowStock > 0" variant="warning" class="mt-2">
              {{ inventoryStats.fermentables.lowStock }} low stock
            </Badge>
          </CardContent>
        </NuxtLink>
      </Card>

      <!-- Hops Card -->
      <Card class="hover:shadow-lg transition-shadow cursor-pointer">
        <NuxtLink href="/inventory/hops" class="block">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Hops</CardTitle>
            <Icon size="24" name="mdi:hops" class="text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ inventoryStats.hops.total }}</div>
            <p class="text-xs text-muted-foreground">
              {{ inventoryStats.hops.totalAmount.toFixed(0) }}g total stock
            </p>
            <Badge v-if="inventoryStats.hops.lowStock > 0" variant="warning" class="mt-2">
              {{ inventoryStats.hops.lowStock }} low stock
            </Badge>
          </CardContent>
        </NuxtLink>
      </Card>

      <!-- Yeasts Card -->
      <Card class="hover:shadow-lg transition-shadow cursor-pointer">
        <NuxtLink href="/inventory/yeasts" class="block">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Yeasts</CardTitle>
            <Icon size="24" name="mdi:yeast" class="text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ inventoryStats.yeasts.total }}</div>
            <p class="text-xs text-muted-foreground">
              {{ inventoryStats.yeasts.totalAmount.toFixed(0) }} units
            </p>
            <Badge v-if="inventoryStats.yeasts.lowStock > 0" variant="warning" class="mt-2">
              {{ inventoryStats.yeasts.lowStock }} low stock
            </Badge>
          </CardContent>
        </NuxtLink>
      </Card>

      <!-- Miscs Card -->
      <Card class="hover:shadow-lg transition-shadow cursor-pointer">
        <NuxtLink href="/inventory/miscs" class="block">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Miscellaneous</CardTitle>
            <Icon size="24" name="healthicons:sugar-alt" class="text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ inventoryStats.miscs.total }}</div>
            <p class="text-xs text-muted-foreground">
              {{ inventoryStats.miscs.totalAmount.toFixed(0) }}g total stock
            </p>
            <Badge v-if="inventoryStats.miscs.lowStock > 0" variant="warning" class="mt-2">
              {{ inventoryStats.miscs.lowStock }} low stock
            </Badge>
          </CardContent>
        </NuxtLink>
      </Card>
    </div>

    <!-- Quick Actions -->
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
        <CardDescription>Manage your brewing ingredients efficiently</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Button asChild variant="outline" class="h-auto py-4">
            <NuxtLink href="/inventory/fermentables/newFermentable" class="flex flex-col items-center gap-2">
              <Icon size="24" name="mdi:plus-circle" />
              <span class="text-sm">Add Fermentable</span>
            </NuxtLink>
          </Button>
          <Button asChild variant="outline" class="h-auto py-4">
            <NuxtLink href="/inventory/hops/newHop" class="flex flex-col items-center gap-2">
              <Icon size="24" name="mdi:plus-circle" />
              <span class="text-sm">Add Hop</span>
            </NuxtLink>
          </Button>
          <Button asChild variant="outline" class="h-auto py-4">
            <NuxtLink href="/inventory/yeasts/newYeast" class="flex flex-col items-center gap-2">
              <Icon size="24" name="mdi:plus-circle" />
              <span class="text-sm">Add Yeast</span>
            </NuxtLink>
          </Button>
          <Button asChild variant="outline" class="h-auto py-4">
            <NuxtLink href="/inventory/miscs/newMisc" class="flex flex-col items-center gap-2">
              <Icon size="24" name="mdi:plus-circle" />
              <span class="text-sm">Add Misc</span>
            </NuxtLink>
          </Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>