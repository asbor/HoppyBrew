<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <CardTitle>Conditioning Phase</CardTitle>
        <CardDescription>Cold conditioning and clarification</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Conditioning phase component - placeholder for now</p>
        <Button class="mt-4" @click="$emit('package-batch')">
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

defineProps<{ batch: any }>()
defineEmits<{
  'package-batch': []
  'update-batch': [data: any]
}>()
</script>