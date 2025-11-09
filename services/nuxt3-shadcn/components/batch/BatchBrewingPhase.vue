<template>
  <div class="space-y-6">
    <!-- Brew Day Header -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle class="text-xl">Brew Day - {{ formatDate(new Date()) }}</CardTitle>
            <CardDescription>Active brewing session for {{ batch.batch_name }}</CardDescription>
          </div>
          <div class="flex gap-2">
            <Button @click="pauseSession" variant="outline">
              <Icon name="mdi:pause" class="mr-2 h-4 w-4" />
              Pause Session
            </Button>
            <Button @click="$emit('start-fermentation')" :disabled="!isBrewingComplete">
              <Icon name="mdi:flask" class="mr-2 h-4 w-4" />
              Start Fermentation
            </Button>
          </div>
        </div>
      </CardHeader>
    </Card>

    <!-- Brew Sheet Overview -->
    <div class="grid lg:grid-cols-3 gap-6">
      <!-- Recipe Summary -->
      <Card>
        <CardHeader>
          <CardTitle class="text-lg">{{ batch.recipe?.name || '5 Yeast Experimental NEIPA' }}</CardTitle>
          <CardDescription>6.0% / 15.6 °P</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <!-- Recipe Type -->
            <div class="text-center">
              <p class="text-sm text-muted-foreground">All Grain</p>
              <p class="text-lg font-semibold">eBIAB</p>
              <p class="text-sm">70% efficiency</p>
              <p class="text-sm">Batch Volume: {{ batch.batch_size }}L</p>
              <p class="text-sm">Boil Time: 60 min</p>
            </div>

            <!-- Water Volumes -->
            <div class="space-y-2">
              <h4 class="font-medium">Water</h4>
              <div class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <span>Mash Water:</span>
                  <span>{{ waterCalculations.mashWater }}L</span>
                </div>
                <div class="flex justify-between">
                  <span>Total Water:</span>
                  <span>{{ waterCalculations.totalWater }}L</span>
                </div>
                <div class="flex justify-between">
                  <span>Boil Volume:</span>
                  <span>{{ waterCalculations.boilVolume }}L</span>
                </div>
                <div class="flex justify-between">
                  <span>Pre-Boil Gravity:</span>
                  <span>1.058</span>
                </div>
              </div>
            </div>

            <!-- Vitals -->
            <div class="space-y-2">
              <h4 class="font-medium">Vitals</h4>
              <div class="space-y-1 text-sm">
                <div class="flex justify-between">
                  <span>Original Gravity:</span>
                  <span>1.064</span>
                </div>
                <div class="flex justify-between">
                  <span>Final Gravity:</span>
                  <span>1.018</span>
                </div>
                <div class="flex justify-between">
                  <span>IBU (Tinseth):</span>
                  <span>26</span>
                </div>
                <div class="flex justify-between">
                  <span>Color:</span>
                  <span class="flex items-center gap-1">
                    4 SRM 
                    <div class="w-4 h-4 rounded" style="background-color: #D4B76A"></div>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Measured Values -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <CardTitle class="text-lg">Measured Values</CardTitle>
            <Button @click="showMeasurementDialog = true" size="sm">
              <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
              Add
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <!-- Current Readings -->
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center p-3 bg-blue-50 rounded">
                <p class="text-2xl font-bold text-blue-600">{{ measuredValues.mash.ph }}</p>
                <p class="text-sm text-muted-foreground">Mash pH</p>
              </div>
              <div class="text-center p-3 bg-green-50 rounded">
                <p class="text-2xl font-bold text-green-600">{{ measuredValues.boil.volume }}L</p>
                <p class="text-sm text-muted-foreground">Boil Vol</p>
              </div>
              <div class="text-center p-3 bg-amber-50 rounded">
                <p class="text-2xl font-bold text-amber-600">{{ measuredValues.preboil.gravity }}</p>
                <p class="text-sm text-muted-foreground">Pre-Boil Gravity</p>
              </div>
              <div class="text-center p-3 bg-purple-50 rounded">
                <p class="text-2xl font-bold text-purple-600">{{ measuredValues.fermenter.volume }}L</p>
                <p class="text-sm text-muted-foreground">Fermenter Vol</p>
              </div>
            </div>

            <!-- Target vs Actual -->
            <div class="space-y-2">
              <h4 class="font-medium text-sm">Target vs Actual</h4>
              <div class="space-y-1 text-xs">
                <div class="flex justify-between">
                  <span>OG:</span>
                  <span>1.064 → {{ measuredValues.originalGravity || 'N/A' }}</span>
                </div>
                <div class="flex justify-between">
                  <span>Volume:</span>
                  <span>{{ batch.batch_size }}L → {{ measuredValues.fermenter.volume }}L</span>
                </div>
                <div class="flex justify-between">
                  <span>Efficiency:</span>
                  <span>70% → {{ calculatedEfficiency }}%</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Stats & Summary -->
      <Card>
        <CardHeader>
          <CardTitle class="text-lg">Stats</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <!-- Efficiency Metrics -->
            <div class="grid grid-cols-2 gap-4 text-center">
              <div class="p-3 bg-gray-50 rounded">
                <p class="text-lg font-bold">{{ stats.abv }}%</p>
                <p class="text-xs text-muted-foreground">ABV</p>
              </div>
              <div class="p-3 bg-gray-50 rounded">
                <p class="text-lg font-bold">{{ stats.attenuation }}%</p>
                <p class="text-xs text-muted-foreground">Attenuation</p>
              </div>
              <div class="p-3 bg-gray-50 rounded">
                <p class="text-lg font-bold">{{ stats.mashEfficiency }}%</p>
                <p class="text-xs text-muted-foreground">Mash Efficiency</p>
              </div>
              <div class="p-3 bg-gray-50 rounded">
                <p class="text-lg font-bold">{{ stats.brewhouseEfficiency }}%</p>
                <p class="text-xs text-muted-foreground">Brewhouse Efficiency</p>
              </div>
            </div>

            <!-- Brew Summary -->
            <div class="space-y-2">
              <h4 class="font-medium text-sm">Summary</h4>
              <div class="text-xs space-y-1">
                <div class="flex justify-between">
                  <span>Recipe:</span>
                  <span>7.01L</span>
                </div>
                <div class="flex justify-between">
                  <span>Measurement:</span>
                  <span>{{ measuredValues.fermenter.volume }}L</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Brew Process Steps -->
    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Mash Profile -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:thermometer" class="h-5 w-5 text-red-500" />
            Mash Profile (High fermentability)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <!-- Mash Steps -->
            <div class="space-y-2">
              <div class="flex justify-between items-center p-3 bg-green-50 rounded border-l-4 border-green-500">
                <div>
                  <p class="font-medium">Strike Temp - 162.9 °F</p>
                  <p class="text-sm text-muted-foreground">154 - 156 °F - 60 min</p>
                </div>
                <Badge variant="default" class="bg-green-500">Complete</Badge>
              </div>
            </div>

            <!-- Temperature Chart Placeholder -->
            <div class="h-32 bg-gray-50 rounded flex items-center justify-center">
              <p class="text-muted-foreground">Temperature Chart</p>
            </div>

            <!-- Mash Actions -->
            <div class="flex gap-2">
              <Button @click="addMashReading" variant="outline" size="sm">
                <Icon name="mdi:thermometer" class="mr-2 h-4 w-4" />
                Add Reading
              </Button>
              <Button @click="mashOut" variant="outline" size="sm">
                <Icon name="mdi:check" class="mr-2 h-4 w-4" />
                Mash Out
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Hop Schedule -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:flower" class="h-5 w-5 text-green-500" />
            Hop Schedule
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <!-- Hop Additions -->
            <div class="space-y-2">
              <div v-for="hop in hopSchedule" :key="`${hop.name}-${hop.time}`"
                   class="flex justify-between items-center p-3 rounded border-l-4"
                   :class="getHopStatusClass(hop)">
                <div>
                  <p class="font-medium">{{ hop.amount }}g {{ hop.name }}</p>
                  <p class="text-sm text-muted-foreground">{{ hop.time }} min - {{ hop.use }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <Badge :variant="getHopBadgeVariant(hop)">
                    {{ getHopStatus(hop) }}
                  </Badge>
                  <Button v-if="hop.status === 'pending'" @click="addHop(hop)" size="sm">
                    <Icon name="mdi:plus" class="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>

            <!-- Boil Timer -->
            <div class="text-center p-4 bg-amber-50 rounded">
              <p class="text-2xl font-bold text-amber-600">{{ boilTimer.display }}</p>
              <p class="text-sm text-muted-foreground">Boil Time Remaining</p>
              <div class="flex gap-2 mt-2 justify-center">
                <Button @click="startBoilTimer" v-if="!boilTimer.running" size="sm">
                  <Icon name="mdi:play" class="mr-2 h-4 w-4" />
                  Start
                </Button>
                <Button @click="pauseBoilTimer" v-if="boilTimer.running" size="sm" variant="outline">
                  <Icon name="mdi:pause" class="mr-2 h-4 w-4" />
                  Pause
                </Button>
                <Button @click="resetBoilTimer" size="sm" variant="outline">
                  <Icon name="mdi:refresh" class="mr-2 h-4 w-4" />
                  Reset
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Fermentation Profile -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Icon name="mdi:bacteria" class="h-5 w-5 text-purple-500" />
          Fermentation Profile (Ale)
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Yeast Information -->
          <div>
            <h4 class="font-medium mb-3">Yeast</h4>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Primary:</span>
                <span class="text-sm font-medium">20°C - 14 days</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Primary:</span>
                <span class="text-sm font-medium">21°C - 8 days</span>
              </div>
            </div>
            
            <div class="mt-4 p-3 bg-purple-50 rounded">
              <div class="flex justify-between items-center">
                <div>
                  <p class="font-medium">1 pkg White Labs WLP001</p>
                  <p class="text-sm text-muted-foreground">California Ale</p>
                  <p class="text-sm text-muted-foreground">1 L starter</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Fermentation Schedule -->
          <div>
            <h4 class="font-medium mb-3">Carbonation</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-muted-foreground">Type:</span>
                <span class="font-medium">Keg (Force)</span>
              </div>
              <div class="flex justify-between">
                <span class="text-muted-foreground">Target:</span>
                <span class="font-medium">0.97 Bar at 7.5°C</span>
              </div>
              <div class="flex justify-between">
                <span class="text-muted-foreground">Method:</span>
                <span class="font-medium">for approximately 1 week to reach 2.4 vol of CO₂</span>
              </div>
            </div>

            <div class="mt-4">
              <h5 class="font-medium mb-2">Volumes of CO₂</h5>
              <div class="text-right">
                <span class="text-lg font-bold">2.5</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Brew Log -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:note-text" class="h-5 w-5" />
            Brew Log
          </CardTitle>
          <Button @click="showLogDialog = true" size="sm">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Add Entry
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div class="space-y-3">
          <div v-for="entry in brewLog" :key="entry.id" 
               class="flex gap-3 p-3 bg-gray-50 rounded">
            <div class="text-xs text-muted-foreground">
              {{ formatTime(entry.timestamp) }}
            </div>
            <div class="flex-1">
              <p class="text-sm">{{ entry.message }}</p>
            </div>
          </div>
        </div>
        
        <!-- Quick Notes -->
        <div class="mt-4">
          <Textarea 
            v-model="quickNote"
            placeholder="Add brew day notes..."
            class="min-h-[80px]"
            @keydown.ctrl.enter="addQuickNote"
          />
          <div class="flex justify-between mt-2">
            <p class="text-xs text-muted-foreground">Ctrl+Enter to save</p>
            <Button @click="addQuickNote" size="sm">Save Note</Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Measurement Dialog -->
    <MeasurementDialog 
      v-model:open="showMeasurementDialog"
      @save="addMeasurement"
    />

    <!-- Log Entry Dialog -->
    <LogEntryDialog 
      v-model:open="showLogDialog"
      @save="addLogEntry"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { Icon } from '#components'

const props = defineProps<{
  batch: any
  readonly?: boolean
}>()

const emit = defineEmits<{
  'start-fermentation': []
  'update-batch': [data: any]
}>()

// Dialog states
const showMeasurementDialog = ref(false)
const showLogDialog = ref(false)

// Measured values
const measuredValues = ref({
  mash: { ph: 5.36 },
  boil: { volume: 7.01 },
  preboil: { gravity: 1.057 },
  fermenter: { volume: 5.5 },
  originalGravity: 1.064
})

// Water calculations
const waterCalculations = computed(() => ({
  mashWater: (props.batch.batch_size * 0.6).toFixed(2),
  totalWater: (props.batch.batch_size * 1.1).toFixed(2),
  boilVolume: (props.batch.batch_size * 1.3).toFixed(2)
}))

// Stats calculations
const stats = computed(() => ({
  abv: 6,
  attenuation: 70.8,
  mashEfficiency: 78.3,
  brewhouseEfficiency: 70
}))

const calculatedEfficiency = computed(() => {
  return Math.round((measuredValues.value.originalGravity - 1) / (1.064 - 1) * 70)
})

// Hop schedule
const hopSchedule = ref([
  { name: 'Summit', amount: 9, time: 60, use: 'Boil', status: 'completed' },
  { name: 'Saaz', amount: 19.4, time: 15, use: 'Boil', status: 'pending' },
  { name: 'Amarillo', amount: 4.7, time: 20, use: 'Aroma', status: 'pending' },
  { name: 'Amarillo', amount: 19.4, time: 0, use: 'Dry Hop', status: 'pending' }
])

// Boil timer
const boilTimer = ref({
  totalTime: 60 * 60, // 60 minutes in seconds
  remainingTime: 60 * 60,
  running: false,
  display: '60:00'
})

let timerInterval: number | null = null

// Brew log
const brewLog = ref([
  { id: 1, timestamp: new Date(Date.now() - 30000), message: 'Mash started at 65°C' },
  { id: 2, timestamp: new Date(Date.now() - 15000), message: 'pH reading: 5.36' },
  { id: 3, timestamp: new Date(), message: 'Temperature holding steady' }
])

const quickNote = ref('')

// Check if brewing is complete
const isBrewingComplete = computed(() => {
  return boilTimer.value.remainingTime <= 0 && 
         hopSchedule.value.every(hop => hop.status === 'completed')
})

// Hop status helpers
const getHopStatus = (hop: any) => {
  if (hop.status === 'completed') return 'Added'
  if (hop.time <= (60 - Math.floor((boilTimer.value.totalTime - boilTimer.value.remainingTime) / 60))) {
    return 'Ready'
  }
  return 'Pending'
}

const getHopStatusClass = (hop: any) => {
  const status = getHopStatus(hop)
  if (status === 'Added') return 'bg-green-50 border-green-500'
  if (status === 'Ready') return 'bg-amber-50 border-amber-500'
  return 'bg-gray-50 border-gray-300'
}

const getHopBadgeVariant = (hop: any) => {
  const status = getHopStatus(hop)
  if (status === 'Added') return 'default'
  if (status === 'Ready') return 'warning'
  return 'secondary'
}

// Timer functions
const updateTimer = () => {
  if (boilTimer.value.remainingTime > 0) {
    boilTimer.value.remainingTime--
    const minutes = Math.floor(boilTimer.value.remainingTime / 60)
    const seconds = boilTimer.value.remainingTime % 60
    boilTimer.value.display = `${minutes}:${seconds.toString().padStart(2, '0')}`
  } else {
    boilTimer.value.display = '0:00'
    pauseBoilTimer()
  }
}

const startBoilTimer = () => {
  boilTimer.value.running = true
  timerInterval = setInterval(updateTimer, 1000)
}

const pauseBoilTimer = () => {
  boilTimer.value.running = false
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

const resetBoilTimer = () => {
  pauseBoilTimer()
  boilTimer.value.remainingTime = boilTimer.value.totalTime
  boilTimer.value.display = '60:00'
}

// Action handlers
const addHop = (hop: any) => {
  hop.status = 'completed'
  addLogEntry(`Added ${hop.amount}g ${hop.name} (${hop.use})`)
}

const addMashReading = () => {
  showMeasurementDialog.value = true
}

const mashOut = () => {
  addLogEntry('Mash out completed')
}

const pauseSession = () => {
  console.log('Pause brewing session')
}

const addMeasurement = (measurement: any) => {
  // Add measurement to measured values
  console.log('Add measurement:', measurement)
  showMeasurementDialog.value = false
}

const addLogEntry = (message: string) => {
  const entry = {
    id: brewLog.value.length + 1,
    timestamp: new Date(),
    message
  }
  brewLog.value.unshift(entry)
}

const addQuickNote = () => {
  if (quickNote.value.trim()) {
    addLogEntry(quickNote.value.trim())
    quickNote.value = ''
  }
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

// Cleanup timer on unmount
onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>