<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = withDefaults(
  defineProps<{
    class?: HTMLAttributes['class']
    orientation?: 'horizontal' | 'vertical'
    decorative?: boolean
  }>(),
  {
    orientation: 'horizontal',
    decorative: false,
  },
)

const ariaOrientation = computed(() =>
  props.decorative || props.orientation === 'horizontal'
    ? undefined
    : 'vertical',
)
</script>

<template>
  <div
    role="separator"
    :aria-orientation="ariaOrientation"
    :class="
      cn(
        'shrink-0 bg-border',
        props.orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
        props.class,
      )
    "
  />
</template>
