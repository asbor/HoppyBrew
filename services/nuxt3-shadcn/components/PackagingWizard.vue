<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-4xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Package Batch: {{ batchName }}</DialogTitle>
        <DialogDescription>
          Complete the packaging process for your batch
        </DialogDescription>
      </DialogHeader>

      <!-- Wizard Steps -->
      <div class="flex items-center justify-between mb-6">
        <div
          v-for="(step, index) in steps"
          :key="step.id"
          class="flex items-center"
          :class="{ 'flex-1': index < steps.length - 1 }"
        >
          <div class="flex items-center gap-2">
            <div
              class="flex items-center justify-center w-8 h-8 rounded-full border-2"
              :class="
                currentStep >= index
                  ? 'bg-primary text-primary-foreground border-primary'
                  : 'bg-muted border-muted-foreground/30'
              "
            >
              <span v-if="currentStep > index">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="text-sm font-medium hidden md:inline">{{ step.label }}</span>
          </div>
          <div
            v-if="index < steps.length - 1"
            class="flex-1 h-0.5 mx-2"
            :class="currentStep > index ? 'bg-primary' : 'bg-muted'"
          />
        </div>
      </div>

      <!-- Step Content -->
      <div class="space-y-6">
        <!-- Step 1: Method Selection -->
        <template v-if="currentStep === 0">
          <div class="space-y-4">
            <Label>Select Packaging Method</Label>
            <RadioGroup v-model="formData.method" class="grid grid-cols-2 gap-4">
              <div>
                <RadioGroupItem value="bottle" id="method-bottle" class="peer sr-only" />
                <Label
                  for="method-bottle"
                  class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer"
                >
                  <Icon name="mdi:bottle-wine" class="mb-3 h-12 w-12" />
                  <span class="text-lg font-medium">Bottles</span>
                  <span class="text-sm text-muted-foreground text-center mt-1">
                    Package beer in bottles with priming sugar
                  </span>
                </Label>
              </div>
              <div>
                <RadioGroupItem value="keg" id="method-keg" class="peer sr-only" />
                <Label
                  for="method-keg"
                  class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer"
                >
                  <Icon name="mdi:keg" class="mb-3 h-12 w-12" />
                  <span class="text-lg font-medium">Keg</span>
                  <span class="text-sm text-muted-foreground text-center mt-1">
                    Package beer in keg with forced carbonation
                  </span>
                </Label>
              </div>
            </RadioGroup>
          </div>
        </template>

        <!-- Step 2: Carbonation Settings -->
        <template v-else-if="currentStep === 1">
          <div class="space-y-4">
            <div>
              <Label>Carbonation Method</Label>
              <Select v-model="formData.carbonation_method">
                <SelectTrigger>
                  <SelectValue placeholder="Select carbonation method" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="priming" v-if="formData.method === 'bottle'">
                    Priming Sugar (Bottle Conditioning)
                  </SelectItem>
                  <SelectItem value="forced" v-if="formData.method === 'keg'">
                    Forced Carbonation (CO2)
                  </SelectItem>
                  <SelectItem value="natural">Natural Carbonation</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label for="volumes">Target CO2 Volumes</Label>
              <Input
                id="volumes"
                v-model.number="formData.volumes"
                type="number"
                step="0.1"
                min="0"
                max="5"
                placeholder="2.5"
              />
              <p class="text-sm text-muted-foreground mt-1">
                Typical ranges: Lagers 2.5-2.8, Ales 2.0-2.5, Stouts 1.8-2.3
              </p>
            </div>

            <!-- Priming Sugar Calculator (for bottles) -->
            <template v-if="formData.method === 'bottle' && formData.carbonation_method === 'priming'">
              <Separator />
              <h4 class="font-medium">Priming Sugar Calculator</h4>
              
              <div>
                <Label for="sugar_type">Sugar Type</Label>
                <Select v-model="formData.priming_sugar_type">
                  <SelectTrigger>
                    <SelectValue placeholder="Select sugar type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="corn">Corn Sugar (Dextrose)</SelectItem>
                    <SelectItem value="table">Table Sugar (Sucrose)</SelectItem>
                    <SelectItem value="dme">Dry Malt Extract</SelectItem>
                    <SelectItem value="honey">Honey</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button @click="calculatePrimingSugar" variant="outline" class="w-full">
                <Icon name="mdi:calculator" class="mr-2 h-4 w-4" />
                Calculate Priming Sugar
              </Button>

              <div v-if="calculatedSugar" class="p-4 bg-muted rounded-lg">
                <p class="font-medium">Required Priming Sugar:</p>
                <p class="text-2xl font-bold text-primary">{{ calculatedSugar.grams.toFixed(1) }}g</p>
                <p class="text-sm text-muted-foreground">{{ calculatedSugar.oz.toFixed(2) }} oz</p>
              </div>

              <div>
                <Label for="sugar_amount">Priming Sugar Amount (grams)</Label>
                <Input
                  id="sugar_amount"
                  v-model.number="formData.priming_sugar_amount"
                  type="number"
                  step="1"
                  min="0"
                  placeholder="150"
                />
              </div>
            </template>

            <!-- Kegging PSI Calculator (for kegs) -->
            <template v-if="formData.method === 'keg' && formData.carbonation_method === 'forced'">
              <Separator />
              <h4 class="font-medium">Carbonation Pressure Calculator</h4>
              
              <div>
                <Label for="carb_temp">Serving Temperature (°F)</Label>
                <Input
                  id="carb_temp"
                  v-model.number="formData.carbonation_temp"
                  type="number"
                  step="1"
                  min="32"
                  max="70"
                  placeholder="38"
                />
              </div>

              <Button @click="calculateCarbonationPSI" variant="outline" class="w-full">
                <Icon name="mdi:calculator" class="mr-2 h-4 w-4" />
                Calculate Carbonation PSI
              </Button>

              <div v-if="calculatedPSI" class="p-4 bg-muted rounded-lg">
                <p class="font-medium">Required Pressure:</p>
                <p class="text-2xl font-bold text-primary">{{ calculatedPSI.psi.toFixed(1) }} PSI</p>
                <p class="text-sm text-muted-foreground">{{ calculatedPSI.bar.toFixed(2) }} bar</p>
              </div>

              <div>
                <Label for="carb_psi">Carbonation Pressure (PSI)</Label>
                <Input
                  id="carb_psi"
                  v-model.number="formData.carbonation_psi"
                  type="number"
                  step="0.1"
                  min="0"
                  placeholder="12.5"
                />
              </div>
            </template>
          </div>
        </template>

        <!-- Step 3: Container Details -->
        <template v-else-if="currentStep === 2">
          <div class="space-y-4">
            <div>
              <Label for="container_count">Number of {{ formData.method === 'bottle' ? 'Bottles' : 'Kegs' }}</Label>
              <Input
                id="container_count"
                v-model.number="formData.container_count"
                type="number"
                step="1"
                min="0"
                placeholder="48"
              />
            </div>

            <div>
              <Label for="container_size">Container Size (Liters)</Label>
              <Input
                id="container_size"
                v-model.number="formData.container_size"
                type="number"
                step="0.1"
                min="0"
                placeholder="0.5"
              />
              <p class="text-sm text-muted-foreground mt-1">
                {{ formData.method === 'bottle' ? 'Common sizes: 0.33L, 0.5L, 0.75L' : 'Common sizes: 5L, 19L, 50L' }}
              </p>
            </div>

            <div>
              <Label for="packaging_date">Packaging Date</Label>
              <Input
                id="packaging_date"
                v-model="formData.date"
                type="datetime-local"
              />
            </div>

            <div>
              <Label for="notes">Notes</Label>
              <Textarea
                id="notes"
                v-model="formData.notes"
                placeholder="Add any notes about the packaging process..."
                rows="4"
              />
            </div>
          </div>
        </template>

        <!-- Step 4: Review and Confirm -->
        <template v-else-if="currentStep === 3">
          <div class="space-y-4">
            <h3 class="font-semibold text-lg">Review Packaging Details</h3>
            
            <div class="grid grid-cols-2 gap-4 p-4 bg-muted rounded-lg">
              <div>
                <p class="text-sm text-muted-foreground">Method</p>
                <p class="font-medium capitalize">{{ formData.method }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">Carbonation Method</p>
                <p class="font-medium capitalize">{{ formData.carbonation_method }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">CO2 Volumes</p>
                <p class="font-medium">{{ formData.volumes }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">Container Count</p>
                <p class="font-medium">{{ formData.container_count }} {{ formData.method === 'bottle' ? 'bottles' : 'kegs' }}</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">Container Size</p>
                <p class="font-medium">{{ formData.container_size }}L</p>
              </div>
              <div>
                <p class="text-sm text-muted-foreground">Total Volume</p>
                <p class="font-medium">{{ (formData.container_count * formData.container_size).toFixed(1) }}L</p>
              </div>
              
              <template v-if="formData.priming_sugar_amount">
                <div>
                  <p class="text-sm text-muted-foreground">Priming Sugar</p>
                  <p class="font-medium">{{ formData.priming_sugar_amount }}g ({{ formData.priming_sugar_type }})</p>
                </div>
              </template>
              
              <template v-if="formData.carbonation_psi">
                <div>
                  <p class="text-sm text-muted-foreground">Carbonation Pressure</p>
                  <p class="font-medium">{{ formData.carbonation_psi }} PSI @ {{ formData.carbonation_temp }}°F</p>
                </div>
              </template>
            </div>

            <div v-if="formData.notes" class="p-4 bg-muted rounded-lg">
              <p class="text-sm text-muted-foreground mb-1">Notes</p>
              <p class="text-sm">{{ formData.notes }}</p>
            </div>
          </div>
        </template>
      </div>

      <!-- Footer Buttons -->
      <DialogFooter class="flex justify-between">
        <Button
          v-if="currentStep > 0"
          @click="previousStep"
          variant="outline"
        >
          <Icon name="mdi:arrow-left" class="mr-2 h-4 w-4" />
          Back
        </Button>
        <div class="flex gap-2 ml-auto">
          <Button @click="closeDialog" variant="ghost">Cancel</Button>
          <Button
            v-if="currentStep < steps.length - 1"
            @click="nextStep"
            :disabled="!canProceed"
          >
            Next
            <Icon name="mdi:arrow-right" class="ml-2 h-4 w-4" />
          </Button>
          <Button
            v-else
            @click="submitPackaging"
            :disabled="isSubmitting"
          >
            <Icon name="mdi:check" class="mr-2 h-4 w-4" />
            {{ isSubmitting ? 'Saving...' : 'Complete Packaging' }}
          </Button>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Icon } from '#components'

const props = defineProps<{
  open: boolean
  batchId: number
  batchName: string
  batchSize: number
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'success': []
}>()

const isOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value)
})

