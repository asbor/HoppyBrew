<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { WorkflowHistoryEntry } from '@/composables/useBatches'

interface Props {
  batchId: string
}

const props = defineProps<Props>()
const { fetchWorkflowHistory } = useBatches()
const { getBatchStatusColor } = useStatusColors()

const workflowHistory = ref<WorkflowHistoryEntry[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// Load workflow history on mount
onMounted(async () => {
  loading.value = true
  const response = await fetchWorkflowHistory(props.batchId)
  
  if (response.error.value) {
    error.value = response.error.value
  } else {
    workflowHistory.value = response.data.value || []
  }
  
  loading.value = false
})

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getStatusLabel(status: string) {
  return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Workflow Timeline</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading" class="text-center py-4">
        Loading workflow history...
      </div>
      
      <div v-else-if="error" class="text-red-500 text-center py-4">
        {{ error }}
      </div>
      
      <div v-else-if="workflowHistory.length === 0" class="text-center py-4 text-gray-500">
        No workflow history available
      </div>
      
      <div v-else class="relative">
        <!-- Timeline line -->
        <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200" />
        
        <!-- Timeline entries -->
        <div class="space-y-6">
          <div
            v-for="(entry, index) in workflowHistory"
            :key="entry.id"
            class="relative flex items-start gap-4"
          >
            <!-- Timeline dot -->
            <div class="relative z-10 flex-shrink-0">
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center"
                :class="getBatchStatusColor(entry.to_status)"
              >
                <div class="w-3 h-3 bg-white rounded-full" />
              </div>
            </div>
            
            <!-- Entry content -->
            <div class="flex-1 pb-6">
              <div class="flex items-center gap-2 mb-1">
                <Badge 
                  :class="getBatchStatusColor(entry.to_status)"
                  class="text-white"
                >
                  {{ getStatusLabel(entry.to_status) }}
                </Badge>
                <span class="text-sm text-gray-500">
                  {{ formatDate(entry.changed_at) }}
                </span>
              </div>
              
              <div v-if="entry.from_status" class="text-sm text-gray-600 mb-1">
                From: {{ getStatusLabel(entry.from_status) }}
              </div>
              
              <div v-if="entry.notes" class="text-sm text-gray-700 mt-2">
                {{ entry.notes }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
