<template>
  <div class="space-y-6">
    <!-- Quality Control Tests -->
    <QCTestList :batch-id="batch.id" />

    <!-- Batch Actions -->
    <Card>
      <CardHeader>
        <CardTitle>Packaging Status</CardTitle>
        <CardDescription>Beer has been packaged and is carbonating</CardDescription>
      </CardHeader>
      <CardContent>
        <p class="text-muted-foreground mb-4">
          Your beer is now packaged. Conduct quality control tests to evaluate the final product
          before marking the batch as complete.
        </p>
        <Button @click="$emit('complete-batch')">
          <Icon name="mdi:check-circle" class="mr-2 h-4 w-4" />
          Mark Batch Complete
        </Button>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '#components'
import QCTestList from './QCTestList.vue'

defineProps<{ batch: any }>()
defineEmits<{
  'complete-batch': []
  'update-batch': [data: any]
}>()
</script>