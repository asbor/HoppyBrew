<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Badge } from '~/components/ui/badge'

const props = defineProps<{
  og?: number
  fg?: number
  grainWeight?: number
  grainColor?: number
  batchSize?: number
  hopAdditions?: Array<{
    alphaAcid: number
    weight: number
    boilTime: number
  }>
  boilGravity?: number
}>()

const calculators = useCalculators()

// Calculate ABV
const abvResult = computed(() => {
  if (!props.og || !props.fg) return null
  return calculators.calculateABV(props.og, props.fg)
})

// Calculate SRM
const srmResult = computed(() => {
  if (!props.grainColor || !props.grainWeight || !props.batchSize) return null
  return calculators.calculateSRM(props.grainColor, props.grainWeight, props.batchSize)
})

// Calculate total IBU from all hop additions
const totalIBU = computed(() => {
  if (!props.hopAdditions || !props.batchSize || !props.boilGravity) return null
  
  const total = props.hopAdditions.reduce((sum, hop) => {
    const result = calculators.calculateIBU(
      hop.alphaAcid,
      hop.weight,
      hop.boilTime,
      props.batchSize,
      props.boilGravity
    )
    return sum + result.ibu
  }, 0)
  
  return { ibu: total, formatted: `${total.toFixed(1)} IBU` }
})

// Calculate attenuation
const attenuation = computed(() => {
  if (!props.og || !props.fg) return null
  return calculators.calculateAttenuation(props.og, props.fg)
})
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-lg">Recipe Statistics</CardTitle>
      <CardDescription>Calculated values based on recipe</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- ABV -->
        <div v-if="abvResult" class="space-y-1">
          <p class="text-xs text-muted-foreground">Alcohol by Volume</p>
          <p class="text-2xl font-bold text-primary">{{ abvResult.abv.toFixed(2) }}%</p>
          <Badge variant="outline" class="text-xs">ABV</Badge>
        </div>

        <!-- IBU -->
        <div v-if="totalIBU" class="space-y-1">
          <p class="text-xs text-muted-foreground">Bitterness</p>
          <p class="text-2xl font-bold text-primary">{{ totalIBU.ibu.toFixed(1) }}</p>
          <Badge variant="outline" class="text-xs">IBU</Badge>
        </div>

        <!-- SRM -->
        <div v-if="srmResult" class="space-y-1">
          <p class="text-xs text-muted-foreground">Color</p>
          <div class="flex items-center gap-2">
            <p class="text-2xl font-bold text-primary">{{ srmResult.srm.toFixed(1) }}</p>
            <div 
              class="w-8 h-8 rounded border-2 border-gray-300"
              :style="{ backgroundColor: srmResult.color }"
            ></div>
          </div>
          <Badge variant="outline" class="text-xs">SRM</Badge>
        </div>

        <!-- Attenuation -->
        <div v-if="attenuation" class="space-y-1">
          <p class="text-xs text-muted-foreground">Attenuation</p>
          <p class="text-2xl font-bold text-primary">{{ attenuation.attenuation.toFixed(1) }}%</p>
          <Badge variant="outline" class="text-xs">Atten.</Badge>
        </div>

        <!-- Original Gravity -->
        <div v-if="og" class="space-y-1">
          <p class="text-xs text-muted-foreground">Original Gravity</p>
          <p class="text-xl font-semibold">{{ og.toFixed(3) }}</p>
        </div>

        <!-- Final Gravity -->
        <div v-if="fg" class="space-y-1">
          <p class="text-xs text-muted-foreground">Final Gravity</p>
          <p class="text-xl font-semibold">{{ fg.toFixed(3) }}</p>
        </div>

        <!-- Batch Size -->
        <div v-if="batchSize" class="space-y-1">
          <p class="text-xs text-muted-foreground">Batch Size</p>
          <p class="text-xl font-semibold">{{ batchSize.toFixed(1) }}L</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!abvResult && !totalIBU && !srmResult" class="text-center py-6 text-muted-foreground">
        <p class="text-sm">Enter recipe values to see calculated statistics</p>
      </div>
    </CardContent>
  </Card>
</template>
