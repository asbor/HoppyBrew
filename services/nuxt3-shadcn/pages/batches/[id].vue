<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-96">
      <div class="text-center space-y-4">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto"></div>
        <p class="text-muted-foreground">Loading batch details...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <Card>
        <CardHeader>
          <Icon name="mdi:alert-circle" class="mx-auto h-12 w-12 text-red-500" />
          <CardTitle class="text-red-600">Error Loading Batch</CardTitle>
          <CardDescription>{{ error }}</CardDescription>
        </CardHeader>
        <CardFooter class="justify-center">
          <Button @click="fetchBatch" variant="outline">
            <Icon name="mdi:refresh" class="mr-2 h-4 w-4" />
            Try Again
          </Button>
        </CardFooter>
      </Card>
    </div>

    <!-- Main Content -->
    <template v-else-if="currentBatch">
      <!-- Header -->
      <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <Button variant="ghost" size="sm" @click="$router.push('/batches')">
              <Icon name="mdi:arrow-left" class="h-4 w-4" />
            </Button>
            <h1 class="text-3xl font-bold">{{ currentBatch.batch_name }}</h1>
            <Badge :class="getBatchStatusColor(currentBatch.status)" class="text-white">
              {{ formatStatus(currentBatch.status) }}
            </Badge>
          </div>
          <p class="text-muted-foreground">
            Batch #{{ currentBatch.batch_number }} • {{ currentBatch.batch_size }}L • 
            Brewed {{ formatDate(currentBatch.brew_date || currentBatch.created_at) }}
          </p>
        </div>
        <div class="flex gap-2">
          <Button @click="showEditDialog = true" variant="outline">
            <Icon name="mdi:pencil" class="mr-2 h-4 w-4" />
            Edit Batch
          </Button>
          <Button @click="duplicateBatch" variant="outline">
            <Icon name="mdi:content-copy" class="mr-2 h-4 w-4" />
            Duplicate
          </Button>
        </div>
      </header>

      <!-- Batch Phase Navigation -->
      <Card>
        <CardContent class="p-6">
          <BatchPhaseNavigation 
            :current-phase="currentBatch.status" 
            @phase-change="handlePhaseChange"
          />
        </CardContent>
      </Card>

      <!-- Phase Content -->
      <div class="grid gap-6">
        <!-- Planning Phase -->
        <template v-if="currentBatch.status === 'planning'">
          <BatchPlanningPhase 
            :batch="currentBatch" 
            @start-brew="startBrewDay"
            @update-batch="handleBatchUpdate"
          />
        </template>

        <!-- Brew Day Phase -->
        <template v-else-if="currentBatch.status === 'brew_day'">
          <BatchBrewingPhase 
            :batch="currentBatch"
            @start-fermentation="startFermentation"
            @update-batch="handleBatchUpdate"
          />
        </template>

        <!-- Fermentation Phases -->
        <template v-else-if="['primary_fermentation', 'secondary_fermentation'].includes(currentBatch.status)">
          <BatchFermentationPhase 
            :batch="currentBatch"
            @start-conditioning="startConditioning"
            @update-batch="handleBatchUpdate"
          />
        </template>

        <!-- Conditioning Phase -->
        <template v-else-if="currentBatch.status === 'conditioning'">
          <BatchConditioningPhase 
            :batch="currentBatch"
            @package-batch="packageBatch"
            @update-batch="handleBatchUpdate"
          />
        </template>

        <!-- Packaged Phase -->
        <template v-else-if="currentBatch.status === 'packaged'">
          <BatchPackagedPhase 
            :batch="currentBatch"
            @complete-batch="completeBatch"
            @update-batch="handleBatchUpdate"
          />
        </template>

        <!-- Completed Phase -->
        <template v-else-if="['completed', 'archived'].includes(currentBatch.status)">
          <BatchCompletedPhase 
            :batch="currentBatch"
            @archive-batch="archiveBatch"
            @update-batch="handleBatchUpdate"
          />
        </template>
      </div>

      <!-- Quick Actions Sidebar -->
      <Card class="sticky top-4">
        <CardHeader>
          <CardTitle class="text-lg">Quick Actions</CardTitle>
        </CardHeader>
        <CardContent class="space-y-3">
          <Button @click="addReading" class="w-full" variant="outline">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Add Reading
          </Button>
          <Button @click="addNote" class="w-full" variant="outline">
            <Icon name="mdi:note-plus" class="mr-2 h-4 w-4" />
            Add Note
          </Button>
          <Button @click="generateBrewSheet" class="w-full" variant="outline">
            <Icon name="mdi:printer" class="mr-2 h-4 w-4" />
            Brew Sheet
          </Button>
          <Button @click="exportData" class="w-full" variant="outline">
            <Icon name="mdi:download" class="mr-2 h-4 w-4" />
            Export Data
          </Button>
        </CardContent>
      </Card>

      <!-- Edit Batch Dialog -->
      <BatchEditDialog 
        v-model:open="showEditDialog"
        :batch="currentBatch"
        @save="handleBatchUpdate"
      />

      <!-- Add Reading Dialog -->
      <BatchReadingDialog 
        v-model:open="showReadingDialog"
        :batch-id="currentBatch.id"
        @save="handleReadingAdded"
      />

      <!-- Add Note Dialog -->
      <BatchNoteDialog 
        v-model:open="showNoteDialog"
        :batch-id="currentBatch.id"
        @save="handleNoteAdded"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Icon } from '#components'

