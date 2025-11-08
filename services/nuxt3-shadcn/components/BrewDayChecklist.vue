<template>
  <Card class="w-full">
    <CardHeader>
      <div class="flex items-center justify-between">
        <div>
          <CardTitle>Brew Day Checklist</CardTitle>
          <CardDescription>Track your brew day progress step by step</CardDescription>
        </div>
        <Badge v-if="completedSteps > 0" variant="secondary">
          {{ completedSteps }}/{{ steps.length }} Complete
        </Badge>
      </div>
    </CardHeader>

    <CardContent>
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <div class="text-center space-y-4">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto"></div>
          <p class="text-muted-foreground">Loading brew steps...</p>
        </div>
      </div>

      <!-- Error State -->
      <Alert v-else-if="error" variant="destructive">
        <Icon name="mdi:alert-circle" class="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{{ error }}</AlertDescription>
      </Alert>

      <!-- No Steps State -->
      <div v-else-if="steps.length === 0" class="text-center py-8 space-y-4">
        <Icon name="mdi:clipboard-list-outline" class="mx-auto h-16 w-16 text-muted-foreground" />
        <div>
          <h3 class="text-lg font-semibold">No Brew Steps Yet</h3>
          <p class="text-muted-foreground">Generate brew steps from your recipe to get started.</p>
        </div>
        <Button @click="generateSteps" :disabled="generatingSteps">
          <Icon v-if="generatingSteps" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
          <Icon v-else name="mdi:plus" class="mr-2 h-4 w-4" />
          Generate Brew Steps
        </Button>
      </div>

      <!-- Brew Steps List -->
      <div v-else class="space-y-4">
        <!-- Progress Bar -->
        <div class="mb-6">
          <div class="flex justify-between text-sm mb-2">
            <span class="text-muted-foreground">Overall Progress</span>
            <span class="font-medium">{{ progressPercentage }}%</span>
          </div>
          <div class="w-full bg-secondary rounded-full h-2">
            <div
              class="bg-amber-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${progressPercentage}%` }"
            ></div>
          </div>
        </div>

        <!-- Steps -->
        <div
          v-for="(step, index) in steps"
          :key="step.id"
          class="border rounded-lg p-4 transition-all duration-200"
          :class="{
            'border-amber-500 bg-amber-50 dark:bg-amber-950': currentStepId === step.id && !step.completed,
            'border-green-500 bg-green-50 dark:bg-green-950': step.completed,
            'border-border': currentStepId !== step.id && !step.completed,
          }"
        >
          <div class="flex items-start gap-4">
            <!-- Step Number/Status Icon -->
            <div class="flex-shrink-0">
              <div
                v-if="step.completed"
                class="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center text-white"
              >
                <Icon name="mdi:check" class="h-6 w-6" />
              </div>
              <div
                v-else-if="currentStepId === step.id"
                class="w-10 h-10 rounded-full bg-amber-500 flex items-center justify-center text-white animate-pulse"
              >
                <Icon name="mdi:play" class="h-6 w-6" />
              </div>
              <div
                v-else
                class="w-10 h-10 rounded-full bg-secondary flex items-center justify-center text-muted-foreground font-semibold"
              >
                {{ index + 1 }}
              </div>
            </div>

            <!-- Step Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <div>
                  <h3 class="font-semibold text-lg">{{ step.step_name }}</h3>
                  <p v-if="step.notes" class="text-sm text-muted-foreground mt-1">{{ step.notes }}</p>
                </div>
                <Badge v-if="step.duration" variant="outline">
                  <Icon name="mdi:timer-outline" class="mr-1 h-3 w-3" />
                  {{ step.duration }} min
                </Badge>
              </div>

              <!-- Step Details -->
              <div v-if="step.temperature || step.started_at" class="mt-2 flex flex-wrap gap-3 text-sm">
                <span v-if="step.temperature" class="flex items-center text-muted-foreground">
                  <Icon name="mdi:thermometer" class="mr-1 h-4 w-4" />
                  {{ step.temperature }}°C
                </span>
                <span v-if="step.started_at && !step.completed" class="flex items-center text-muted-foreground">
                  <Icon name="mdi:clock-outline" class="mr-1 h-4 w-4" />
                  Started {{ formatTimeAgo(step.started_at) }}
                </span>
                <span v-if="step.completed_at" class="flex items-center text-green-600 dark:text-green-400">
                  <Icon name="mdi:check-circle" class="mr-1 h-4 w-4" />
                  Completed {{ formatTimeAgo(step.completed_at) }}
                </span>
              </div>

              <!-- Timer Display -->
              <div
                v-if="currentStepId === step.id && step.duration && timerSeconds > 0"
                class="mt-3 p-3 bg-background rounded-md border"
              >
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium">Time Remaining:</span>
                  <span class="text-2xl font-mono font-bold">{{ formatTimerDisplay(timerSeconds) }}</span>
                </div>
                <div class="mt-2">
                  <div class="w-full bg-secondary rounded-full h-1.5">
                    <div
                      class="bg-amber-600 h-1.5 rounded-full transition-all duration-1000"
                      :style="{ width: `${timerProgressPercentage}%` }"
                    ></div>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-3 flex flex-wrap gap-2">
                <Button
                  v-if="!step.completed && !step.started_at"
                  @click="startStep(step)"
                  size="sm"
                  class="bg-amber-600 hover:bg-amber-700"
                >
                  <Icon name="mdi:play" class="mr-2 h-4 w-4" />
                  Start Step
                </Button>
                <Button
                  v-if="step.started_at && !step.completed"
                  @click="completeStep(step)"
                  size="sm"
                  variant="default"
                >
                  <Icon name="mdi:check" class="mr-2 h-4 w-4" />
                  Mark Complete
                </Button>
                <Button
                  v-if="step.started_at && !step.completed && timerRunning"
                  @click="pauseTimer"
                  size="sm"
                  variant="outline"
                >
                  <Icon name="mdi:pause" class="mr-2 h-4 w-4" />
                  Pause Timer
                </Button>
                <Button
                  v-if="step.started_at && !step.completed && !timerRunning && timerSeconds > 0"
                  @click="resumeTimer"
                  size="sm"
                  variant="outline"
                >
                  <Icon name="mdi:play" class="mr-2 h-4 w-4" />
                  Resume Timer
                </Button>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-between items-center pt-4 border-t">
          <Button v-if="!anyStepStarted" @click="startFirstStep" variant="default" size="lg">
            <Icon name="mdi:rocket-launch" class="mr-2 h-5 w-5" />
            Start Brew Day
          </Button>
          <div v-else-if="allStepsCompleted" class="w-full text-center">
            <Alert class="bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800">
              <Icon name="mdi:check-circle" class="h-5 w-5 text-green-600 dark:text-green-400" />
              <AlertTitle class="text-green-800 dark:text-green-200">Brew Day Complete!</AlertTitle>
              <AlertDescription class="text-green-700 dark:text-green-300">
                All steps are completed. Your batch is ready for fermentation.
              </AlertDescription>
            </Alert>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useBrewSteps, type BrewStep } from '~/composables/useBrewSteps'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Button } from '~/components/ui/button'
