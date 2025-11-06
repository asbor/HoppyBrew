<template>
  <ScrollAreaRoot :class="cn('relative overflow-hidden', className)" v-bind="$attrs">
    <ScrollAreaViewport class="h-full w-full rounded-[inherit]">
      <slot />
    </ScrollAreaViewport>
    <ScrollAreaScrollbar
      class="flex touch-none select-none transition-colors"
      orientation="vertical"
    >
      <ScrollAreaThumb class="relative flex-1 rounded-full bg-border" />
    </ScrollAreaScrollbar>
    <ScrollAreaScrollbar
      class="flex touch-none select-none transition-colors"
      orientation="horizontal"
    >
      <ScrollAreaThumb class="relative flex-1 rounded-full bg-border" />
    </ScrollAreaScrollbar>
    <ScrollAreaCorner />
  </ScrollAreaRoot>
</template>

<script setup lang="ts">
import {
  ScrollAreaRoot,
  ScrollAreaViewport,
  ScrollAreaScrollbar,
  ScrollAreaThumb,
  ScrollAreaCorner
} from 'radix-vue'
import { cn } from '~/lib/utils'

interface Props {
  className?: string
}

defineProps<Props>()
</script>