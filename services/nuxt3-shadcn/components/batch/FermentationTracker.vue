<template>
  <div class="space-y-6">
    <!-- Header with Add Reading Button -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle class="text-xl">Fermentation Tracking</CardTitle>
            <CardDescription>
              Monitor gravity, temperature, and pH throughout fermentation
            </CardDescription>
          </div>
          <div class="flex gap-2">
            <Button variant="default" @click="showReadingDialog = true">
              <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
              Add Reading
            </Button>
            <Button variant="outline" @click="refreshData">
              <Icon name="mdi:refresh" class="mr-2 h-4 w-4" />
              Refresh
            </Button>
          </div>
        </div>
      </CardHeader>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="text-center space-y-4">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto"></div>
        <p class="text-muted-foreground">Loading fermentation data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <Card>
        <CardHeader>
          <Icon name="mdi:alert-circle" class="mx-auto h-12 w-12 text-red-500" />
          <CardTitle class="text-red-600">Error Loading Data</CardTitle>
          <CardDescription>{{ error }}</CardDescription>
        </CardHeader>
        <CardFooter class="justify-center">
          <Button variant="outline" @click="refreshData">
            <Icon name="mdi:refresh" class="mr-2 h-4 w-4" />
            Try Again
          </Button>
        </CardFooter>
      </Card>
    </div>

    <!-- Main Content -->
    <template v-else>
      <!-- Current Metrics Cards -->
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent class="p-4 text-center">
            <div class="flex items-center justify-center gap-2 mb-2">
              <Icon name="mdi:speedometer" class="h-5 w-5 text-amber-500" />
              <span class="text-sm font-medium">Current Gravity</span>
            </div>
            <p class="text-2xl font-bold text-amber-600">
              {{ latestReading?.gravity?.toFixed(3) || 'N/A' }}
            </p>
            <p class="text-xs text-muted-foreground">SG</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent class="p-4 text-center">
            <div class="flex items-center justify-center gap-2 mb-2">
              <Icon name="mdi:thermometer" class="h-5 w-5 text-orange-500" />
              <span class="text-sm font-medium">Temperature</span>
            </div>
            <p class="text-2xl font-bold text-orange-600">
              {{ latestReading?.temperature?.toFixed(1) || 'N/A' }}°C
            </p>
            <p class="text-xs text-muted-foreground">
              {{ latestReading ? formatDate(latestReading.timestamp) : '' }}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent class="p-4 text-center">
            <div class="flex items-center justify-center gap-2 mb-2">
              <Icon name="mdi:water" class="h-5 w-5 text-blue-500" />
              <span class="text-sm font-medium">pH Level</span>
            </div>
            <p class="text-2xl font-bold text-blue-600">
              {{ latestReading?.ph?.toFixed(1) || 'N/A' }}
            </p>
            <p class="text-xs text-muted-foreground">pH</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent class="p-4 text-center">
            <div class="flex items-center justify-center gap-2 mb-2">
              <Icon name="mdi:beer" class="h-5 w-5 text-purple-500" />
              <span class="text-sm font-medium">Est. ABV</span>
            </div>
            <p class="text-2xl font-bold text-purple-600">
              {{ currentABV?.toFixed(1) || 'N/A' }}%
            </p>
            <p class="text-xs text-muted-foreground">
              {{ currentAttenuation?.toFixed(0) || '0' }}% attenuation
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- Charts -->
      <div class="grid lg:grid-cols-2 gap-6">
        <!-- Gravity Chart -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Icon name="mdi:chart-line" class="h-5 w-5" />
              Gravity Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div ref="gravityChartEl" class="h-64"></div>
          </CardContent>
        </Card>

        <!-- Temperature Chart -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Icon name="mdi:thermometer" class="h-5 w-5" />
              Temperature Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div ref="temperatureChartEl" class="h-64"></div>
          </CardContent>
        </Card>

        <!-- ABV/Attenuation Chart -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Icon name="mdi:percent" class="h-5 w-5" />
              ABV & Attenuation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div ref="abvChartEl" class="h-64"></div>
          </CardContent>
        </Card>

        <!-- pH Chart -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Icon name="mdi:water" class="h-5 w-5" />
              pH Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div ref="phChartEl" class="h-64"></div>
          </CardContent>
        </Card>
      </div>

      <!-- Readings Timeline -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:timeline" class="h-5 w-5" />
            Reading History
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="readings.length === 0" class="text-center py-8 text-muted-foreground">
            <Icon name="mdi:information" class="h-12 w-12 mx-auto mb-2 opacity-50" />
            <p>No readings recorded yet. Add your first reading to start tracking!</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="reading in readings"
              :key="reading.id"
              class="flex items-start gap-4 p-4 border rounded-lg hover:bg-gray-50"
            >
              <div class="flex-shrink-0 mt-1">
                <Icon name="mdi:circle-small" class="h-6 w-6 text-amber-500" />
              </div>
              <div class="flex-grow">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-medium">{{ formatDateTime(reading.timestamp) }}</span>
                  <div class="flex gap-2">
                    <Button size="sm" variant="ghost" @click="editReading(reading)">
                      <Icon name="mdi:pencil" class="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="ghost" @click="deleteReading(reading.id)">
                      <Icon name="mdi:delete" class="h-4 w-4 text-red-500" />
                    </Button>
                  </div>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm mb-2">
                  <div>
                    <span class="text-muted-foreground">Gravity:</span>
                    <span class="font-medium ml-1">{{ reading.gravity?.toFixed(3) || 'N/A' }}</span>
                  </div>
                  <div>
                    <span class="text-muted-foreground">Temp:</span>
                    <span class="font-medium ml-1">{{ reading.temperature?.toFixed(1) || 'N/A' }}°C</span>
                  </div>
                  <div>
                    <span class="text-muted-foreground">pH:</span>
                    <span class="font-medium ml-1">{{ reading.ph?.toFixed(1) || 'N/A' }}</span>
                  </div>
                  <div>
                    <span class="text-muted-foreground">ABV:</span>
                    <span class="font-medium ml-1">
                      {{ calculateReadingABV(reading)?.toFixed(1) || 'N/A' }}%
                    </span>
                  </div>
                </div>
                <p v-if="reading.notes" class="text-sm text-muted-foreground">
                  {{ reading.notes }}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </template>

    <!-- Add/Edit Reading Dialog -->
    <Dialog v-model:open="showReadingDialog">
      <DialogContent class="max-w-md">
        <DialogHeader>
          <DialogTitle>{{ editingReading ? 'Edit' : 'Add' }} Reading</DialogTitle>
          <DialogDescription>Record fermentation measurements</DialogDescription>
        </DialogHeader>
        
        <div class="space-y-4">
          <div>
            <label class="text-sm font-medium">Reading Date & Time</label>
            <Input v-model="formData.timestamp" type="datetime-local" />
          </div>
          <div>
            <label class="text-sm font-medium">Gravity (SG)</label>
            <Input v-model="formData.gravity" type="number" step="0.001" placeholder="1.020" />
          </div>
          <div>
            <label class="text-sm font-medium">Temperature (°C)</label>
            <Input v-model="formData.temperature" type="number" step="0.1" placeholder="20.5" />
          </div>
          <div>
            <label class="text-sm font-medium">pH (optional)</label>
            <Input v-model="formData.ph" type="number" step="0.1" placeholder="5.4" />
          </div>
          <div>
            <label class="text-sm font-medium">Notes (optional)</label>
            <Textarea v-model="formData.notes" placeholder="Additional notes about this reading..." />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" @click="showReadingDialog = false">Cancel</Button>
          <Button @click="saveReading">{{ editingReading ? 'Update' : 'Save' }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import Highcharts from 'highcharts'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

const props = defineProps<{
  batchId: number | string
}>()

// State
const loading = ref(false)
const error = ref<string | null>(null)
const readings = ref<any[]>([])
const chartData = ref<any>(null)
const showReadingDialog = ref(false)
const editingReading = ref<any>(null)
const formData = ref({
  timestamp: new Date().toISOString().slice(0, 16),
  gravity: '',
  temperature: '',
  ph: '',
  notes: ''
})

// Chart refs
const gravityChartEl = ref<HTMLElement | null>(null)
const temperatureChartEl = ref<HTMLElement | null>(null)
const abvChartEl = ref<HTMLElement | null>(null)
const phChartEl = ref<HTMLElement | null>(null)

// Computed
const latestReading = computed(() => {
  if (readings.value.length === 0) return null
  return readings.value[readings.value.length - 1]
})

const currentABV = computed(() => {
  if (!chartData.value || chartData.value.abv.length === 0) return null
  return chartData.value.abv[chartData.value.abv.length - 1]
})

const currentAttenuation = computed(() => {
  if (!chartData.value || chartData.value.attenuation.length === 0) return null
  return chartData.value.attenuation[chartData.value.attenuation.length - 1]
})

// Methods
const fetchReadings = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await fetch(`http://localhost:8000/batches/${props.batchId}/fermentation/readings`)
    if (!response.ok) throw new Error('Failed to fetch readings')
    
    readings.value = await response.json()
  } catch (err: any) {
    error.value = err.message
    console.error('Error fetching readings:', err)
  } finally {
    loading.value = false
  }
}

