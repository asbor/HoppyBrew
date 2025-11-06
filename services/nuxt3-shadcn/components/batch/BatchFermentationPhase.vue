<template>
  <div class="space-y-6">
    <!-- Fermentation Header -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle class="text-xl">Fermentation - Batch #{{ batch.batch_number }}</CardTitle>
            <CardDescription>
              {{ getCurrentFermentationPhase() }} • Day {{ fermentationDay }} of fermentation
            </CardDescription>
          </div>
          <div class="flex gap-2">
            <Button @click="showReadingDialog = true" variant="outline">
              <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
              Add Reading
            </Button>
            <Button @click="exportReadings" variant="outline">
              <Icon name="mdi:download" class="mr-2 h-4 w-4" />
              Export
            </Button>
            <Button @click="showDevicesDialog = true" variant="outline">
              <Icon name="mdi:cellphone-cog" class="mr-2 h-4 w-4" />
              Devices
            </Button>
          </div>
        </div>
      </CardHeader>
    </Card>

    <!-- Current Readings -->
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card>
        <CardContent class="p-4 text-center">
          <div class="flex items-center justify-center gap-2 mb-2">
            <Icon name="mdi:speedometer" class="h-5 w-5 text-red-500" />
            <span class="text-sm font-medium">SG</span>
          </div>
          <p class="text-2xl font-bold text-red-600">{{ currentReadings.gravity }}</p>
          <p class="text-xs text-muted-foreground">Temp {{ currentReadings.temperature }}°C</p>
          <p class="text-xs text-muted-foreground">At {{ currentReadings.percentage }}% ABV {{ currentReadings.abv }}%</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="p-4 text-center">
          <div class="flex items-center justify-center gap-2 mb-2">
            <Icon name="mdi:thermometer" class="h-5 w-5 text-orange-500" />
            <span class="text-sm font-medium">Temp</span>
          </div>
          <p class="text-2xl font-bold text-orange-600">{{ currentReadings.temperature }}°C</p>
          <p class="text-xs text-muted-foreground">{{ formatDate(currentReadings.lastUpdate) }}</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="p-4 text-center">
          <div class="flex items-center justify-center gap-2 mb-2">
            <Icon name="mdi:beaker" class="h-5 w-5 text-blue-500" />
            <span class="text-sm font-medium">Original Gravity</span>
          </div>
          <p class="text-2xl font-bold text-blue-600">{{ fermentationData.originalGravity }}</p>
          <p class="text-xs text-muted-foreground">SG</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="p-4 text-center">
          <div class="flex items-center justify-center gap-2 mb-2">
            <Icon name="mdi:flask" class="h-5 w-5 text-green-500" />
            <span class="text-sm font-medium">Fermenter Vol</span>
          </div>
          <p class="text-2xl font-bold text-green-600">{{ fermentationData.fermenterVolume }}</p>
          <p class="text-xs text-muted-foreground">L</p>
        </CardContent>
      </Card>
    </div>

    <!-- Fermentation Charts -->
    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Gravity Chart -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <CardTitle class="flex items-center gap-2">
              <Icon name="mdi:chart-line" class="h-5 w-5" />
              Gravity Readings
            </CardTitle>
            <Button variant="ghost" size="sm" @click="toggleGravityView">
              <Icon name="mdi:eye" class="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <!-- Chart Placeholder with simulated data -->
          <div class="h-64 bg-gray-50 rounded relative overflow-hidden">
            <!-- Y-axis labels -->
            <div class="absolute left-2 top-2 text-xs text-muted-foreground">1.064</div>
            <div class="absolute left-2 top-16 text-xs text-muted-foreground">1.056</div>
            <div class="absolute left-2 top-32 text-xs text-muted-foreground">1.048</div>
            <div class="absolute left-2 top-48 text-xs text-muted-foreground">1.040</div>
            <div class="absolute left-2 bottom-2 text-xs text-muted-foreground">1.032</div>
            
            <!-- X-axis labels -->
            <div class="absolute bottom-2 left-16 text-xs text-muted-foreground">3 Sep</div>
            <div class="absolute bottom-2 left-32 text-xs text-muted-foreground">4 Sep</div>
            <div class="absolute bottom-2 left-48 text-xs text-muted-foreground">5 Sep</div>
            <div class="absolute bottom-2 left-64 text-xs text-muted-foreground">6 Sep</div>
            <div class="absolute bottom-2 left-80 text-xs text-muted-foreground">7 Sep</div>
            <div class="absolute bottom-2 left-96 text-xs text-muted-foreground">8 Sep</div>
            <div class="absolute bottom-2 right-16 text-xs text-muted-foreground">9 Sep</div>

            <!-- Simulated gravity line -->
            <svg class="absolute inset-4 w-full h-full" viewBox="0 0 300 200">
              <path 
                d="M 10 20 L 50 40 L 90 60 L 130 80 L 170 100 L 210 120 L 250 140 L 290 150" 
                stroke="#ef4444" 
                stroke-width="2" 
                fill="none"
              />
              <!-- Data points -->
              <circle cx="10" cy="20" r="3" fill="#ef4444" />
              <circle cx="50" cy="40" r="3" fill="#ef4444" />
              <circle cx="90" cy="60" r="3" fill="#ef4444" />
              <circle cx="130" cy="80" r="3" fill="#ef4444" />
              <circle cx="170" cy="100" r="3" fill="#ef4444" />
              <circle cx="210" cy="120" r="3" fill="#ef4444" />
              <circle cx="250" cy="140" r="3" fill="#ef4444" />
              <circle cx="290" cy="150" r="3" fill="#ef4444" />
            </svg>

            <!-- Fermentation phases background -->
            <div class="absolute top-4 left-4 right-4 bottom-8 flex">
              <div class="flex-1 bg-blue-100/30 border-r border-blue-300"></div>
              <div class="flex-1 bg-indigo-100/30 border-r border-indigo-300"></div>
              <div class="flex-1 bg-purple-100/30"></div>
            </div>
          </div>
          
          <!-- Chart Legend -->
          <div class="flex justify-center gap-4 mt-4 text-xs">
            <div class="flex items-center gap-1">
              <div class="w-3 h-3 bg-blue-100 border border-blue-300"></div>
              <span>Primary</span>
            </div>
            <div class="flex items-center gap-1">
              <div class="w-3 h-3 bg-indigo-100 border border-indigo-300"></div>
              <span>Secondary</span>
            </div>
            <div class="flex items-center gap-1">
              <div class="w-3 h-3 bg-purple-100 border border-purple-300"></div>
              <span>Conditioning</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Temperature Chart -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:thermometer" class="h-5 w-5" />
            Temperature Profile
          </CardTitle>
        </CardHeader>
        <CardContent>
          <!-- Temperature Chart Placeholder -->
          <div class="h-64 bg-gray-50 rounded relative overflow-hidden">
            <!-- Y-axis labels for temperature -->
            <div class="absolute left-2 top-2 text-xs text-muted-foreground">24°C</div>
            <div class="absolute left-2 top-16 text-xs text-muted-foreground">22°C</div>
            <div class="absolute left-2 top-32 text-xs text-muted-foreground">20°C</div>
            <div class="absolute left-2 top-48 text-xs text-muted-foreground">18°C</div>
            <div class="absolute left-2 bottom-2 text-xs text-muted-foreground">16°C</div>
            
            <!-- X-axis labels -->
            <div class="absolute bottom-2 left-16 text-xs text-muted-foreground">3 Sep</div>
            <div class="absolute bottom-2 left-32 text-xs text-muted-foreground">4 Sep</div>
            <div class="absolute bottom-2 left-48 text-xs text-muted-foreground">5 Sep</div>
            <div class="absolute bottom-2 right-16 text-xs text-muted-foreground">9 Sep</div>

            <!-- Simulated temperature line -->
            <svg class="absolute inset-4 w-full h-full" viewBox="0 0 300 200">
              <path 
                d="M 10 60 L 50 58 L 90 62 L 130 65 L 170 63 L 210 61 L 250 64 L 290 62" 
                stroke="#f97316" 
                stroke-width="2" 
                fill="none"
              />
              <!-- Temperature target zone -->
              <rect x="0" y="50" width="300" height="20" fill="#f97316" opacity="0.1" />
            </svg>
          </div>

          <!-- Temperature Stats -->
          <div class="grid grid-cols-3 gap-4 mt-4 text-center text-xs">
            <div>
              <p class="font-medium">Min</p>
              <p class="text-muted-foreground">20.1°C</p>
            </div>
            <div>
              <p class="font-medium">Avg</p>
              <p class="text-muted-foreground">21.1°C</p>
            </div>
            <div>
              <p class="font-medium">Max</p>
              <p class="text-muted-foreground">22.3°C</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Fermentation Profile & Carbonation -->
    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Fermentation Profile -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:clipboard-list" class="h-5 w-5" />
            Fermentation Profile
          </CardTitle>
          <Button @click="editProfile" size="sm" variant="outline" class="ml-auto">
            <Icon name="mdi:pencil" class="mr-2 h-4 w-4" />
            Edit
          </Button>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <!-- Primary Fermentation -->
            <div class="p-3 bg-blue-50 rounded">
              <div class="flex justify-between items-center mb-2">
                <h4 class="font-medium text-blue-700">Primary - 18°C - 8 days</h4>
                <Badge variant="default" class="bg-blue-500">Active</Badge>
              </div>
              <div class="text-sm text-muted-foreground">
                <p>Primary - 21°C - 8 days</p>
              </div>
            </div>

            <!-- Bottling Date -->
            <div class="flex justify-between items-center">
              <span class="font-medium">Bottling Date</span>
              <span class="text-muted-foreground">{{ formatDate(bottlingDate) }}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Carbonation -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:bubble-chart" class="h-5 w-5" />
            Carbonation
          </CardTitle>
          <Button @click="editCarbonation" size="sm" variant="outline" class="ml-auto">
            <Icon name="mdi:pencil" class="mr-2 h-4 w-4" />
            Change
          </Button>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <!-- Carbonation Type -->
            <div class="text-center p-4 bg-gray-50 rounded">
              <p class="text-lg font-bold">Keg (Force)</p>
              <p class="text-sm text-muted-foreground">
                0.97 Bar at 7.5°C<br>
                for approximately 1 week<br>
                to reach 2.4 vol of CO₂
              </p>
            </div>

            <!-- Current Status -->
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Type:</span>
                <span class="text-sm font-medium">Keg (Force)</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">SG:</span>
                <span class="text-sm font-medium">1.031</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Temp:</span>
                <span class="text-sm font-medium">21.1°C</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">At 45%:</span>
                <span class="text-sm font-medium">ABV 3.5%</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Stats Summary -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Icon name="mdi:chart-bar" class="h-5 w-5" />
          Stats
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="text-center">
            <p class="text-2xl font-bold text-blue-600">5.3%</p>
            <p class="text-sm text-muted-foreground">ABV</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-green-600">69.2%</p>
            <p class="text-sm text-muted-foreground">Attenuation</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-amber-600">78.59%</p>
            <p class="text-sm text-muted-foreground">Mash Efficiency</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-purple-600">72.59%</p>
            <p class="text-sm text-muted-foreground">Brewhouse Efficiency</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Log Entries -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:note-text" class="h-5 w-5" />
            Log
          </CardTitle>
          <Button @click="showLogDialog = true" size="sm">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Add Entry
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div class="space-y-3">
          <div v-for="entry in fermentationLog" :key="entry.id" 
               class="flex gap-3 p-3 bg-gray-50 rounded">
            <div class="text-xs text-muted-foreground w-20">
              {{ formatDate(entry.date) }}
            </div>
            <div class="text-xs text-muted-foreground w-16">
              {{ formatTime(entry.date) }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <Icon :name="entry.icon" class="h-4 w-4" />
                <span class="text-sm">{{ entry.message }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Batch Notes Section -->
        <div class="mt-6">
          <h4 class="font-medium mb-2">Batch Notes</h4>
          <p class="text-sm text-muted-foreground">
            Justerede med bagepulver. Fejl i hop pH som resultat. HUSK DET NU !
          </p>
        </div>
      </CardContent>
    </Card>

    <!-- Action Buttons -->
    <div class="flex gap-3">
      <Button @click="$emit('start-conditioning')" :disabled="!canMoveToConditioning">
        <Icon name="mdi:snowflake" class="mr-2 h-4 w-4" />
        Start Conditioning
      </Button>
      <Button @click="packageBeer" variant="outline" :disabled="!canPackage">
        <Icon name="mdi:bottle-wine" class="mr-2 h-4 w-4" />
        Package Beer
      </Button>
    </div>

    <!-- Dialogs -->
    <ReadingDialog 
      v-model:open="showReadingDialog"
      @save="addReading"
    />
    
    <DevicesDialog 
      v-model:open="showDevicesDialog"
      :devices="connectedDevices"
    />
    
    <LogDialog 
      v-model:open="showLogDialog"
      @save="addLogEntry"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Icon } from '#components'

const props = defineProps<{
  batch: any
}>()

const emit = defineEmits<{
  'start-conditioning': []
  'update-batch': [data: any]
}>()

// Dialog states
const showReadingDialog = ref(false)
const showDevicesDialog = ref(false)
const showLogDialog = ref(false)

// Current readings from latest sensor data
const currentReadings = ref({
  gravity: 1.031,
  temperature: 21.1,
  percentage: 45,
  abv: 3.5,
  lastUpdate: new Date()
})

// Fermentation data
const fermentationData = ref({
  originalGravity: 1.057,
  fermenterVolume: 21.0,
  startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
})

// Connected devices simulation
const connectedDevices = ref([
  { 
    id: 1, 
    name: 'Tilt Hydrometer', 
    type: 'tilt', 
    color: 'Red', 
    connected: true,
    lastReading: new Date(),
    battery: 85
  }
])

// Fermentation log
const fermentationLog = ref([
  { 
    id: 1, 
    date: new Date('2018-09-02T22:39:00'), 
    message: 'Fermenting', 
    icon: 'mdi:arrow-right' 
  },
  { 
    id: 2, 
    date: new Date('2018-09-02T17:52:00'), 
    message: 'Brewing', 
    icon: 'mdi:arrow-right' 
  },
  { 
    id: 3, 
    date: new Date('2018-09-02T17:52:00'), 
    message: 'Justerede med bagepulver. Fejl. For høj pH som resultat. HUSK DET NU !', 
    icon: 'mdi:alert' 
  }
])

// Computed properties
const fermentationDay = computed(() => {
  const start = fermentationData.value.startDate
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - start.getTime())
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
})

