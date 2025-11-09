<template>
  <Card>
    <CardHeader>
      <div class="flex items-center justify-between">
        <div>
          <CardTitle>Quality Control Tests</CardTitle>
          <CardDescription>Record and review quality control test results</CardDescription>
        </div>
        <Button @click="showAddDialog = true">
          <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
          Add QC Test
        </Button>
      </div>
    </CardHeader>
    <CardContent>
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center space-y-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-600 mx-auto"></div>
          <p class="text-sm text-muted-foreground">Loading tests...</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!qcTests || qcTests.length === 0" class="text-center py-12">
        <Icon name="mdi:flask-outline" class="mx-auto h-16 w-16 text-muted-foreground" />
        <h3 class="mt-4 text-lg font-semibold">No Quality Control Tests</h3>
        <p class="mt-2 text-sm text-muted-foreground">
          Start recording quality control data for this batch
        </p>
        <Button @click="showAddDialog = true" class="mt-4" variant="outline">
          <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
          Add First Test
        </Button>
      </div>

      <!-- QC Tests List -->
      <div v-else class="space-y-4">
        <div
          v-for="test in qcTests"
          :key="test.id"
          class="border rounded-lg p-4 hover:bg-muted/50 transition-colors"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <!-- Test Header -->
              <div class="flex items-center gap-3 mb-3">
                <Icon name="mdi:clipboard-check" class="h-5 w-5 text-primary" />
                <span class="font-semibold">
                  {{ formatDate(test.test_date) }}
                </span>
                <Badge v-if="test.score" :class="getScoreBadgeColor(test.score)">
                  {{ test.score }} / 50
                </Badge>
              </div>

              <!-- Measurements Grid -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                <div v-if="test.final_gravity">
                  <p class="text-xs text-muted-foreground">Final Gravity</p>
                  <p class="font-medium">{{ test.final_gravity.toFixed(3) }}</p>
                </div>
                <div v-if="test.abv_actual">
                  <p class="text-xs text-muted-foreground">ABV</p>
                  <p class="font-medium">{{ test.abv_actual.toFixed(1) }}%</p>
                </div>
                <div v-if="test.color">
                  <p class="text-xs text-muted-foreground">Color</p>
                  <p class="font-medium">{{ test.color }}</p>
                </div>
                <div v-if="test.clarity">
                  <p class="text-xs text-muted-foreground">Clarity</p>
                  <p class="font-medium">{{ test.clarity }}</p>
                </div>
              </div>

              <!-- Tasting Notes -->
              <div v-if="test.taste_notes" class="mb-3">
                <p class="text-xs text-muted-foreground mb-1">Tasting Notes</p>
                <p class="text-sm whitespace-pre-line">{{ test.taste_notes }}</p>
              </div>

              <!-- Photo -->
              <div v-if="test.photo_url" class="mb-3">
                <img
                  :src="test.photo_url"
                  alt="Beer appearance"
                  class="w-32 h-32 object-cover rounded-md border"
                />
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 ml-4">
              <Button
                size="sm"
                variant="ghost"
                @click="editTest(test)"
                title="Edit test"
              >
                <Icon name="mdi:pencil" class="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                variant="ghost"
                @click="exportPDF(test.id)"
                title="Export as PDF"
              >
                <Icon name="mdi:file-pdf" class="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                variant="ghost"
                @click="deleteTest(test.id)"
                title="Delete test"
              >
                <Icon name="mdi:delete" class="h-4 w-4 text-red-500" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </CardContent>

    <!-- Add/Edit Dialog -->
    <QualityControlDialog
      v-model:open="showAddDialog"
      :batch-id="batchId"
      :existing-test="selectedTest"
      @save="handleTestSaved"
    />
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Icon } from '#components'
import QualityControlDialog from './QualityControlDialog.vue'

interface Props {
  batchId: number
}

const props = defineProps<Props>()

const qcTests = ref<any[]>([])
const loading = ref(false)
const showAddDialog = ref(false)
const selectedTest = ref<any>(null)

// Fetch QC tests
const fetchQCTests = async () => {
  loading.value = true
  try {
    const response = await $fetch(`/api/batches/${props.batchId}/quality-control-tests`)
    qcTests.value = response as any[]
  } catch (error) {
    console.error('Error fetching QC tests:', error)
  } finally {
    loading.value = false
  }
}

// Format date
const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Get score badge color
const getScoreBadgeColor = (score: number) => {
  if (score >= 45) return 'bg-green-600'
  if (score >= 38) return 'bg-green-500'
  if (score >= 30) return 'bg-blue-500'
  if (score >= 21) return 'bg-blue-400'
  if (score >= 14) return 'bg-yellow-500'
  if (score >= 6) return 'bg-orange-500'
  return 'bg-red-500'
}

// Edit test
const editTest = (test: any) => {
  selectedTest.value = test
  showAddDialog.value = true
}

// Delete test
const deleteTest = async (testId: number) => {
  if (!confirm('Are you sure you want to delete this quality control test?')) {
    return
  }

  try {
    await $fetch(`/api/quality-control-tests/${testId}`, {
      method: 'DELETE'
    })
    await fetchQCTests()
  } catch (error) {
    console.error('Error deleting QC test:', error)
    alert('Failed to delete quality control test')
  }
}

// Export PDF
const exportPDF = async (testId: number) => {
  try {
    const blob = await $fetch(`/api/quality-control-tests/${testId}/export-pdf`, {
      responseType: 'blob'
    })
    
    // Create download link
    const url = window.URL.createObjectURL(blob as Blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `qc_test_${testId}_${new Date().toISOString().split('T')[0]}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error exporting PDF:', error)
    alert('Failed to export PDF')
  }
}

// Handle test saved
const handleTestSaved = () => {
  selectedTest.value = null
  fetchQCTests()
}

// Load tests on mount
onMounted(() => {
  fetchQCTests()
})
</script>
