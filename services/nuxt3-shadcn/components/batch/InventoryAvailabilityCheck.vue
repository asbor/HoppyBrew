<template>
  <Card v-if="availability.length > 0" class="mt-4">
    <CardHeader>
      <CardTitle class="flex items-center gap-2">
        <Icon name="mdi:package-variant" class="h-5 w-5" />
        Inventory Availability
      </CardTitle>
      <CardDescription>
        Check ingredient stock levels before creating the batch
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div v-if="loading" class="flex items-center justify-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-600"></div>
      </div>
      
      <div v-else-if="error" class="text-sm text-red-600">
        {{ error }}
      </div>
      
      <div v-else class="space-y-2">
        <div 
          v-for="item in availability" 
          :key="`${item.inventory_item_type}-${item.inventory_item_id}`"
          class="flex items-center justify-between p-3 rounded-lg border"
          :class="{
            'bg-red-50 border-red-200': item.warning_level === 'out_of_stock',
            'bg-yellow-50 border-yellow-200': item.warning_level === 'low_stock',
            'bg-green-50 border-green-200': item.is_available && !item.warning_level
          }"
        >
          <div class="flex items-center gap-3">
            <Icon 
              :name="getItemIcon(item.inventory_item_type)" 
              class="h-5 w-5"
              :class="{
                'text-red-600': item.warning_level === 'out_of_stock',
                'text-yellow-600': item.warning_level === 'low_stock',
                'text-green-600': item.is_available && !item.warning_level
              }"
            />
            <div>
              <p class="font-medium">{{ item.name }}</p>
              <p class="text-sm text-muted-foreground">
                Required: {{ item.required_quantity }} {{ item.unit }} • 
                Available: {{ item.available_quantity }} {{ item.unit }}
              </p>
            </div>
          </div>
          
          <Badge 
            :variant="getWarningVariant(item.warning_level)"
            class="ml-2"
          >
            {{ getWarningLabel(item.warning_level, item.is_available) }}
          </Badge>
        </div>
      </div>
      
      <div v-if="hasOutOfStock" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-800 font-medium">
          ⚠️ Some ingredients are out of stock. You may need to adjust the recipe or restock inventory.
        </p>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface InventoryAvailability {
  inventory_item_id: number
  inventory_item_type: string
  name: string
  available_quantity: number
  required_quantity: number
  unit: string
  is_available: boolean
  warning_level?: 'low_stock' | 'out_of_stock' | null
}

const props = defineProps<{
  recipeId: string | number
}>()

const { checkInventoryAvailability } = useInventory()

const availability = ref<InventoryAvailability[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const hasOutOfStock = computed(() => {
  return availability.value.some(item => item.warning_level === 'out_of_stock')
})

async function checkAvailability() {
  if (!props.recipeId) return
  
  loading.value = true
  error.value = null
  
  const response = await checkInventoryAvailability(props.recipeId.toString())
  
  if (response.error.value) {
    error.value = response.error.value
  } else {
    availability.value = response.data.value || []
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

function getWarningVariant(warningLevel?: string | null): string {
  if (warningLevel === 'out_of_stock') return 'destructive'
  if (warningLevel === 'low_stock') return 'warning'
  return 'success'
}

function getWarningLabel(warningLevel?: string | null, isAvailable?: boolean): string {
  if (warningLevel === 'out_of_stock') return 'Out of Stock'
  if (warningLevel === 'low_stock') return 'Low Stock'
  if (isAvailable) return 'In Stock'
  return 'Unknown'
}

// Watch for recipe changes
watch(() => props.recipeId, () => {
  checkAvailability()
}, { immediate: true })
</script>
