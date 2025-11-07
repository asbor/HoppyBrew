<template>
  <label
    :class="cn(
      'inline-flex items-center gap-2 text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
      props.class
    )"
  >
    <input
      v-model="localChecked"
      type="checkbox"
      :disabled="disabled"
      class="peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground"
      :class="cn(
        'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        localChecked && 'bg-primary text-primary-foreground'
      )"
    />
    <slot />
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

interface CheckboxProps {
  checked?: boolean
  disabled?: boolean
  class?: string
}

const props = withDefaults(defineProps<CheckboxProps>(), {
  checked: false,
  disabled: false,
  class: ''
})

const emit = defineEmits<{
  'update:checked': [value: boolean]
}>()

const localChecked = computed({
  get: () => props.checked,
  set: (value: boolean) => emit('update:checked', value)
})
</script>