<template>
  <div class="flex flex-col space-y-1.5 text-center sm:text-left">
    <DialogTitle v-if="title" :class="cn('text-lg font-semibold leading-none tracking-tight', titleClass)">
      {{ title }}
    </DialogTitle>
    <DialogDescription v-if="description" :class="cn('text-sm text-muted-foreground', descriptionClass)">
      {{ description }}
    </DialogDescription>
    <slot />
  </div>
</template>

<script setup lang="ts">
import { DialogTitle, DialogDescription } from 'radix-vue'
import { cn } from '~/lib/utils'

interface Props {
  title?: string
  description?: string
  titleClass?: string
  descriptionClass?: string
}

defineProps<Props>()
</script>