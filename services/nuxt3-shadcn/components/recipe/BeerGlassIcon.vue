<script setup lang="ts">
import { getBeerHexFromColor, getBeerTextColor } from '@/lib/beerColor'

interface Props {
  srm?: number | null
  size?: number
  label?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 48,
  srm: null,
  label: ''
})

const beerColor = computed(() => getBeerHexFromColor(props.srm))
const textColor = computed(() => getBeerTextColor(props.srm))
</script>

<template>
  <div class="relative flex items-center justify-center" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg :width="size" :height="size" viewBox="0 0 64 64" role="img" aria-label="Beer color">
      <!-- Glass outline -->
      <rect x="18" y="10" width="28" height="44" rx="5" ry="5" fill="#e5e7eb" stroke="#94a3b8" stroke-width="2" />
      <!-- Beer fill -->
      <rect x="20" y="18" width="24" height="32" rx="4" ry="4" :fill="beerColor" />
      <!-- Foam -->
      <rect x="18" y="10" width="28" height="10" rx="5" ry="5" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" />
      <circle cx="24" cy="16" r="3" fill="#fff" opacity="0.7" />
      <circle cx="32" cy="14" r="4" fill="#fff" opacity="0.8" />
      <circle cx="40" cy="16" r="3" fill="#fff" opacity="0.7" />
      <!-- Handle -->
      <path d="M46 18 h4 a4 4 0 0 1 4 4 v12 a6 6 0 0 1 -6 6 h-2" fill="none" stroke="#94a3b8" stroke-width="3" />
    </svg>
    <span v-if="label" class="absolute text-[10px] font-semibold px-1 rounded"
      :style="{ color: textColor, bottom: '2px' }">
      {{ label }}
    </span>
  </div>
</template>
