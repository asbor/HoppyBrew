<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <CardTitle>Completed Batch</CardTitle>
        <CardDescription>Brewing process completed successfully</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Completed phase component - placeholder for now</p>
        <Button variant="outline" class="mt-4" @click="$emit('archive-batch')">
          <Icon name="mdi:archive" class="mr-2 h-4 w-4" />
          Archive Batch
        </Button>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '#components'

defineProps<{ batch: any }>()
defineEmits<{
  'archive-batch': []
  'update-batch': [data: any]
}>()
</script>