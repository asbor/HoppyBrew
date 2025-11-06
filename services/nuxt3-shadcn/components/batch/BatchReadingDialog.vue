<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>Add Reading</DialogTitle>
        <DialogDescription>Record a new measurement</DialogDescription>
      </DialogHeader>
      
      <div class="space-y-4">
        <div>
          <label class="text-sm font-medium">Reading Date</label>
          <Input v-model="formData.reading_date" type="datetime-local" />
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
          <Input v-model="formData.ph" type="number" step="0.1" placeholder="4.2" />
        </div>
        <div>
          <label class="text-sm font-medium">Notes (optional)</label>
          <Textarea v-model="formData.notes" placeholder="Additional notes about this reading..." />
        </div>
      </div>

      <DialogFooter>
        <Button @click="$emit('update:open', false)" variant="outline">Cancel</Button>
        <Button @click="save">Save Reading</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

const props = defineProps<{
  open: boolean
  batchId: string
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'save': [data: any]
}>()

const formData = ref({
  reading_date: new Date().toISOString().slice(0, 16),
  gravity: '',
  temperature: '',
  ph: '',
  notes: ''
})

const save = () => {
  const data = {
    batch_id: props.batchId,
    ...formData.value,
    gravity: parseFloat(formData.value.gravity),
    temperature: parseFloat(formData.value.temperature),
    ph: formData.value.ph ? parseFloat(formData.value.ph) : null
  }
  emit('save', data)
  
  // Reset form
  formData.value = {
    reading_date: new Date().toISOString().slice(0, 16),
    gravity: '',
    temperature: '',
    ph: '',
    notes: ''
  }
}
</script>