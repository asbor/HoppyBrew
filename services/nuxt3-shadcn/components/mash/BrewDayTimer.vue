<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Button } from '~/components/ui/button'
import { Badge } from '~/components/ui/badge'
import { PlayIcon, PauseIcon, StopIcon, CheckIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps<{
  steps: MashStep[]
  profileName?: string
}>()

// Types
interface MashStep {
  id?: number
  name: string
  type: string
  step_temp: number
  step_time: number
  ramp_time?: number
  description?: string
}

// State
const currentStepIndex = ref(0)
const isRunning = ref(false)
const isPaused = ref(false)
const elapsedSeconds = ref(0)
const startTime = ref<number | null>(null)
const pausedAt = ref<number | null>(null)
const totalPausedTime = ref(0)

let timerInterval: any = null

// Computed
const currentStep = computed(() => {
  if (currentStepIndex.value >= props.steps.length) return null
  return props.steps[currentStepIndex.value]
})

const currentStepDurationSeconds = computed(() => {
  if (!currentStep.value) return 0
  return (currentStep.value.step_time + (currentStep.value.ramp_time || 0)) * 60
})

const remainingSeconds = computed(() => {
  return Math.max(0, currentStepDurationSeconds.value - elapsedSeconds.value)
})

const progress = computed(() => {
  if (currentStepDurationSeconds.value === 0) return 0
  return (elapsedSeconds.value / currentStepDurationSeconds.value) * 100
})

const totalMashTime = computed(() => {
  return props.steps.reduce((total, step) => {
    return total + (step.step_time || 0) + (step.ramp_time || 0)
  }, 0)
})

const completedTime = computed(() => {
  let time = 0
  for (let i = 0; i < currentStepIndex.value; i++) {
    time += (props.steps[i].step_time || 0) + (props.steps[i].ramp_time || 0)
  }
  time += Math.floor(elapsedSeconds.value / 60)
  return time
})

// Format time
const formatTime = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`
}

// Timer functions
const startTimer = () => {
  if (isPaused.value) {
    // Resume from pause
    if (pausedAt.value && startTime.value) {
      totalPausedTime.value += Date.now() - pausedAt.value
      pausedAt.value = null
    }
    isPaused.value = false
  } else {
    // Start fresh
    startTime.value = Date.now()
    totalPausedTime.value = 0
    elapsedSeconds.value = 0
  }
  
  isRunning.value = true
  
  timerInterval = setInterval(() => {
    if (startTime.value && !isPaused.value) {
      const elapsed = Date.now() - startTime.value - totalPausedTime.value
      elapsedSeconds.value = Math.floor(elapsed / 1000)
      
      // Check if step is complete
      if (elapsedSeconds.value >= currentStepDurationSeconds.value) {
        nextStep()
      }
    }
  }, 100)
}

const pauseTimer = () => {
  isPaused.value = true
  pausedAt.value = Date.now()
}

const stopTimer = () => {
  if (confirm('Are you sure you want to stop the timer? Progress will be lost.')) {
    resetTimer()
  }
}

const resetTimer = () => {
  isRunning.value = false
  isPaused.value = false
  currentStepIndex.value = 0
  elapsedSeconds.value = 0
  startTime.value = null
  pausedAt.value = null
  totalPausedTime.value = 0
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

const nextStep = () => {
  if (currentStepIndex.value < props.steps.length - 1) {
    currentStepIndex.value++
    elapsedSeconds.value = 0
    startTime.value = Date.now()
    totalPausedTime.value = 0
    
    // Play notification sound (optional)
    if (typeof Audio !== 'undefined') {
      try {
        const audio = new Audio('/notification.mp3')
        audio.play().catch(() => {
          // Ignore audio errors
        })
      } catch (e) {
        // Ignore audio errors
      }
    }
    
    // Browser notification
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('Mash Step Complete', {
        body: `Next step: ${props.steps[currentStepIndex.value].name}`,
        icon: '/logo.png'
      })
    }
  } else {
    // All steps complete
    resetTimer()
    alert('Mash schedule complete! 🎉')
  }
}

const skipToStep = (index: number) => {
  if (confirm(`Skip to step ${index + 1}?`)) {
    currentStepIndex.value = index
    elapsedSeconds.value = 0
    startTime.value = Date.now()
    totalPausedTime.value = 0
  }
}

// Request notification permission
const requestNotificationPermission = () => {
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission()
  }
}

onMounted(() => {
  requestNotificationPermission()
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>

<template>
  <div class="space-y-4">
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Brew Day Timer</CardTitle>
            <CardDescription v-if="profileName">{{ profileName }}</CardDescription>
          </div>
          <Badge v-if="isRunning && !isPaused" class="bg-green-500">
            Running
          </Badge>
          <Badge v-else-if="isPaused" class="bg-yellow-500">
            Paused
          </Badge>
        </div>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- Current step display -->
        <div v-if="currentStep" class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-2xl font-bold">{{ currentStep.name }}</h3>
              <p class="text-sm text-muted-foreground">Step {{ currentStepIndex + 1 }} of {{ steps.length }}</p>
            </div>
            <div class="text-right">
              <div class="text-4xl font-bold">{{ formatTime(remainingSeconds) }}</div>
              <p class="text-sm text-muted-foreground">remaining</p>
            </div>
          </div>

          <!-- Progress bar -->
          <div class="relative w-full h-4 bg-gray-200 rounded-full overflow-hidden">
            <div 
              class="absolute top-0 left-0 h-full bg-primary transition-all duration-300"
              :style="{ width: `${progress}%` }"
            />
          </div>

          <!-- Step details -->
          <div class="grid grid-cols-3 gap-4 p-4 bg-muted rounded-lg">
            <div class="text-center">
              <div class="text-2xl font-bold">{{ currentStep.step_temp }}°C</div>
              <div class="text-xs text-muted-foreground">Target Temp</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold">{{ currentStep.step_time }} min</div>
              <div class="text-xs text-muted-foreground">Duration</div>
            </div>
            <div v-if="currentStep.ramp_time" class="text-center">
              <div class="text-2xl font-bold">{{ currentStep.ramp_time }} min</div>
              <div class="text-xs text-muted-foreground">Ramp Time</div>
            </div>
          </div>

          <p v-if="currentStep.description" class="text-sm text-muted-foreground italic">
            {{ currentStep.description }}
          </p>
        </div>

        <!-- Completion message -->
        <div v-else class="text-center py-8">
          <CheckIcon class="h-16 w-16 mx-auto text-green-500 mb-4" />
          <h3 class="text-xl font-bold">Mash Complete!</h3>
          <p class="text-muted-foreground">All steps have been completed</p>
        </div>

        <!-- Controls -->
        <div class="flex gap-2">
          <Button 
            v-if="!isRunning"
            @click="startTimer"
            class="flex-1"
            :disabled="!currentStep"
          >
            <PlayIcon class="h-4 w-4 mr-2" />
            Start
          </Button>
          <Button 
            v-else-if="!isPaused"
            @click="pauseTimer"
            class="flex-1"
            variant="outline"
          >
            <PauseIcon class="h-4 w-4 mr-2" />
            Pause
          </Button>
          <Button 
            v-else
            @click="startTimer"
            class="flex-1"
          >
            <PlayIcon class="h-4 w-4 mr-2" />
            Resume
          </Button>
          
          <Button 
            v-if="isRunning"
            @click="stopTimer"
            variant="destructive"
          >
            <StopIcon class="h-4 w-4 mr-2" />
            Stop
          </Button>
          
          <Button 
            v-if="isRunning && currentStepIndex < steps.length - 1"
            @click="nextStep"
            variant="outline"
          >
            Skip Step
          </Button>
        </div>

        <!-- Overall progress -->
        <div class="space-y-2 pt-4 border-t">
          <div class="flex justify-between text-sm">
            <span class="text-muted-foreground">Overall Progress</span>
            <span class="font-semibold">{{ completedTime }} / {{ totalMashTime }} minutes</span>
          </div>
          <div class="relative w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              class="absolute top-0 left-0 h-full bg-green-500 transition-all duration-300"
              :style="{ width: `${(completedTime / totalMashTime) * 100}%` }"
            />
          </div>
        </div>

        <!-- Step timeline -->
        <div class="space-y-2">
          <h4 class="font-semibold text-sm">Mash Schedule</h4>
          <div class="space-y-2">
            <button
              v-for="(step, index) in steps"
              :key="index"
              @click="isRunning ? skipToStep(index) : null"
              class="w-full text-left p-3 rounded-lg border transition-all"
              :class="{
                'border-primary bg-primary/10': index === currentStepIndex,
                'border-green-500 bg-green-50 opacity-60': index < currentStepIndex,
                'border-gray-200 hover:border-gray-300': index > currentStepIndex,
                'cursor-pointer': isRunning
              }"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold"
                    :class="{
                      'bg-primary text-primary-foreground': index === currentStepIndex,
                      'bg-green-500 text-white': index < currentStepIndex,
                      'bg-gray-200 text-gray-600': index > currentStepIndex
                    }"
                  >
                    <CheckIcon v-if="index < currentStepIndex" class="h-4 w-4" />
                    <template v-else>{{ index + 1 }}</template>
                  </div>
                  <div>
                    <div class="font-medium">{{ step.name }}</div>
                    <div class="text-xs text-muted-foreground">
                      {{ step.step_temp }}°C • {{ step.step_time }}min
                      <template v-if="step.ramp_time"> • {{ step.ramp_time }}min ramp</template>
                    </div>
                  </div>
                </div>
                <Badge variant="outline">{{ step.type }}</Badge>
              </div>
            </button>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
