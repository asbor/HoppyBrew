<template>
  <div class="space-y-6">
    <!-- Completion Summary -->
    <Card>
      <CardHeader>
        <CardTitle>Completed Batch</CardTitle>
        <CardDescription>Brewing process completed successfully</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p class="text-xs text-muted-foreground">Batch Name</p>
            <p class="font-medium">{{ batch.batch_name }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground">Batch Number</p>
            <p class="font-medium">#{{ batch.batch_number }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground">Batch Size</p>
            <p class="font-medium">{{ batch.batch_size }}L</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground">Status</p>
            <Badge class="bg-green-600">Completed</Badge>
          </div>
        </div>

        <Button @click="$emit('archive-batch')" variant="outline">
          <Icon name="mdi:archive" class="mr-2 h-4 w-4" />
          Archive Batch
        </Button>
      </CardContent>
    </Card>

    <!-- Quality Control Section -->
    <QualityControlPanel :batch-id="batch.id" />
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Icon } from '#components'
import QualityControlPanel from './QualityControlPanel.vue'

defineProps<{ batch: any }>()
defineEmits<{
  'archive-batch': []
  'update-batch': [data: any]
}>()
</script>