// Import batch phase components
import BatchPhaseNavigation from '@/components/batch/BatchPhaseNavigation.vue'
import BatchPlanningPhase from '@/components/batch/BatchPlanningPhase.vue'
import BatchBrewingPhase from '@/components/batch/BatchBrewingPhase.vue'
import BatchFermentationPhase from '@/components/batch/BatchFermentationPhase.vue'
import BatchConditioningPhase from '@/components/batch/BatchConditioningPhase.vue'
import BatchPackagedPhase from '@/components/batch/BatchPackagedPhase.vue'
import BatchCompletedPhase from '@/components/batch/BatchCompletedPhase.vue'

// Import dialogs
import BatchEditDialog from '@/components/batch/BatchEditDialog.vue'
import BatchReadingDialog from '@/components/batch/BatchReadingDialog.vue'
import BatchNoteDialog from '@/components/batch/BatchNoteDialog.vue'

const route = useRoute()
const router = useRouter()
const { fetchOne, currentBatch, loading, error, update: updateBatch, updateStatus } = useBatches()
const { getBatchStatusColor } = useStatusColors()

const batchId = route.params.id as string

// Dialog states
const showEditDialog = ref(false)
const showReadingDialog = ref(false)
const showNoteDialog = ref(false)

// Fetch batch data
const fetchBatch = async () => {
  if (batchId) {
    await fetchOne(batchId)
  }
}

// Format helpers
const formatStatus = (status: string) => {
  return status.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())
}

const formatDate = (date: string | Date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit', 
    year: 'numeric'
  })
}

// Phase transition handlers
const handlePhaseChange = async (newPhase: string) => {
  if (currentBatch.value) {
    await updateStatus(currentBatch.value.id, newPhase)
  }
}

const startBrewDay = async () => {
  await handlePhaseChange('brew_day')
}

const startFermentation = async () => {
  await handlePhaseChange('primary_fermentation')
}

const startConditioning = async () => {
  await handlePhaseChange('conditioning')
}

const packageBatch = async () => {
  await handlePhaseChange('packaged')
}

const completeBatch = async () => {
  await handlePhaseChange('completed')
}

const archiveBatch = async () => {
  await handlePhaseChange('archived')
}

// Update handlers
const handleBatchUpdate = async (updatedData: any) => {
  if (currentBatch.value) {
    await updateBatch(currentBatch.value.id, updatedData)
    await fetchBatch() // Refresh data
  }
  showEditDialog.value = false
}

const handleReadingAdded = async () => {
  await fetchBatch() // Refresh to show new reading
  showReadingDialog.value = false
}

const handleNoteAdded = async () => {
  await fetchBatch() // Refresh to show new note
  showNoteDialog.value = false
}

// Quick action handlers
const addReading = () => {
  showReadingDialog.value = true
}

const addNote = () => {
  showNoteDialog.value = true
}

const duplicateBatch = async () => {
  if (currentBatch.value) {
    // Create a new batch based on the current one
    const newBatchData = {
      ...currentBatch.value,
      batch_name: `${currentBatch.value.batch_name} (Copy)`,
      batch_number: currentBatch.value.batch_number + 1,
      status: 'planning',
      brew_date: new Date().toISOString(),
    }
    delete newBatchData.id
    delete newBatchData.created_at
    delete newBatchData.updated_at
    
    // Navigate to create batch with pre-filled data
    router.push({
      path: '/batches/newBatch',
      query: { duplicate: JSON.stringify(newBatchData) }
    })
  }
}

const generateBrewSheet = () => {
  // Generate and download/print brew sheet
  window.print()
}

const exportData = () => {
  if (currentBatch.value) {
    const data = JSON.stringify(currentBatch.value, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `batch-${currentBatch.value.batch_number}-${currentBatch.value.batch_name}.json`
    a.click()
    URL.revokeObjectURL(url)
  }
}

// Load batch on mount
onMounted(() => {
  fetchBatch()
})

// Set page title
useHead({
  title: computed(() => currentBatch.value ? `${currentBatch.value.batch_name} - HoppyBrew` : 'Batch Details - HoppyBrew')
})
</script>

<style scoped>
@media print {
  .sticky {
    position: static !important;
  }
  
  nav, button, .no-print {
    display: none !important;
  }
}
</style>