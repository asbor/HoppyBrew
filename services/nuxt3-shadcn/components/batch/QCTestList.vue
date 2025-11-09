<template>
  <Card>
    <CardHeader>
      <div class="flex items-center justify-between">
        <div>
          <CardTitle>Quality Control Tests</CardTitle>
          <CardDescription>BJCP evaluations and tasting notes</CardDescription>
        </div>
        <Button @click="openNewTestDialog">
          <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
          New QC Test
        </Button>
      </div>
    </CardHeader>
    <CardContent>
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <Icon name="mdi:loading" class="h-8 w-8 animate-spin text-muted-foreground" />
      </div>

      <!-- Empty State -->
      <div v-else-if="!tests || tests.length === 0" class="text-center py-12">
        <Icon name="mdi:clipboard-check-outline" class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
        <h3 class="text-lg font-semibold mb-2">No Quality Control Tests</h3>
        <p class="text-muted-foreground mb-4">
          Start documenting your beer's quality with BJCP-style evaluations
        </p>
        <Button @click="openNewTestDialog" variant="outline">
          <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
          Create First Test
        </Button>
      </div>

      <!-- QC Tests List -->
      <div v-else class="space-y-4">
        <div
          v-for="test in tests"
          :key="test.id"
          class="border rounded-lg p-4 hover:bg-accent/50 transition-colors"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-1">
                <h4 class="font-semibold">
                  {{ formatDate(test.test_date) }}
                </h4>
                <Badge v-if="test.score" :class="getScoreColor(test.score)">
                  {{ test.score }}/50 - {{ getScoreCategory(test.score) }}
                </Badge>
              </div>
              <p v-if="test.tester_name" class="text-sm text-muted-foreground">
                Tester: {{ test.tester_name }}
              </p>
            </div>
            <div class="flex gap-2">
              <Button
                v-if="test.id"
                @click="exportPDF(test.id)"
                variant="outline"
                size="sm"
              >
                <Icon name="mdi:file-pdf-box" class="h-4 w-4" />
              </Button>
              <Button
                @click="openEditDialog(test)"
                variant="outline"
                size="sm"
              >
                <Icon name="mdi:pencil" class="h-4 w-4" />
              </Button>
              <Button
                @click="deleteTest(test.id)"
                variant="outline"
                size="sm"
              >
                <Icon name="mdi:delete" class="h-4 w-4 text-red-500" />
              </Button>
            </div>
          </div>

          <!-- Measured Values -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3 text-sm">
            <div v-if="test.final_gravity">
              <span class="text-muted-foreground">FG:</span>
              <span class="ml-2 font-medium">{{ test.final_gravity }}</span>
            </div>
            <div v-if="test.abv_actual">
              <span class="text-muted-foreground">ABV:</span>
              <span class="ml-2 font-medium">{{ test.abv_actual }}%</span>
            </div>
            <div v-if="test.color">
              <span class="text-muted-foreground">Color:</span>
              <span class="ml-2 font-medium">{{ test.color }}</span>
            </div>
            <div v-if="test.clarity">
              <span class="text-muted-foreground">Clarity:</span>
              <span class="ml-2 font-medium">{{ test.clarity }}</span>
            </div>
          </div>

          <!-- BJCP Scores -->
          <div v-if="hasScores(test)" class="mb-3">
            <div class="grid grid-cols-5 gap-2 text-sm">
              <div v-if="test.aroma_score !== null" class="text-center">
                <div class="text-muted-foreground text-xs">Aroma</div>
                <div class="font-semibold">{{ test.aroma_score }}/12</div>
              </div>
              <div v-if="test.appearance_score !== null" class="text-center">
                <div class="text-muted-foreground text-xs">Appearance</div>
                <div class="font-semibold">{{ test.appearance_score }}/3</div>
              </div>
              <div v-if="test.flavor_score !== null" class="text-center">
                <div class="text-muted-foreground text-xs">Flavor</div>
                <div class="font-semibold">{{ test.flavor_score }}/20</div>
              </div>
              <div v-if="test.mouthfeel_score !== null" class="text-center">
                <div class="text-muted-foreground text-xs">Mouthfeel</div>
                <div class="font-semibold">{{ test.mouthfeel_score }}/5</div>
              </div>
              <div v-if="test.overall_impression_score !== null" class="text-center">
                <div class="text-muted-foreground text-xs">Overall</div>
                <div class="font-semibold">{{ test.overall_impression_score }}/10</div>
              </div>
            </div>
          </div>

          <!-- Tasting Notes Preview -->
          <div v-if="test.taste_notes" class="text-sm">
            <p class="text-muted-foreground line-clamp-2">{{ test.taste_notes }}</p>
          </div>

          <!-- Photo Indicator -->
          <div v-if="test.photo_path" class="mt-2">
            <Badge variant="outline">
              <Icon name="mdi:camera" class="mr-1 h-3 w-3" />
              Photo attached
            </Badge>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>

  <!-- QC Test Dialog -->
  <QCTestDialog
    v-model:open="dialogOpen"
    :batch-id="batchId"
    :test="selectedTest"
    @saved="handleTestSaved"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Icon } from '#components'
