<template>
  <div class="space-y-6">
    <!-- Packaging Details Card -->
    <Card v-if="!packagingDetails">
      <CardHeader>
        <CardTitle>Package Your Beer</CardTitle>
        <CardDescription>
          Choose your packaging method and carbonation settings
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- Step 1: Packaging Method -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">Packaging Method</h3>
          <div class="grid grid-cols-2 gap-4">
            <Card 
              :class="[
                'cursor-pointer transition-all hover:shadow-md',
                packagingForm.method === 'bottling' ? 'ring-2 ring-primary' : ''
              ]"
              @click="packagingForm.method = 'bottling'"
            >
              <CardContent class="p-6 text-center">
                <Icon name="mdi:bottle-wine" class="h-12 w-12 mx-auto mb-2 text-amber-600" />
                <h4 class="font-semibold">Bottling</h4>
                <p class="text-sm text-muted-foreground">Package in bottles</p>
              </CardContent>
            </Card>
            
            <Card 
              :class="[
                'cursor-pointer transition-all hover:shadow-md',
                packagingForm.method === 'kegging' ? 'ring-2 ring-primary' : ''
              ]"
              @click="packagingForm.method = 'kegging'"
            >
              <CardContent class="p-6 text-center">
                <Icon name="mdi:keg" class="h-12 w-12 mx-auto mb-2 text-amber-600" />
                <h4 class="font-semibold">Kegging</h4>
                <p class="text-sm text-muted-foreground">Package in kegs</p>
              </CardContent>
            </Card>
          </div>
        </div>

        <!-- Step 2: Carbonation Method -->
        <div v-if="packagingForm.method" class="space-y-4">
          <h3 class="text-lg font-semibold">Carbonation Method</h3>
          <div class="grid grid-cols-3 gap-4">
            <Card 
              v-if="packagingForm.method === 'bottling'"
              :class="[
                'cursor-pointer transition-all hover:shadow-md',
                packagingForm.carbonation_method === 'priming_sugar' ? 'ring-2 ring-primary' : ''
              ]"
              @click="packagingForm.carbonation_method = 'priming_sugar'"
            >
              <CardContent class="p-4 text-center">
                <Icon name="mdi:shaker" class="h-8 w-8 mx-auto mb-2" />
                <h4 class="text-sm font-semibold">Priming Sugar</h4>
              </CardContent>
            </Card>
            
            <Card 
              v-if="packagingForm.method === 'kegging'"
              :class="[
                'cursor-pointer transition-all hover:shadow-md',
                packagingForm.carbonation_method === 'forced' ? 'ring-2 ring-primary' : ''
              ]"
              @click="packagingForm.carbonation_method = 'forced'"
            >
              <CardContent class="p-4 text-center">
                <Icon name="mdi:air-filter" class="h-8 w-8 mx-auto mb-2" />
                <h4 class="text-sm font-semibold">Forced CO2</h4>
              </CardContent>
            </Card>
            
            <Card 
              :class="[
                'cursor-pointer transition-all hover:shadow-md',
                packagingForm.carbonation_method === 'natural' ? 'ring-2 ring-primary' : ''
              ]"
              @click="packagingForm.carbonation_method = 'natural'"
            >
              <CardContent class="p-4 text-center">
                <Icon name="mdi:weather-sunny" class="h-8 w-8 mx-auto mb-2" />
                <h4 class="text-sm font-semibold">Natural</h4>
              </CardContent>
            </Card>
          </div>
        </div>

        <!-- Step 3: Packaging Details Form -->
        <div v-if="packagingForm.carbonation_method" class="space-y-4">
          <h3 class="text-lg font-semibold">Packaging Details</h3>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="text-sm font-medium">Packaging Date</label>
              <Input v-model="packagingForm.packaging_date" type="datetime-local" />
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-medium">Temperature (°F)</label>
              <Input v-model.number="packagingForm.temperature" type="number" placeholder="68" />
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-medium">Target CO₂ Volumes</label>
              <Input v-model.number="packagingForm.volumes_co2" type="number" step="0.1" placeholder="2.4" />
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-medium">
                {{ packagingForm.method === 'bottling' ? 'Number of Bottles' : 'Number of Kegs' }}
              </label>
              <Input v-model.number="packagingForm.container_count" type="number" placeholder="48" />
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-medium">Container Size (L)</label>
              <Input v-model.number="packagingForm.container_size" type="number" step="0.1" 
                :placeholder="packagingForm.method === 'bottling' ? '0.5' : '19'" />
            </div>
          </div>

          <!-- Priming Sugar Calculator (for bottling with priming sugar) -->
          <div v-if="packagingForm.method === 'bottling' && packagingForm.carbonation_method === 'priming_sugar'" 
               class="space-y-4 p-4 bg-muted rounded-lg">
            <h4 class="font-semibold">Priming Sugar Calculator</h4>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <label class="text-sm font-medium">Sugar Type</label>
                <select v-model="packagingForm.priming_sugar_type" class="w-full p-2 border rounded">
                  <option value="table">Table Sugar</option>
                  <option value="corn">Corn Sugar</option>
                  <option value="dme">Dry Malt Extract</option>
                  <option value="honey">Honey</option>
                </select>
              </div>
              <div class="space-y-2">
                <label class="text-sm font-medium">Calculated Amount</label>
                <div class="p-2 bg-background rounded border">
                  <p v-if="calculatedPrimingSugar" class="font-semibold">
                    {{ calculatedPrimingSugar.grams.toFixed(1) }}g 
                    ({{ calculatedPrimingSugar.oz.toFixed(2) }}oz)
                  </p>
                  <p v-else class="text-muted-foreground">Enter details above</p>
                </div>
              </div>
            </div>
            <Button @click="calculatePrimingSugar" variant="outline" size="sm">
              <Icon name="mdi:calculator" class="mr-2 h-4 w-4" />
              Calculate Priming Sugar
            </Button>
          </div>

          <!-- Carbonation PSI Calculator (for kegging with forced carbonation) -->
          <div v-if="packagingForm.method === 'kegging' && packagingForm.carbonation_method === 'forced'" 
               class="space-y-4 p-4 bg-muted rounded-lg">
            <h4 class="font-semibold">Carbonation Pressure Calculator</h4>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <label class="text-sm font-medium">Calculated PSI</label>
                <div class="p-2 bg-background rounded border">
                  <p v-if="calculatedPSI" class="font-semibold">
                    {{ calculatedPSI.psi.toFixed(1) }} PSI
                    ({{ calculatedPSI.bar.toFixed(2) }} bar)
                  </p>
                  <p v-else class="text-muted-foreground">Enter details above</p>
                </div>
              </div>
            </div>
            <Button @click="calculateCarbonationPSI" variant="outline" size="sm">
              <Icon name="mdi:calculator" class="mr-2 h-4 w-4" />
              Calculate Pressure
            </Button>
          </div>

          <!-- Notes -->
          <div class="space-y-2">
            <label class="text-sm font-medium">Notes (Optional)</label>
            <Textarea v-model="packagingForm.notes" 
              placeholder="Add any notes about packaging process..." 
              rows="3" />
          </div>
        </div>
      </CardContent>
      
      <CardFooter class="flex justify-between">
        <Button @click="$emit('update-batch', {})" variant="outline">
          Cancel
        </Button>
        <Button @click="savePackagingDetails" :disabled="!isFormValid">
          <Icon name="mdi:check" class="mr-2 h-4 w-4" />
          Save Packaging Details
        </Button>
      </CardFooter>
    </Card>

    <!-- Packaging Complete View -->
    <Card v-else>
      <CardHeader>
        <CardTitle>Packaging Complete</CardTitle>
        <CardDescription>
          Your beer has been packaged and is ready for carbonation
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-muted-foreground">Method</p>
            <p class="font-semibold capitalize">{{ packagingDetails.method }}</p>
          </div>
          <div>
            <p class="text-sm text-muted-foreground">Carbonation</p>
            <p class="font-semibold capitalize">{{ packagingDetails.carbonation_method.replace('_', ' ') }}</p>
          </div>
          <div>
            <p class="text-sm text-muted-foreground">Date Packaged</p>
            <p class="font-semibold">{{ formatDate(packagingDetails.packaging_date) }}</p>
          </div>
          <div>
            <p class="text-sm text-muted-foreground">CO₂ Volumes</p>
            <p class="font-semibold">{{ packagingDetails.volumes_co2 }} vol</p>
          </div>
          <div>
            <p class="text-sm text-muted-foreground">Containers</p>
            <p class="font-semibold">
              {{ packagingDetails.container_count }} × {{ packagingDetails.container_size }}L
            </p>
          </div>
          <div v-if="packagingDetails.priming_sugar_amount">
            <p class="text-sm text-muted-foreground">Priming Sugar</p>
            <p class="font-semibold">{{ packagingDetails.priming_sugar_amount.toFixed(1) }}g</p>
          </div>
          <div v-if="packagingDetails.pressure_psi">
            <p class="text-sm text-muted-foreground">Serving Pressure</p>
            <p class="font-semibold">{{ packagingDetails.pressure_psi.toFixed(1) }} PSI</p>
          </div>
        </div>
        
        <div v-if="packagingDetails.notes" class="pt-4 border-t">
          <p class="text-sm text-muted-foreground">Notes</p>
          <p>{{ packagingDetails.notes }}</p>
        </div>
      </CardContent>
      <CardFooter class="flex justify-between">
        <Button @click="editPackaging" variant="outline">
          <Icon name="mdi:pencil" class="mr-2 h-4 w-4" />
          Edit Details
        </Button>
        <Button @click="$emit('complete-batch')">
          <Icon name="mdi:check-circle" class="mr-2 h-4 w-4" />
          Mark Complete
        </Button>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Icon } from '#components'

