<template>
  <div class="space-y-6">
    <!-- Fermentation Tracker Component -->
    <FermentationTracker :batch-id="batch.id" />

    <!-- Action Buttons -->
    <Card>
      <CardHeader>
        <CardTitle>Progress Batch</CardTitle>
        <CardDescription>Move this batch to the next stage</CardDescription>
      </CardHeader>
      <CardContent class="space-y-3">
        <Button variant="default" class="w-full" @click="$emit('start-conditioning')">
          <Icon name="mdi:snowflake" class="mr-2 h-4 w-4" />
          Start Conditioning
        </Button>
        <Button variant="outline" class="w-full" @click="packageBeer">
          <Icon name="mdi:bottle-wine" class="mr-2 h-4 w-4" />
          Package Beer
        </Button>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '#components'
import FermentationTracker from '@/components/batch/FermentationTracker.vue'

const props = defineProps<{
  batch: any
}>()

const emit = defineEmits<{
  'start-conditioning': []
  'update-batch': [data: any]
}>()

const packageBeer = () => {
  // Handle packaging logic
  console.log('Package beer - navigating to packaged phase')
  emit('update-batch', { status: 'packaging' })
}
</script>