import { Badge } from '~/components/ui/badge'
import { Alert, AlertDescription, AlertTitle } from '~/components/ui/alert'

const props = defineProps<{
  batchId: number
}>()

const { loading, error, getBrewSteps, updateBrewStep, createBrewSteps, startBrewDay } = useBrewSteps()

const steps = ref<BrewStep[]>([])
const currentStepId = ref<number | null>(null)
const timerSeconds = ref(0)
const timerRunning = ref(false)
const timerInterval = ref<NodeJS.Timeout | null>(null)
const generatingSteps = ref(false)

// Computed properties
const completedSteps = computed(() => steps.value.filter((s) => s.completed).length)
const progressPercentage = computed(() => {
  if (steps.value.length === 0) return 0
  return Math.round((completedSteps.value / steps.value.length) * 100)
})

const anyStepStarted = computed(() => steps.value.some((s) => s.started_at))
const allStepsCompleted = computed(() => steps.value.length > 0 && steps.value.every((s) => s.completed))

const timerProgressPercentage = computed(() => {
  const currentStep = steps.value.find((s) => s.id === currentStepId.value)
  if (!currentStep || !currentStep.duration) return 0
  const totalSeconds = currentStep.duration * 60
  return Math.max(0, Math.min(100, ((totalSeconds - timerSeconds.value) / totalSeconds) * 100))
})

