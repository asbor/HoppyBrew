<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const api = useApi()

const logContent = ref<string | null>(null)
const previousLogContent = ref<string | null>(null)
const isAutoScroll = ref(true)
const isPaused = ref(false)
const logContainer = ref<HTMLElement | null>(null)

// Format log content with color coding
const formattedLogContent = computed(() => {
  if (!logContent.value) return ''

  const lines = logContent.value.split('\n')
  
  return lines.map(line => {
    let className = 'text-foreground'
    if (line.includes('ERROR')) {
      className = 'text-red-500 dark:text-red-400 font-semibold'
    } else if (line.includes('WARNING')) {
      className = 'text-orange-500 dark:text-orange-400'
    } else if (line.includes('INFO')) {
      className = 'text-blue-500 dark:text-blue-400'
    } else if (line.includes('DEBUG')) {
      className = 'text-green-500 dark:text-green-400'
    }
    return `<span class="${className}">${line}</span>`
  }).join('\n')
})

async function fetchLogContent() {
  if (isPaused.value) return

  try {
    const response = await api.get<{ log_content: string }>('/api/logs')
    const newLogContent = response.data.value?.log_content ?? ''

    // Always update on first load, and whenever content changes
    if (previousLogContent.value === null || newLogContent !== previousLogContent.value) {
      logContent.value = newLogContent
      previousLogContent.value = newLogContent

      if (isAutoScroll.value) {
        scrollToBottom()
      }
    }
  } catch (error) {
    console.error('Failed to fetch log content:', error)
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}

function togglePause() {
  isPaused.value = !isPaused.value
}

function clearLogs() {
  logContent.value = ''
}

function downloadLogs() {
  if (!logContent.value) return
  
  // Create safe filename for Windows and other OSes
  const now = new Date()
  const timestamp = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}-${String(now.getMinutes()).padStart(2, '0')}-${String(now.getSeconds()).padStart(2, '0')}`
  
  const blob = new Blob([logContent.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `hoppybrew-logs-${timestamp}.txt`
  a.click()
  URL.revokeObjectURL(url)
}

// Update logs periodically
let updateInterval: NodeJS.Timeout | null = null

function startUpdates() {
  updateInterval = setInterval(fetchLogContent, 1000)
}

function stopUpdates() {
  if (updateInterval) {
    clearInterval(updateInterval)
    updateInterval = null
  }
}

function handleVisibilityChange() {
  if (document.hidden) {
    stopUpdates()
  } else {
    startUpdates()
  }
}

onMounted(() => {
  fetchLogContent()
  startUpdates()
  document.addEventListener('visibilitychange', handleVisibilityChange)
})

onBeforeUnmount(() => {
  stopUpdates()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold">System Logs</h1>
        <p class="text-muted-foreground">Real-time application logs and diagnostics</p>
      </div>
      <div class="flex gap-2">
        <Button 
          @click="togglePause" 
          variant="outline"
          size="sm"
        >
          <Icon :name="isPaused ? 'mdi:play' : 'mdi:pause'" class="mr-2 h-4 w-4" />
          {{ isPaused ? 'Resume' : 'Pause' }}
        </Button>
        <Button 
          @click="scrollToBottom" 
          variant="outline"
          size="sm"
        >
          <Icon name="mdi:arrow-down" class="mr-2 h-4 w-4" />
          Scroll to Bottom
        </Button>
        <Button 
          @click="downloadLogs" 
          variant="outline"
          size="sm"
          :disabled="!logContent"
        >
          <Icon name="mdi:download" class="mr-2 h-4 w-4" />
          Download
        </Button>
      </div>
    </header>

    <!-- Log Stats -->
    <div class="flex gap-4 flex-wrap">
      <div class="flex items-center gap-2">
        <Badge variant="outline" class="text-red-500 border-red-500">
          <Icon name="mdi:alert-circle" class="mr-1 h-3 w-3" />
          Errors
        </Badge>
      </div>
      <div class="flex items-center gap-2">
        <Badge variant="outline" class="text-orange-500 border-orange-500">
          <Icon name="mdi:alert" class="mr-1 h-3 w-3" />
          Warnings
        </Badge>
      </div>
      <div class="flex items-center gap-2">
        <Badge variant="outline" class="text-blue-500 border-blue-500">
          <Icon name="mdi:information" class="mr-1 h-3 w-3" />
          Info
        </Badge>
      </div>
      <div class="flex items-center gap-2">
        <Badge variant="outline" class="text-green-500 border-green-500">
          <Icon name="mdi:bug" class="mr-1 h-3 w-3" />
          Debug
        </Badge>
      </div>
      <div class="ml-auto flex items-center gap-2">
        <label class="text-sm text-muted-foreground flex items-center gap-2 cursor-pointer">
          <input 
            type="checkbox" 
            v-model="isAutoScroll" 
            class="rounded border-input"
          />
          Auto-scroll
        </label>
      </div>
    </div>

    <!-- Log Viewer -->
    <Card>
      <CardContent class="p-0">
        <div 
          ref="logContainer"
          class="h-[600px] overflow-y-auto bg-background font-mono text-sm"
        >
          <pre 
            v-if="logContent" 
            v-html="formattedLogContent"
            class="p-4 whitespace-pre-wrap break-words"
          ></pre>
          <div v-else class="p-8 text-center text-muted-foreground">
            <Icon name="mdi:file-document-outline" class="mx-auto h-12 w-12 mb-2" />
            <p>No logs available</p>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Info Message -->
    <Card class="bg-muted/50">
      <CardContent class="p-4">
        <div class="flex items-start gap-3">
          <Icon name="mdi:information-outline" class="h-5 w-5 text-muted-foreground mt-0.5" />
          <div class="text-sm text-muted-foreground">
            <p>Logs are updated automatically every second. Use the Pause button to stop updates while reviewing. 
            Color coding helps identify different log levels: 
            <span class="text-red-500">errors</span>, 
            <span class="text-orange-500">warnings</span>, 
            <span class="text-blue-500">info</span>, and 
            <span class="text-green-500">debug</span> messages.</p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
