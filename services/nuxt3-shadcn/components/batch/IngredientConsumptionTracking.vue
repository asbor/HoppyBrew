<template>
  <Card>
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <Icon name="mdi:chart-timeline-variant" class="h-5 w-5" />
        Ingredient Consumption Tracking
      </CardTitle>
      <CardDescription>
        View ingredients consumed for this batch and transaction history
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div v-if="loading" class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-amber-600"></div>
      </div>
      
      <div v-else-if="error" class="text-center py-8">
        <Icon name="mdi:alert-circle" class="mx-auto h-12 w-12 text-red-500 mb-2" />
        <p class="text-sm text-red-600">{{ error }}</p>
      </div>
      
      <div v-else-if="trackingData">
        <!-- Consumed Ingredients -->
        <div v-if="trackingData.consumed_ingredients && trackingData.consumed_ingredients.length > 0" class="mb-6">
          <h3 class="text-sm font-semibold mb-3 flex items-center gap-2">
            <Icon name="mdi:package-variant-closed" class="h-4 w-4" />
            Consumed Ingredients
          </h3>
          <div class="space-y-2">
            <div 
              v-for="ingredient in trackingData.consumed_ingredients" 
              :key="ingredient.id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center gap-3">
                <Icon 
                  :name="getItemIcon(ingredient.inventory_item_type)" 
                  class="h-5 w-5 text-gray-600"
                />
                <div>
                  <p class="text-sm font-medium capitalize">{{ ingredient.inventory_item_type }}</p>
                  <p class="text-xs text-muted-foreground">ID: {{ ingredient.inventory_item_id }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold">{{ ingredient.quantity_used }} {{ ingredient.unit }}</p>
                <p class="text-xs text-muted-foreground">{{ formatDate(ingredient.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="mb-6 p-4 bg-gray-50 rounded-lg text-center">
          <Icon name="mdi:information-outline" class="mx-auto h-8 w-8 text-gray-400 mb-2" />
          <p class="text-sm text-muted-foreground">No ingredients consumed yet for this batch</p>
        </div>

        <!-- Transaction History -->
        <div v-if="trackingData.transactions && trackingData.transactions.length > 0">
          <h3 class="text-sm font-semibold mb-3 flex items-center gap-2">
            <Icon name="mdi:history" class="h-4 w-4" />
            Transaction History
          </h3>
          <div class="space-y-2">
            <div 
              v-for="transaction in trackingData.transactions" 
              :key="transaction.id"
              class="flex items-start justify-between p-3 border rounded-lg"
            >
              <div class="flex items-start gap-3 flex-1">
                <Icon 
                  :name="getTransactionIcon(transaction.transaction_type)" 
                  class="h-5 w-5 mt-0.5"
                  :class="getTransactionColor(transaction.transaction_type)"
                />
                <div class="flex-1">
                  <p class="text-sm font-medium capitalize">{{ transaction.transaction_type }}</p>
                  <p class="text-xs text-muted-foreground">
                    {{ transaction.inventory_item_type }} • 
                    {{ Math.abs(transaction.quantity_change) }} {{ transaction.unit }}
                  </p>
                  <p v-if="transaction.notes" class="text-xs text-muted-foreground mt-1">
                    {{ transaction.notes }}
                  </p>
                </div>
              </div>
              <div class="text-right text-xs text-muted-foreground ml-3">
                <p>{{ formatDate(transaction.created_at) }}</p>
                <p class="mt-1">
                  {{ transaction.quantity_before }} → {{ transaction.quantity_after }} {{ transaction.unit }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const props = defineProps<{
  batchId: string | number
}>()

const { getIngredientTracking } = useInventory()

const trackingData = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchTracking() {
  if (!props.batchId) return
  
  loading.value = true
  error.value = null
  
  const response = await getIngredientTracking(props.batchId.toString())
  
  if (response.error.value) {
    error.value = response.error.value
  } else {
    trackingData.value = response.data.value
  }
  
  loading.value = false
}

function getItemIcon(itemType: string): string {
  const icons: Record<string, string> = {
    'hop': 'mdi:leaf',
    'fermentable': 'mdi:barley',
    'yeast': 'mdi:bacteria',
    'misc': 'mdi:flask'
  }
  return icons[itemType] || 'mdi:package'
}

function getTransactionIcon(type: string): string {
  const icons: Record<string, string> = {
    'consumption': 'mdi:minus-circle',
    'addition': 'mdi:plus-circle',
    'adjustment': 'mdi:pencil-circle'
  }
  return icons[type] || 'mdi:circle'
}

function getTransactionColor(type: string): string {
  const colors: Record<string, string> = {
    'consumption': 'text-red-600',
    'addition': 'text-green-600',
    'adjustment': 'text-blue-600'
  }
  return colors[type] || 'text-gray-600'
}

function formatDate(dateString: string): string {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Watch for batch ID changes
watch(() => props.batchId, () => {
  fetchTracking()
}, { immediate: true })
</script>