// Methods
const fetchSteps = async () => {
  try {
    steps.value = await getBrewSteps(props.batchId)
    // Find the current active step
    const activeStep = steps.value.find((s) => s.started_at && !s.completed)
    if (activeStep) {
      currentStepId.value = activeStep.id
      startTimerForStep(activeStep)
    }
  } catch (e) {
    console.error('Error fetching brew steps:', e)
  }
}

const generateSteps = async () => {
  generatingSteps.value = true
  try {
    steps.value = await createBrewSteps(props.batchId)
  } catch (e) {
    console.error('Error generating brew steps:', e)
  } finally {
    generatingSteps.value = false
  }
}

const startFirstStep = async () => {
  try {
    const firstStep = await startBrewDay(props.batchId)
    await fetchSteps()
    currentStepId.value = firstStep.id
    startTimerForStep(firstStep)
  } catch (e) {
    console.error('Error starting brew day:', e)
  }
}

const startStep = async (step: BrewStep) => {
  try {
    const updatedStep = await updateBrewStep(step.id, {
      started_at: new Date().toISOString(),
    })
    step.started_at = updatedStep.started_at
    currentStepId.value = step.id
    startTimerForStep(step)
    saveProgress()
  } catch (e) {
    console.error('Error starting step:', e)
  }
}

const completeStep = async (step: BrewStep) => {
  try {
    const updatedStep = await updateBrewStep(step.id, {
      completed: true,
      completed_at: new Date().toISOString(),
    })
    step.completed = updatedStep.completed
    step.completed_at = updatedStep.completed_at
    stopTimer()
    currentStepId.value = null
    saveProgress()
    
    // Send notification
    sendNotification(step.step_name, 'Step completed!')
    
    // Auto-start next step if available
    const nextStep = steps.value.find((s) => !s.started_at && !s.completed)
    if (nextStep) {
      // Small delay before starting next step
      setTimeout(() => {
        const confirmStart = confirm(`Start next step: ${nextStep.step_name}?`)
        if (confirmStart) {
          startStep(nextStep)
        }
      }, 500)
    }
  } catch (e) {
    console.error('Error completing step:', e)
  }
}

const startTimerForStep = (step: BrewStep) => {
  if (!step.duration || !step.started_at) return
  
  const startedAt = new Date(step.started_at).getTime()
  const now = Date.now()
  const elapsed = Math.floor((now - startedAt) / 1000)
  const totalSeconds = step.duration * 60
  timerSeconds.value = Math.max(0, totalSeconds - elapsed)
  
  if (timerSeconds.value > 0) {
    timerRunning.value = true
    startTimer()
  }
}

const startTimer = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  
  timerInterval.value = setInterval(() => {
    if (timerSeconds.value > 0) {
      timerSeconds.value--
      
      // Send notification when timer completes
      if (timerSeconds.value === 0) {
        const currentStep = steps.value.find((s) => s.id === currentStepId.value)
        if (currentStep) {
          sendNotification('Timer Complete!', `${currentStep.step_name} timer has finished.`)
        }
        stopTimer()
      }
    } else {
      stopTimer()
    }
  }, 1000)
}

const stopTimer = () => {
  timerRunning.value = false
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const pauseTimer = () => {
  timerRunning.value = false
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const resumeTimer = () => {
  timerRunning.value = true
  startTimer()
}

const formatTimerDisplay = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

const formatTimeAgo = (timestamp: string): string => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins} min ago`
  
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
}

const sendNotification = (title: string, body: string) => {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body, icon: '/favicon.ico' })
  }
}

const requestNotificationPermission = () => {
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission()
  }
}

const saveProgress = () => {
  // Auto-save is handled by the API calls
  console.log('Progress auto-saved')
}

// Lifecycle
onMounted(() => {
  fetchSteps()
  requestNotificationPermission()
})

onUnmounted(() => {
  stopTimer()
})

// Watch for batch ID changes
watch(() => props.batchId, () => {
  stopTimer()
  fetchSteps()
})
</script>