const fetchChartData = async () => {
  try {
    const response = await fetch(`http://localhost:8000/batches/${props.batchId}/fermentation/chart-data`)
    if (!response.ok) throw new Error('Failed to fetch chart data')
    
    chartData.value = await response.json()
    renderCharts()
  } catch (err: any) {
    console.error('Error fetching chart data:', err)
  }
}

const refreshData = async () => {
  await Promise.all([fetchReadings(), fetchChartData()])
}

const saveReading = async () => {
  try {
    const data = {
      timestamp: new Date(formData.value.timestamp).toISOString(),
      gravity: formData.value.gravity ? parseFloat(formData.value.gravity) : null,
      temperature: formData.value.temperature ? parseFloat(formData.value.temperature) : null,
      ph: formData.value.ph ? parseFloat(formData.value.ph) : null,
      notes: formData.value.notes || null
    }

    let response
    if (editingReading.value) {
      response = await fetch(`http://localhost:8000/fermentation/readings/${editingReading.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
    } else {
      response = await fetch(`http://localhost:8000/batches/${props.batchId}/fermentation/readings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
    }

    if (!response.ok) throw new Error('Failed to save reading')

    showReadingDialog.value = false
    resetForm()
    await refreshData()
  } catch (err: any) {
    alert('Error saving reading: ' + err.message)
  }
}

const editReading = (reading: any) => {
  editingReading.value = reading
  formData.value = {
    timestamp: new Date(reading.timestamp).toISOString().slice(0, 16),
    gravity: reading.gravity?.toString() || '',
    temperature: reading.temperature?.toString() || '',
    ph: reading.ph?.toString() || '',
    notes: reading.notes || ''
  }
  showReadingDialog.value = true
}

const deleteReading = async (readingId: number) => {
  if (!confirm('Are you sure you want to delete this reading?')) return

  try {
    const response = await fetch(`http://localhost:8000/fermentation/readings/${readingId}`, {
      method: 'DELETE'
    })

    if (!response.ok) throw new Error('Failed to delete reading')

    await refreshData()
  } catch (err: any) {
    alert('Error deleting reading: ' + err.message)
  }
}

const resetForm = () => {
  editingReading.value = null
  formData.value = {
    timestamp: new Date().toISOString().slice(0, 16),
    gravity: '',
    temperature: '',
    ph: '',
    notes: ''
  }
}

const calculateReadingABV = (reading: any) => {
  if (!chartData.value || !reading.gravity) return null
  const index = readings.value.findIndex(r => r.id === reading.id)
  if (index >= 0 && index < chartData.value.abv.length) {
    return chartData.value.abv[index]
  }
  return null
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString()
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleString()
}

const renderCharts = () => {
  if (!chartData.value) return

  const { timestamps, gravity, temperature, ph, abv, attenuation } = chartData.value

  // Gravity Chart
  if (gravityChartEl.value) {
    Highcharts.chart(gravityChartEl.value, {
      chart: { type: 'line' },
      title: { text: null },
      xAxis: {
        categories: timestamps.map((t: string) => new Date(t).toLocaleDateString()),
        title: { text: 'Date' }
      },
      yAxis: { title: { text: 'Specific Gravity' } },
      series: [{
        name: 'Gravity',
        data: gravity,
        color: '#f59e0b'
      }],
      credits: { enabled: false }
    })
  }

  // Temperature Chart
  if (temperatureChartEl.value) {
    Highcharts.chart(temperatureChartEl.value, {
      chart: { type: 'line' },
      title: { text: null },
      xAxis: {
        categories: timestamps.map((t: string) => new Date(t).toLocaleDateString()),
        title: { text: 'Date' }
      },
      yAxis: { title: { text: 'Temperature (°C)' } },
      series: [{
        name: 'Temperature',
        data: temperature,
        color: '#f97316'
      }],
      credits: { enabled: false }
    })
  }

  // ABV/Attenuation Chart
  if (abvChartEl.value) {
    Highcharts.chart(abvChartEl.value, {
      chart: { type: 'line' },
      title: { text: null },
      xAxis: {
        categories: timestamps.map((t: string) => new Date(t).toLocaleDateString()),
        title: { text: 'Date' }
      },
      yAxis: [
        { title: { text: 'ABV (%)' } },
        { title: { text: 'Attenuation (%)' }, opposite: true }
      ],
      series: [
        { name: 'ABV', data: abv, color: '#a855f7', yAxis: 0 },
        { name: 'Attenuation', data: attenuation, color: '#8b5cf6', yAxis: 1 }
      ],
      credits: { enabled: false }
    })
  }

  // pH Chart
  if (phChartEl.value) {
    Highcharts.chart(phChartEl.value, {
      chart: { type: 'line' },
      title: { text: null },
      xAxis: {
        categories: timestamps.map((t: string) => new Date(t).toLocaleDateString()),
        title: { text: 'Date' }
      },
      yAxis: { title: { text: 'pH' } },
      series: [{
        name: 'pH',
        data: ph,
        color: '#3b82f6'
      }],
      credits: { enabled: false }
    })
  }
}

// Lifecycle
onMounted(() => {
  refreshData()
})

watch(showReadingDialog, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})
</script>
