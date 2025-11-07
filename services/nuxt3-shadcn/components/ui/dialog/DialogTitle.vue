<template>
  <DialogTitle :class="cn('text-lg font-semibold leading-none tracking-tight', className)" v-bind="$attrs">
    <slot />
  </DialogTitle>
</template>

<script setup lang="ts">
import { DialogTitle } from 'radix-vue'
import { cn } from '~/lib/utils'

interface Props {
  className?: string
}

defineProps<Props>()
</script>