import QCTestDialog from './QCTestDialog.vue'

interface QCTest {
  id?: number
  batch_id?: number
  test_date: string
  final_gravity?: number | null
  abv_actual?: number | null
  color?: string | null
  clarity?: string | null
  taste_notes?: string | null
  aroma_notes?: string | null
  appearance_notes?: string | null
  flavor_notes?: string | null
  mouthfeel_notes?: string | null
  score?: number | null
  aroma_score?: number | null
  appearance_score?: number | null
  flavor_score?: number | null
  mouthfeel_score?: number | null
  overall_impression_score?: number | null
  tester_name?: string | null
  notes?: string | null
  photo_path?: string | null
}

const props = defineProps<{
  batchId: number
}>()

const tests = ref<QCTest[]>([])
const loading = ref(false)
const dialogOpen = ref(false)
const selectedTest = ref<QCTest | null>(null)

const fetchTests = async () => {
  loading.value = true
  try {
    const apiUrl = useApiUrl()
    const response = await fetch(`${apiUrl}/batches/${props.batchId}/qc-tests`)
    if (!response.ok) throw new Error('Failed to fetch QC tests')
    tests.value = await response.json()
  } catch (error) {
    console.error('Error fetching QC tests:', error)
  } finally {
    loading.value = false
  }
}

const openNewTestDialog = () => {
  selectedTest.value = null
  dialogOpen.value = true
}

const openEditDialog = (test: QCTest) => {
  selectedTest.value = test
  dialogOpen.value = true
}

const handleTestSaved = () => {
  fetchTests()
}

const deleteTest = async (testId?: number) => {
  if (!testId) return
  
  if (!confirm('Are you sure you want to delete this QC test?')) return

  try {
    const apiUrl = useApiUrl()
    const response = await fetch(`${apiUrl}/qc-tests/${testId}`, {
      method: 'DELETE',
    })
    if (!response.ok) throw new Error('Failed to delete QC test')
    fetchTests()
  } catch (error) {
    console.error('Error deleting QC test:', error)
    alert('Failed to delete QC test')
  }
}

const exportPDF = async (testId: number) => {
  try {
    const apiUrl = useApiUrl()
    const response = await fetch(`${apiUrl}/qc-tests/${testId}/export/pdf`)
    if (!response.ok) throw new Error('Failed to export PDF')
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `qc_test_${testId}.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (error) {
    console.error('Error exporting PDF:', error)
    alert('Failed to export PDF')
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getScoreCategory = (score: number) => {
  if (score >= 45) return 'Outstanding'
  if (score >= 38) return 'Excellent'
  if (score >= 30) return 'Very Good'
  if (score >= 21) return 'Good'
  if (score >= 14) return 'Fair'
  return 'Problematic'
}

const getScoreColor = (score: number) => {
  if (score >= 45) return 'bg-green-600 text-white'
  if (score >= 38) return 'bg-blue-600 text-white'
  if (score >= 30) return 'bg-cyan-600 text-white'
  if (score >= 21) return 'bg-yellow-600 text-white'
  if (score >= 14) return 'bg-orange-600 text-white'
  return 'bg-red-600 text-white'
}

const hasScores = (test: QCTest) => {
  return test.aroma_score !== null ||
    test.appearance_score !== null ||
    test.flavor_score !== null ||
    test.mouthfeel_score !== null ||
    test.overall_impression_score !== null
}

onMounted(() => {
  fetchTests()
})
</script>
