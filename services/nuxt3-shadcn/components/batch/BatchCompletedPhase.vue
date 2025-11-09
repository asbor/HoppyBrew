<template>
  <div class="space-y-6">
    <!-- Quality Control Tests -->
    <QCTestList :batch-id="batch.id" />

    <!-- Batch Actions -->
    <Card>
      <CardHeader>
        <CardTitle>Batch Management</CardTitle>
        <CardDescription>Archive or manage your completed batch</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="flex gap-4">
          <Button @click="$emit('archive-batch')" variant="outline">
            <Icon name="mdi:archive" class="mr-2 h-4 w-4" />
            Archive Batch
          </Button>
        </div>
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
  'archive-batch': []
  'update-batch': [data: any]
}>()
</script>