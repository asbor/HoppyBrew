<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import type { Batch, BatchStatus } from '@/composables/useBatches'

interface Props {
  batch: Batch
}

const props = defineProps<Props>()
const emit = defineEmits(['statusUpdated'])

const { updateStatus, fetchValidTransitions } = useBatches()
const { getBatchStatusColor } = useStatusColors()

const selectedStatus = ref<BatchStatus | null>(null)
const notes = ref('')
const validTransitions = ref<BatchStatus[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)

// Load valid transitions on mount
onMounted(async () => {
  const response = await fetchValidTransitions(props.batch.id)
  
  if (response.data.value) {
    validTransitions.value = response.data.value.valid_transitions
  }
})

async function handleStatusUpdate() {
  if (!selectedStatus.value) {
    error.value = 'Please select a status'
    return
  }
  
  loading.value = true
  error.value = null
  successMessage.value = null
  
  const response = await updateStatus(props.batch.id, {
    status: selectedStatus.value,
    notes: notes.value || undefined
  })
  
  if (response.error.value) {
    error.value = response.error.value
  } else {
    successMessage.value = 'Status updated successfully!'
    notes.value = ''
    selectedStatus.value = null
    emit('statusUpdated', response.data.value)
    
    // Reload valid transitions for the new status
    const transitionsResponse = await fetchValidTransitions(props.batch.id)
    if (transitionsResponse.data.value) {
      validTransitions.value = transitionsResponse.data.value.valid_transitions
    }
  }
  
  loading.value = false
}

function getStatusLabel(status: string) {
  return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Update Batch Status</CardTitle>
      <CardDescription>
        Change the status of this batch through the workflow
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="space-y-4">
        <!-- Current Status -->
        <div>
          <Label class="text-sm font-medium">Current Status</Label>
          <div class="mt-1">
            <span 
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium text-white"
              :class="getBatchStatusColor(batch.status)"
            >
              {{ getStatusLabel(batch.status) }}
            </span>
          </div>
        </div>
        
        <!-- New Status Selection -->
        <div v-if="validTransitions.length > 0">
          <Label for="status-select">New Status</Label>
          <Select v-model="selectedStatus">
            <SelectTrigger id="status-select" class="mt-1">
              <SelectValue placeholder="Select new status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem 
                v-for="status in validTransitions" 
                :key="status" 
                :value="status"
              >
                {{ getStatusLabel(status) }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <!-- No valid transitions message -->
        <div v-else class="text-sm text-gray-500">
          No valid status transitions available from the current status.
        </div>
        
        <!-- Notes -->
        <div v-if="validTransitions.length > 0">
          <Label for="notes">Notes (optional)</Label>
          <Textarea
            id="notes"
            v-model="notes"
            placeholder="Add notes about this status change..."
            class="mt-1"
            rows="3"
          />
        </div>
        
        <!-- Error Message -->
        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>
        
        <!-- Success Message -->
        <div v-if="successMessage" class="text-green-600 text-sm">
          {{ successMessage }}
        </div>
        
        <!-- Update Button -->
        <Button 
          v-if="validTransitions.length > 0"
          @click="handleStatusUpdate"
          :disabled="!selectedStatus || loading"
          class="w-full"
        >
          {{ loading ? 'Updating...' : 'Update Status' }}
        </Button>
      </div>
    </CardContent>
  </Card>
</template>
