<template>
  <div class="space-y-6">
    <!-- Packaging Details Card -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Packaging Details</CardTitle>
            <CardDescription>Your beer has been packaged</CardDescription>
          </div>
          <Button @click="loadPackagingDetails" variant="outline" size="sm">
            <Icon name="mdi:refresh" class="mr-2 h-4 w-4" />
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-8">
          <Icon name="mdi:alert-circle" class="h-12 w-12 text-muted-foreground mx-auto mb-2" />
          <p class="text-muted-foreground">{{ error }}</p>
        </div>

        <!-- Packaging Details -->
        <div v-else-if="packagingDetails" class="space-y-6">
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">Method</p>
              <div class="flex items-center gap-2">
                <Icon
                  :name="packagingDetails.method === 'bottle' ? 'mdi:bottle-wine' : 'mdi:keg'"
                  class="h-5 w-5 text-primary"
                />
                <p class="font-medium capitalize">{{ packagingDetails.method }}</p>
              </div>
            </div>

            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">Packaging Date</p>
              <p class="font-medium">{{ formatDate(packagingDetails.date) }}</p>
            </div>

            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">Carbonation Method</p>
              <p class="font-medium capitalize">{{ packagingDetails.carbonation_method || 'N/A' }}</p>
            </div>

            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">CO2 Volumes</p>
              <p class="font-medium">{{ packagingDetails.volumes || 'N/A' }}</p>
            </div>

            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">Container Count</p>
              <p class="font-medium">
                {{ packagingDetails.container_count }} {{ packagingDetails.method === 'bottle' ? 'bottles' : 'kegs' }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">Container Size</p>
              <p class="font-medium">{{ packagingDetails.container_size }}L</p>
            </div>

            <div class="space-y-1">
              <p class="text-sm text-muted-foreground">Total Volume</p>
              <p class="font-medium">
                {{ (packagingDetails.container_count * packagingDetails.container_size).toFixed(1) }}L
              </p>
            </div>
          </div>

          <!-- Priming Sugar Details (for bottles) -->
          <template v-if="packagingDetails.method === 'bottle' && packagingDetails.priming_sugar_amount">
            <Separator />
            <div>
              <h4 class="font-medium mb-3">Priming Sugar Details</h4>
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1">
                  <p class="text-sm text-muted-foreground">Sugar Type</p>
                  <p class="font-medium capitalize">{{ packagingDetails.priming_sugar_type }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-sm text-muted-foreground">Amount</p>
                  <p class="font-medium">{{ packagingDetails.priming_sugar_amount }}g</p>
                </div>
              </div>
            </div>
          </template>

          <!-- Kegging Details (for kegs) -->
          <template v-if="packagingDetails.method === 'keg' && packagingDetails.carbonation_psi">
            <Separator />
            <div>
              <h4 class="font-medium mb-3">Carbonation Settings</h4>
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1">
                  <p class="text-sm text-muted-foreground">Temperature</p>
                  <p class="font-medium">{{ packagingDetails.carbonation_temp }}°F</p>
                </div>
                <div class="space-y-1">
                  <p class="text-sm text-muted-foreground">Pressure</p>
                  <p class="font-medium">{{ packagingDetails.carbonation_psi }} PSI</p>
                </div>
              </div>
            </div>
          </template>

          <!-- Notes -->
          <template v-if="packagingDetails.notes">
            <Separator />
            <div>
              <h4 class="font-medium mb-2">Notes</h4>
              <p class="text-sm text-muted-foreground">{{ packagingDetails.notes }}</p>
            </div>
          </template>

          <Separator />

          <div class="flex gap-2">
            <Button @click="$emit('complete-batch')" class="flex-1">
              <Icon name="mdi:check-circle" class="mr-2 h-4 w-4" />
              Mark as Complete
            </Button>
            <Button @click="editPackaging" variant="outline">
              <Icon name="mdi:pencil" class="mr-2 h-4 w-4" />
              Edit
            </Button>
          </div>
        </div>

        <!-- No Packaging Details -->
        <div v-else class="text-center py-8">
          <Icon name="mdi:package-variant" class="h-12 w-12 text-muted-foreground mx-auto mb-2" />
          <p class="text-muted-foreground mb-4">No packaging details found</p>
          <Button @click="showPackagingWizard = true" variant="outline">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Add Packaging Details
          </Button>
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
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Icon } from '#components'
import PackagingWizard from '@/components/PackagingWizard.vue'

const props = defineProps<{ batch: any }>()
const emit = defineEmits<{
  'complete-batch': []
  'update-batch': [data: any]
}>()

const packagingDetails = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const showPackagingWizard = ref(false)

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadPackagingDetails = async () => {
  loading.value = true
  error.value = null
  try {
    packagingDetails.value = await $fetch(`/packaging/${props.batch.id}`)
  } catch (err: any) {
    if (err.status === 404) {
      error.value = 'Packaging details not found. Please add packaging information.'
    } else {
      error.value = 'Failed to load packaging details'
    }
    console.error('Error loading packaging details:', err)
  } finally {
    loading.value = false
  }
}

const editPackaging = () => {
  // TODO: Implement edit functionality - could reuse the wizard or create a separate edit dialog
  showPackagingWizard.value = true
}

const handlePackagingSuccess = () => {
  loadPackagingDetails()
  emit('update-batch', { refresh: true })
}

// Load packaging details on mount
onMounted(() => {
  loadPackagingDetails()
})
</script>
</script>