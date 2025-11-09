<template>
  <div class="space-y-6">
    <Card>
      <CardHeader>
        <CardTitle>Conditioning Phase</CardTitle>
        <CardDescription>Cold conditioning and clarification</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="prose prose-sm max-w-none">
          <p>Your beer is now in the conditioning phase. This is the time for cold conditioning and clarification.</p>
          <ul>
            <li>Monitor the clarity of your beer</li>
            <li>Check for any off-flavors or aromas</li>
            <li>Ensure proper temperature for conditioning (typically 32-40°F / 0-4°C)</li>
          </ul>
        </div>

        <Separator />

        <div class="flex flex-col gap-2">
          <Button @click="showPackagingWizard = true" size="lg" class="w-full">
            <Icon name="mdi:bottle-wine" class="mr-2 h-5 w-5" />
            Package Beer
          </Button>
          <p class="text-sm text-muted-foreground text-center">
            Ready to package your beer? Start the packaging wizard to bottle or keg your batch.
          </p>
        </div>
      </CardContent>
    </Card>

    <!-- Packaging Wizard Dialog -->
    <PackagingWizard
      v-model:open="showPackagingWizard"
      :batch-id="batch.id"
      :batch-name="batch.batch_name"
      :batch-size="batch.batch_size"
      @success="handlePackagingSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Icon } from '#components'
import PackagingWizard from '@/components/PackagingWizard.vue'

const props = defineProps<{ batch: any }>()
const emit = defineEmits<{
  'package-batch': []
  'update-batch': [data: any]
}>()

const showPackagingWizard = ref(false)

const handlePackagingSuccess = () => {
  // Emit package-batch event to update batch status
  emit('package-batch')
  // Optionally refresh batch data
  emit('update-batch', { refresh: true })
}
</script>