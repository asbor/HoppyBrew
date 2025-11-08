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
import type { BatchStatus } from '@/composables/useBatches'

const router = useRouter()
const { batches, loading, error, fetchAll, remove } = useBatches()
const { getBatchStatusColor } = useStatusColors()

const searchQuery = ref('')
const filterStatus = ref<BatchStatus | 'all'>('all')
const viewMode = ref<'table' | 'cards'>('table')

// Filtered batches based on search and status
const filteredBatches = computed(() => {
  let result = batches.value

  // Filter by status
  if (filterStatus.value !== 'all') {
    result = result.filter(batch => batch.status === filterStatus.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(batch =>
      batch.batch_name.toLowerCase().includes(query)
    )
  }

  return result
})

function handleEditBatch(batch: any) {
  router.push(`/batches/${batch.id}`)
}

async function handleDeleteBatch(batch: any) {
  if (!confirm(`Are you sure you want to delete "${batch.batch_name}"?`)) {
    return
  }

  const result = await remove(batch.id)
  if (result.error) {
    alert(`Failed to delete batch: ${result.error.value}`)
  }
}

async function deleteBatch(id: string) {
  if (!confirm('Are you sure you want to delete this batch?')) {
    return
  }

  const result = await remove(id)
  if (result.error) {
    alert(`Failed to delete batch: ${result.error.value}`)
  }
}

function formatDate(dateString: string | undefined) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

function calculateDaysInStage(batch: any) {
  const statusDate = batch.fermentation_start_date || batch.brew_date || batch.created_at
  if (!statusDate) return 0

  const now = new Date()
  const start = new Date(statusDate)
  const diffTime = Math.abs(now.getTime() - start.getTime())
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

// Load batches on mount
onMounted(async () => {
  await fetchAll()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold">Batches</h1>
        <p class="text-muted-foreground">Track your brewing batches and fermentation progress</p>
      </div>
      <div class="flex gap-3">
        <div class="flex gap-1 border rounded-md">
          <Button 
            variant="ghost" 
            size="sm" 
            :class="{ 'bg-muted': viewMode === 'table' }"
            @click="viewMode = 'table'"
          >
            <Icon name="mdi:table" class="h-4 w-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            :class="{ 'bg-muted': viewMode === 'cards' }"
            @click="viewMode = 'cards'"
          >
            <Icon name="mdi:view-grid" class="h-4 w-4" />
          </Button>
        </div>
        <Button asChild>
          <NuxtLink href="/batches/newBatch">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            New Batch
          </NuxtLink>
        </Button>
      </div>
    </header>

    <!-- Search & Filters -->
    <div class="flex flex-col md:flex-row gap-4">
      <div class="flex-1">
        <Input v-model="searchQuery" placeholder="Search batches by name..." class="max-w-md">
        <template #prefix>
          <Icon name="mdi:magnify" class="h-4 w-4 text-muted-foreground" />
        </template>
        </Input>
      </div>
      <div class="flex gap-2 flex-wrap">
        <Button variant="outline" size="sm" :class="{ 'bg-primary text-primary-foreground': filterStatus === 'all' }"
          @click="filterStatus = 'all'">
          All
        </Button>
        <Button variant="outline" size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterStatus === 'planning' }"
          @click="filterStatus = 'planning'">
          Planning
        </Button>
        <Button variant="outline" size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterStatus === 'brewing' }"
          @click="filterStatus = 'brewing'">
          Brewing
        </Button>
        <Button variant="outline" size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterStatus === 'fermenting' }"
          @click="filterStatus = 'fermenting'">
          Fermenting
        </Button>
        <Button variant="outline" size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterStatus === 'conditioning' }"
          @click="filterStatus = 'conditioning'">
          Conditioning
        </Button>
        <Button variant="outline" size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterStatus === 'packaging' }"
          @click="filterStatus = 'packaging'">
          Packaging
        </Button>
        <Button variant="outline" size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterStatus === 'complete' }"
          @click="filterStatus = 'complete'">
          Complete
        </Button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-muted-foreground">Loading batches...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-destructive">{{ error }}</p>
    </div>

    <!-- Empty State -->
    <Card v-else-if="batches.length === 0" class="text-center py-12">
      <CardHeader>
        <Icon name="mdi:beer" class="mx-auto h-12 w-12 text-muted-foreground" />
        <CardTitle>No batches yet</CardTitle>
        <CardDescription>
          Start your first brew by creating a batch from a recipe
        </CardDescription>
      </CardHeader>
      <CardFooter class="justify-center">
        <Button asChild>
          <NuxtLink href="/batches/newBatch">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Create First Batch
          </NuxtLink>
        </Button>
      </CardFooter>
    </Card>

    <!-- Batches Table View -->
    <Card v-if="viewMode === 'table'">
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Batch List</CardTitle>
            <CardDescription>
              {{ filteredBatches.length }} {{ filteredBatches.length === 1 ? 'batch' : 'batches' }} found
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Batch Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Batch Size</TableHead>
              <TableHead>Brew Date</TableHead>
              <TableHead>Days in Stage</TableHead>
              <TableHead>OG</TableHead>
              <TableHead>FG</TableHead>
              <TableHead>ABV</TableHead>
              <TableHead class="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="batch in filteredBatches" :key="batch.id">
              <TableCell class="font-medium">
                <NuxtLink :href="`/batches/${batch.id}`" class="hover:underline">
                  {{ batch.batch_name }}
                </NuxtLink>
              </TableCell>
              <TableCell>
                <Badge :class="getBatchStatusColor(batch.status)" class="text-white">
                  {{ batch.status ? batch.status.replace(/_/g, ' ') : 'N/A' }}
                </Badge>
              </TableCell>
              <TableCell>{{ batch.batch_size }} L</TableCell>
              <TableCell>{{ formatDate(batch.brew_date || batch.created_at) }}</TableCell>
              <TableCell>{{ calculateDaysInStage(batch) }} days</TableCell>
              <TableCell>{{ batch.og?.toFixed(3) || 'N/A' }}</TableCell>
              <TableCell>{{ batch.fg?.toFixed(3) || 'N/A' }}</TableCell>
              <TableCell>{{ batch.abv?.toFixed(1) || 'N/A' }}%</TableCell>
              <TableCell class="text-right space-x-2">
                <Button asChild variant="ghost" size="sm">
                  <NuxtLink :href="`/batches/${batch.id}`">
                    <Icon name="mdi:pencil" class="h-4 w-4" />
                  </NuxtLink>
                </Button>
                <Button variant="ghost" size="sm" @click="deleteBatch(batch.id)"
                  class="text-destructive hover:text-destructive">
                  <Icon name="mdi:delete" class="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>

    <!-- Batches Card View -->
    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <BatchCard 
        v-for="batch in filteredBatches" 
        :key="batch.id"
        :batch="batch"
        @edit="handleEditBatch"
        @delete="handleDeleteBatch"
      />
    </div>
  </div>
</template>
