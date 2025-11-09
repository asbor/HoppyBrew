<template>
  <div class="space-y-6">
    <!-- Recipe Overview Card -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle class="text-xl">{{ batch.recipe?.name || 'Recipe Name' }}</CardTitle>
            <CardDescription>{{ batch.recipe?.style || 'Beer Style' }}</CardDescription>
          </div>
          <Button variant="outline" @click="editRecipe">
            <Icon name="mdi:pencil" class="mr-2 h-4 w-4" />
            Edit Recipe
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Recipe Stats -->
          <div class="space-y-4">
            <h4 class="font-semibold text-amber-700">Style</h4>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">ABV:</span>
                <span class="font-medium">{{ batch.recipe?.abv || '6.0' }}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">IBU:</span>
                <span class="font-medium">{{ batch.recipe?.ibu || '26' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">OG:</span>
                <span class="font-medium">{{ batch.recipe?.og || '1.064' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">FG:</span>
                <span class="font-medium">{{ batch.recipe?.fg || '1.018' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Color:</span>
                <span class="font-medium">{{ batch.recipe?.srm || '8.7' }} EBC</span>
              </div>
            </div>
          </div>

          <!-- Equipment Profile -->
          <div class="space-y-4">
            <h4 class="font-semibold text-blue-700">Equipment</h4>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Brewster Beacon:</span>
                <span class="font-medium">{{ batch.batch_size }}L</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Boil Time:</span>
                <span class="font-medium">60 min</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Efficiency:</span>
                <span class="font-medium">70%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Brew Volume:</span>
                <span class="font-medium">{{ (batch.batch_size * 1.1).toFixed(1) }}L</span>
              </div>
            </div>
          </div>

          <!-- Water Profile -->
          <div class="space-y-4">
            <h4 class="font-semibold text-cyan-700">Water</h4>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Mash Water:</span>
                <span class="font-medium">{{ waterProfile.mashWater }}L</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Sparge Water:</span>
                <span class="font-medium">{{ waterProfile.spargeWater }}L</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Total Water:</span>
                <span class="font-medium">{{ waterProfile.totalWater }}L</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Mash pH:</span>
                <span class="font-medium">{{ waterProfile.ph }}</span>
              </div>
            </div>
          </div>

          <!-- Batch Info -->
          <div class="space-y-4">
            <h4 class="font-semibold text-green-700">Batch</h4>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Batch #:</span>
                <span class="font-medium">{{ batch.batch_number }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Brewer:</span>
                <span class="font-medium">{{ batch.brewer }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Brew Date:</span>
                <span class="font-medium">{{ formatDate(batch.brew_date) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-muted-foreground">Batch Size:</span>
                <span class="font-medium">{{ batch.batch_size }}L</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Ingredients Overview -->
    <div class="grid md:grid-cols-2 gap-6">
      <!-- Fermentables -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:grain" class="h-5 w-5 text-amber-600" />
            Fermentables ({{ fermentablesWeight }}kg)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <div v-for="fermentable in sampleFermentables" :key="fermentable.name" 
                 class="flex justify-between items-center">
              <div>
                <p class="font-medium">{{ fermentable.amount }}kg {{ fermentable.name }}</p>
                <p class="text-sm text-muted-foreground">{{ fermentable.percentage }}%</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-muted-foreground">{{ fermentable.type }}</p>
                <p class="text-sm font-medium">{{ fermentable.color }} EBC</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Hops -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:flower" class="h-5 w-5 text-green-600" />
            Hops ({{ hopsWeight }}g)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <div v-for="hop in sampleHops" :key="hop.name" 
                 class="flex justify-between items-center">
              <div>
                <p class="font-medium">{{ hop.amount }}g {{ hop.name }}</p>
                <p class="text-sm text-muted-foreground">{{ hop.alpha }}% Alpha</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-muted-foreground">{{ hop.use }}</p>
                <p class="text-sm font-medium">{{ hop.time }} min</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Mash Schedule & Yeast -->
    <div class="grid md:grid-cols-2 gap-6">
      <!-- Mash Schedule -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:thermometer" class="h-5 w-5 text-red-600" />
            Mash Schedule
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <div v-for="step in mashSteps" :key="step.name" 
                 class="flex justify-between items-center p-3 bg-gray-50 rounded">
              <div>
                <p class="font-medium">{{ step.name }}</p>
                <p class="text-sm text-muted-foreground">{{ step.temperature }}°C</p>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium">{{ step.time }} min</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Yeast & Misc -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <Icon name="mdi:bacteria" class="h-5 w-5 text-purple-600" />
            Yeast & Misc
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <!-- Yeast -->
            <div>
              <h5 class="font-medium mb-2">Yeast</h5>
              <div v-for="yeast in sampleYeasts" :key="yeast.name" 
                   class="flex justify-between items-center">
                <div>
                  <p class="font-medium">{{ yeast.amount }} {{ yeast.name }}</p>
                  <p class="text-sm text-muted-foreground">{{ yeast.type }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium">{{ yeast.attenuation }}%</p>
                </div>
              </div>
            </div>

            <!-- Misc -->
            <div v-if="sampleMiscs.length > 0">
              <h5 class="font-medium mb-2">Additions</h5>
              <div v-for="misc in sampleMiscs" :key="misc.name" 
                   class="flex justify-between items-center">
                <div>
                  <p class="font-medium">{{ misc.amount }}g {{ misc.name }}</p>
                  <p class="text-sm text-muted-foreground">{{ misc.use }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium">{{ misc.time }} min</p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Planning Actions -->
    <Card>
      <CardHeader>
        <CardTitle>Pre-Brew Checklist</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Inventory Check -->
          <div>
            <h4 class="font-semibold mb-3">Inventory Status</h4>
            <div class="space-y-2">
              <div class="flex items-center justify-between p-2 rounded" 
                   :class="getInventoryStatusClass('fermentables')">
                <span class="flex items-center gap-2">
                  <Icon name="mdi:grain" class="h-4 w-4" />
                  Fermentables
                </span>
                <Badge :variant="getInventoryBadgeVariant('fermentables')">
                  {{ getInventoryStatus('fermentables') }}
                </Badge>
              </div>
              <div class="flex items-center justify-between p-2 rounded" 
                   :class="getInventoryStatusClass('hops')">
                <span class="flex items-center gap-2">
                  <Icon name="mdi:flower" class="h-4 w-4" />
                  Hops
                </span>
                <Badge :variant="getInventoryBadgeVariant('hops')">
                  {{ getInventoryStatus('hops') }}
                </Badge>
              </div>
              <div class="flex items-center justify-between p-2 rounded" 
                   :class="getInventoryStatusClass('yeast')">
                <span class="flex items-center gap-2">
                  <Icon name="mdi:bacteria" class="h-4 w-4" />
                  Yeast
                </span>
                <Badge :variant="getInventoryBadgeVariant('yeast')">
                  {{ getInventoryStatus('yeast') }}
                </Badge>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div>
            <h4 class="font-semibold mb-3">Actions</h4>
            <div class="space-y-2">
              <Button @click="printBrewSheet" variant="outline" class="w-full justify-start">
                <Icon name="mdi:printer" class="mr-2 h-4 w-4" />
                Print Brew Sheet
              </Button>
              <Button @click="reserveIngredients" variant="outline" class="w-full justify-start">
                <Icon name="mdi:cart" class="mr-2 h-4 w-4" />
                Reserve Ingredients
              </Button>
              <Button @click="scheduleBrewDay" variant="outline" class="w-full justify-start">
                <Icon name="mdi:calendar" class="mr-2 h-4 w-4" />
                Schedule Brew Day
              </Button>
              <Button @click="$emit('start-brew')" class="w-full justify-start">
                <Icon name="mdi:fire" class="mr-2 h-4 w-4" />
                Start Brew Day
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Batch Notes -->
    <Card>
      <CardHeader>
        <CardTitle>Planning Notes</CardTitle>
      </CardHeader>
      <CardContent>
        <Textarea 
          v-model="batchNotes"
          placeholder="Add any planning notes, modifications, or reminders for brew day..."
          class="min-h-[100px]"
          @blur="updateNotes"
        />
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { Icon } from '#components'

const props = defineProps<{
  batch: any
  readonly?: boolean
}>()

const emit = defineEmits<{
  'start-brew': []
  'update-batch': [data: any]
}>()

const batchNotes = ref(props.batch.notes || '')

// Sample data based on Brewfather screenshots
const sampleFermentables = [
  { name: 'Pale Ale Malt', amount: 1.86, percentage: 42.8, type: 'Grain', color: 5 },
  { name: 'Pilsen Malt', amount: 1.86, percentage: 42.8, type: 'Grain', color: 3 },
  { name: 'Caramel Pils Malt', amount: 0.53, percentage: 12.2, type: 'Grain', color: 5 },
  { name: 'Pale Crystal Malt', amount: 0.1, percentage: 2.3, type: 'Grain', color: 75 }
]

const sampleHops = [
  { name: 'Summit', amount: 9, alpha: 17.0, use: 'Boil', time: 60 },
  { name: 'Saaz', amount: 19.4, alpha: 3.8, use: 'Boil', time: 15 },
  { name: 'Amarillo', amount: 4.7, alpha: 9.2, use: 'Boil', time: 20 },
  { name: 'Amarillo', amount: 4.7, alpha: 9.2, use: 'Aroma', time: 20 },
  { name: 'Amarillo', amount: 19.4, alpha: 9.2, use: 'Dry Hop', time: 7 }
]

const sampleYeasts = [
  { name: 'White Labs WLP041 Pacific Ale', amount: '1 pkg', type: 'California Ale', attenuation: 70.8 }
]

const sampleMiscs = [
  { name: 'Servomyces', amount: 0.2, use: 'Boil', time: 15 },
  { name: 'Whirlfloc', amount: 0.5, use: 'Boil', time: 15 }
]

const mashSteps = [
  { name: 'Mash In', temperature: 65, time: 60 },
  { name: 'Mash Out', temperature: 76, time: 10 }
]

const waterProfile = computed(() => ({
  mashWater: (props.batch.batch_size * 0.7).toFixed(1),
  spargeWater: (props.batch.batch_size * 0.8).toFixed(1),
  totalWater: (props.batch.batch_size * 1.5).toFixed(1),
  ph: '5.71'
}))

const fermentablesWeight = computed(() => {
  return sampleFermentables.reduce((total, f) => total + f.amount, 0).toFixed(2)
})

const hopsWeight = computed(() => {
  return sampleHops.reduce((total, h) => total + h.amount, 0)
})

// Inventory status simulation
const getInventoryStatus = (type: string) => {
  // Simulate inventory checking
  const statuses = ['Available', 'Low Stock', 'Out of Stock']
  return statuses[Math.floor(Math.random() * statuses.length)]
}

const getInventoryStatusClass = (type: string) => {
  const status = getInventoryStatus(type)
  if (status === 'Available') return 'bg-green-50'
  if (status === 'Low Stock') return 'bg-yellow-50'
  return 'bg-red-50'
}

const getInventoryBadgeVariant = (type: string) => {
  const status = getInventoryStatus(type)
  if (status === 'Available') return 'success'
  if (status === 'Low Stock') return 'warning'
  return 'destructive'
}

const formatDate = (date: string | Date) => {
  if (!date) return 'Not set'
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

// Action handlers
const editRecipe = () => {
  // Navigate to recipe editing
  console.log('Edit recipe')
}

const printBrewSheet = () => {
  window.print()
}

const reserveIngredients = () => {
  // Reserve ingredients in inventory
  console.log('Reserve ingredients')
}

const scheduleBrewDay = () => {
  // Open calendar/scheduling
  console.log('Schedule brew day')
}

const updateNotes = () => {
  emit('update-batch', { notes: batchNotes.value })
}
</script>