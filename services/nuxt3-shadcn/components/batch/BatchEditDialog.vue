<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>Edit Batch</DialogTitle>
        <DialogDescription>Update batch information</DialogDescription>
      </DialogHeader>
      
      <div class="space-y-4">
        <div>
          <label class="text-sm font-medium">Batch Name</label>
          <Input v-model="formData.batch_name" />
        </div>
        <div>
          <label class="text-sm font-medium">Brewer</label>
          <Input v-model="formData.brewer" />
        </div>
        <div>
          <label class="text-sm font-medium">Batch Size (L)</label>
          <Input v-model="formData.batch_size" type="number" />
        </div>
        <div>
          <label class="text-sm font-medium">Brew Date</label>
          <Input v-model="formData.brew_date" type="datetime-local" />
        </div>
      </div>

      <DialogFooter>
        <Button @click="$emit('update:open', false)" variant="outline">Cancel</Button>
        <Button @click="save">Save</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const props = defineProps<{
  open: boolean
  batch: any
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'save': [data: any]
}>()

const formData = ref({
  batch_name: '',
  brewer: '',
  batch_size: 0,
  brew_date: ''
})

watch(() => props.batch, (newBatch) => {
  if (newBatch) {
    formData.value = {
      batch_name: newBatch.batch_name || '',
      brewer: newBatch.brewer || '',
      batch_size: newBatch.batch_size || 0,
      brew_date: newBatch.brew_date ? new Date(newBatch.brew_date).toISOString().slice(0, 16) : ''
    }
  }
}, { immediate: true })

const save = () => {
  emit('save', formData.value)
}
</script>