const bottlingDate = computed(() => {
  const start = fermentationData.value.startDate
  const bottling = new Date(start.getTime() + 18 * 24 * 60 * 60 * 1000) // 18 days later
  return bottling
})

const canMoveToConditioning = computed(() => {
  return currentReadings.value.gravity <= 1.020 && fermentationDay.value >= 7
})

const canPackage = computed(() => {
  return currentReadings.value.gravity <= 1.015 && fermentationDay.value >= 14
})

// Methods
const getCurrentFermentationPhase = () => {
  if (fermentationDay.value <= 7) return 'Primary Fermentation'
  if (fermentationDay.value <= 14) return 'Secondary Fermentation' 
  return 'Conditioning'
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Action handlers
const addReading = (reading: any) => {
  currentReadings.value = { ...currentReadings.value, ...reading, lastUpdate: new Date() }
  showReadingDialog.value = false
}

const addLogEntry = (entry: any) => {
  const newEntry = {
    id: fermentationLog.value.length + 1,
    date: new Date(),
    message: entry.message,
    icon: entry.icon || 'mdi:note'
  }
  fermentationLog.value.unshift(newEntry)
  showLogDialog.value = false
}

const toggleGravityView = () => {
  console.log('Toggle gravity chart view')
}

const editProfile = () => {
  console.log('Edit fermentation profile')
}

const editCarbonation = () => {
  console.log('Edit carbonation settings')
}

const exportReadings = () => {
  console.log('Export fermentation readings')
}

const packageBeer = () => {
  console.log('Package beer')
}
</script>