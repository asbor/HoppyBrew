<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <div :class="cn('flex flex-col gap-y-ha-xs p-ha-md', props.class)">
    <slot />
  </div>
</template>
