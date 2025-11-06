<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>Add Note</DialogTitle>
        <DialogDescription>Add a note to the batch log</DialogDescription>
      </DialogHeader>
      
      <div class="space-y-4">
        <div>
          <label class="text-sm font-medium">Note</label>
          <Textarea 
            v-model="noteText" 
            placeholder="Enter your note here..."
            class="min-h-[100px]"
          />
        </div>
      </div>

      <DialogFooter>
        <Button @click="$emit('update:open', false)" variant="outline">Cancel</Button>
        <Button @click="save" :disabled="!noteText.trim()">Save Note</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

const props = defineProps<{
  open: boolean
  batchId: string
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'save': [data: any]
}>()

const noteText = ref('')

const save = () => {
  if (noteText.value.trim()) {
    const data = {
      batch_id: props.batchId,
      message: noteText.value.trim(),
      timestamp: new Date().toISOString()
    }
    emit('save', data)
    noteText.value = ''
  }
}
</script>