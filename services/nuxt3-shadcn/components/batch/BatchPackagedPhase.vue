<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <CardTitle>Packaged Phase</CardTitle>
        <CardDescription>Beer has been packaged and is carbonating</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Packaged phase component - placeholder for now</p>
        <Button @click="$emit('complete-batch')" class="mt-4">
          <Icon name="mdi:check-circle" class="mr-2 h-4 w-4" />
          Mark Complete
        </Button>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '#components'

defineProps<{ batch: any; readonly?: boolean }>()
defineEmits<{
  'complete-batch': []
  'update-batch': [data: any]
}>()
</script>