const props = defineProps<{ batch: any }>()
const emit = defineEmits<{
  'complete-batch': []
  'update-batch': [data: any]
}>()

const packagingDetails = ref<any>(null)
const calculatedPrimingSugar = ref<any>(null)
const calculatedPSI = ref<any>(null)

const packagingForm = reactive({
  packaging_date: new Date().toISOString().slice(0, 16),
  method: '',
  carbonation_method: '',
  volumes_co2: 2.4,
  container_count: null as number | null,
  container_size: null as number | null,
  priming_sugar_amount: null as number | null,
  priming_sugar_type: 'table',
  pressure_psi: null as number | null,
  temperature: 68,
  notes: '',
})

const isFormValid = computed(() => {
  return packagingForm.method && 
         packagingForm.carbonation_method && 
         packagingForm.packaging_date &&
         packagingForm.volumes_co2 &&
         packagingForm.container_count &&
         packagingForm.container_size
})

const fetchPackagingDetails = async () => {
  try {
    const response = await fetch(`/api/batches/${props.batch.id}/packaging`)
    if (response.ok) {
      packagingDetails.value = await response.json()
    }
  } catch (error) {
    // Packaging details don't exist yet, which is fine
  }
}

const calculatePrimingSugar = async () => {
  if (!packagingForm.container_count || !packagingForm.container_size || !packagingForm.volumes_co2) {
    return
  }
  
  const volumeGal = (packagingForm.container_count * packagingForm.container_size) / 3.78541
  
  try {
    const response = await fetch(
      `/api/packaging/calculate-priming-sugar?` +
      `volume_gal=${volumeGal}&` +
      `carbonation_level=${packagingForm.volumes_co2}&` +
      `sugar_type=${packagingForm.priming_sugar_type}`,
      { method: 'POST' }
    )
    
    if (response.ok) {
      calculatedPrimingSugar.value = await response.json()
      packagingForm.priming_sugar_amount = calculatedPrimingSugar.value.grams
    }
  } catch (error) {
    console.error('Error calculating priming sugar:', error)
  }
}

const calculateCarbonationPSI = async () => {
  if (!packagingForm.temperature || !packagingForm.volumes_co2) {
    return
  }
  
  try {
    const response = await fetch(
      `/api/packaging/calculate-carbonation-psi?` +
      `temp_f=${packagingForm.temperature}&` +
      `co2_volumes=${packagingForm.volumes_co2}`,
      { method: 'POST' }
    )
    
    if (response.ok) {
      calculatedPSI.value = await response.json()
      packagingForm.pressure_psi = calculatedPSI.value.psi
    }
  } catch (error) {
    console.error('Error calculating carbonation PSI:', error)
  }
}

const savePackagingDetails = async () => {
  try {
    const response = await fetch(`/api/batches/${props.batch.id}/packaging`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(packagingForm)
    })
    
    if (response.ok) {
      packagingDetails.value = await response.json()
      emit('update-batch', {})
    }
  } catch (error) {
    console.error('Error saving packaging details:', error)
  }
}

const editPackaging = () => {
  packagingDetails.value = null
  // Pre-populate form with existing data
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

onMounted(() => {
  fetchPackagingDetails()
})
</script>
