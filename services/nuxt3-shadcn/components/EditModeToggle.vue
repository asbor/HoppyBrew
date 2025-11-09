<template>
  <div class="flex items-center gap-3 p-3 bg-muted/50 rounded-lg border border-border">
    <div class="flex items-center gap-2">
      <Icon 
        :name="isEditMode ? 'mdi:pencil' : 'mdi:eye'" 
        :class="isEditMode ? 'text-orange-600' : 'text-blue-600'"
        class="h-5 w-5"
      />
      <span class="text-sm font-medium text-card-foreground">
        {{ isEditMode ? 'Edit Mode' : 'View Mode' }}
      </span>
    </div>
    
    <div class="flex-1">
      <p class="text-xs text-muted-foreground">
        {{ isEditMode 
          ? 'You can modify data. Click to switch to view-only mode.' 
          : 'Data is protected from changes. Click to enable editing.' 
        }}
      </p>
    </div>

    <Button 
      :variant="isEditMode ? 'default' : 'outline'"
      size="sm"
      @click="toggleMode"
      class="shrink-0"
    >
      <Icon 
        :name="isEditMode ? 'mdi:eye' : 'mdi:pencil'" 
        class="h-4 w-4 mr-2"
      />
      {{ isEditMode ? 'View Only' : 'Enable Editing' }}
    </Button>
  </div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Icon } from '#components'

interface Props {
  modelValue: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const isEditMode = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value)
})

const toggleMode = () => {
  isEditMode.value = !isEditMode.value
}
</script>