const currentStep = ref(0)
const isSubmitting = ref(false)
const calculatedSugar = ref<{ grams: number; oz: number } | null>(null)
const calculatedPSI = ref<{ psi: number; bar: number } | null>(null)

const steps = [
  { id: 'method', label: 'Method' },
  { id: 'carbonation', label: 'Carbonation' },
  { id: 'details', label: 'Details' },
  { id: 'review', label: 'Review' }
]

const formData = ref({
  batch_id: props.batchId,
  method: 'bottle',
  date: new Date().toISOString().slice(0, 16),
  carbonation_method: 'priming',
  volumes: 2.5,
  container_count: 48,
  container_size: 0.5,
  priming_sugar_type: 'corn',
  priming_sugar_amount: null as number | null,
  carbonation_temp: 38,
  carbonation_psi: null as number | null,
  notes: ''
})

// Update carbonation method when packaging method changes
watch(() => formData.value.method, (newMethod) => {
  if (newMethod === 'bottle') {
    formData.value.carbonation_method = 'priming'
  } else {
    formData.value.carbonation_method = 'forced'
  }
})

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return formData.value.method !== ''
    case 1:
      return formData.value.carbonation_method !== '' && formData.value.volumes > 0
    case 2:
      return formData.value.container_count > 0 && formData.value.container_size > 0
    default:
      return true
  }
})

const nextStep = () => {
  if (currentStep.value < steps.length - 1 && canProceed.value) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const closeDialog = () => {
  isOpen.value = false
  currentStep.value = 0
  calculatedSugar.value = null
  calculatedPSI.value = null
}

const calculatePrimingSugar = async () => {
  try {
    const response = await $fetch('/calculators/priming-sugar', {
      method: 'POST',
      body: {
        volume_gal: props.batchSize / 3.78541, // Convert liters to gallons
        carbonation_level: formData.value.volumes,
        sugar_type: formData.value.priming_sugar_type
      }
    })
    calculatedSugar.value = response as { grams: number; oz: number }
    formData.value.priming_sugar_amount = Math.round(calculatedSugar.value.grams)
  } catch (error) {
    console.error('Error calculating priming sugar:', error)
  }
}

const calculateCarbonationPSI = async () => {
  try {
    const response = await $fetch('/calculators/carbonation', {
      method: 'POST',
      body: {
        temp_f: formData.value.carbonation_temp,
        co2_volumes: formData.value.volumes
      }
    })
    calculatedPSI.value = response as { psi: number; bar: number }
    formData.value.carbonation_psi = parseFloat(calculatedPSI.value.psi.toFixed(1))
  } catch (error) {
    console.error('Error calculating carbonation PSI:', error)
  }
}

const submitPackaging = async () => {
  if (isSubmitting.value) return
  
  isSubmitting.value = true
  try {
    await $fetch('/packaging', {
      method: 'POST',
      body: formData.value
    })
    
    emit('success')
    closeDialog()
  } catch (error) {
    console.error('Error submitting packaging details:', error)
    alert('Failed to save packaging details. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}
</script>
