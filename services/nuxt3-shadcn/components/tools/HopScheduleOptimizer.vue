<template>
  <Card>
    <CardHeader>
      <CardTitle>Hop Schedule Optimizer</CardTitle>
      <CardDescription>
        Design your hop schedule with IBU contribution visualization and substitution suggestions
      </CardDescription>
    </CardHeader>
    <CardContent class="space-y-6">
      <!-- Batch Parameters -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <Label for="batch-size">Batch Size (gallons)</Label>
          <Input
            id="batch-size"
            v-model.number="batchSize"
            type="number"
            step="0.1"
            min="0"
          />
        </div>
        <div class="space-y-2">
          <Label for="boil-gravity">Boil Gravity</Label>
          <Input
            id="boil-gravity"
            v-model.number="boilGravity"
            type="number"
            step="0.001"
            min="1.000"
          />
        </div>
      </div>

      <!-- Hop Additions -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold">Hop Additions</h3>
          <Button size="sm" @click="addHop">
            <Plus class="h-4 w-4 mr-2" />
            Add Hop
          </Button>
        </div>

        <div v-if="hops.length === 0" class="text-center py-8 text-gray-500">
          No hop additions yet. Click "Add Hop" to get started.
        </div>

        <div v-for="(hop, index) in hops" :key="index" class="p-4 border rounded-lg space-y-3">
          <div class="flex items-center justify-between">
            <span class="font-medium">Hop Addition {{ index + 1 }}</span>
            <Button variant="ghost" size="sm" @click="removeHop(index)">
              <Trash2 class="h-4 w-4" />
            </Button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div class="space-y-2">
              <Label :for="`hop-name-${index}`">Hop Variety</Label>
              <Input
                :id="`hop-name-${index}`"
                v-model="hop.name"
                placeholder="e.g., Cascade"
              />
            </div>
            <div class="space-y-2">
              <Label :for="`hop-alpha-${index}`">Alpha Acid %</Label>
              <Input
                :id="`hop-alpha-${index}`"
                v-model.number="hop.alpha_acid"
                type="number"
                step="0.1"
                min="0"
              />
            </div>
            <div class="space-y-2">
              <Label :for="`hop-amount-${index}`">Amount (oz)</Label>
              <Input
                :id="`hop-amount-${index}`"
                v-model.number="hop.amount_oz"
                type="number"
                step="0.1"
                min="0"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div class="space-y-2">
              <Label :for="`hop-time-${index}`">Boil Time (min)</Label>
              <Input
                :id="`hop-time-${index}`"
                v-model.number="hop.time_min"
                type="number"
                step="1"
                min="0"
              />
            </div>
            <div class="space-y-2">
              <Label :for="`hop-type-${index}`">Type</Label>
              <select
                :id="`hop-type-${index}`"
                v-model="hop.type"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
              >
                <option value="Bittering">Bittering</option>
                <option value="Aroma">Aroma</option>
                <option value="Dual Purpose">Dual Purpose</option>
              </select>
            </div>
            <div class="space-y-2">
              <Label :for="`hop-form-${index}`">Form</Label>
              <select
                :id="`hop-form-${index}`"
                v-model="hop.form"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
              >
                <option value="Pellet">Pellet</option>
                <option value="Whole">Whole</option>
                <option value="Plug">Plug</option>
              </select>
            </div>
          </div>

          <!-- Substitution Suggestions -->
          <div v-if="hop.name" class="pt-2">
            <Button
              variant="outline"
              size="sm"
              @click="showSubstitutions(hop.name, hop.alpha_acid)"
            >
              <Search class="h-4 w-4 mr-2" />
              Find Substitutions
            </Button>
          </div>
        </div>
      </div>

      <!-- Calculate Button -->
      <div class="flex justify-center">
        <Button :disabled="hops.length === 0 || calculating" @click="calculateSchedule">
          <Calculator class="h-4 w-4 mr-2" />
          {{ calculating ? 'Calculating...' : 'Calculate Hop Schedule' }}
        </Button>
      </div>

      <!-- Results -->
      <div v-if="results" class="space-y-4 pt-4 border-t">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold">Results</h3>
          <div class="text-2xl font-bold text-primary">
            {{ results.total_ibu }} IBU
          </div>
        </div>

        <!-- IBU Contribution Chart -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-semibold mb-3">IBU Contributions</h4>
          <div class="space-y-2">
            <div
              v-for="(contribution, index) in sortedContributions"
              :key="index"
              class="flex items-center gap-3"
            >
              <div class="flex-shrink-0 w-32 text-sm">
                {{ contribution.name }}
              </div>
              <div class="flex-1">
                <div class="h-8 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    class="h-full bg-gradient-to-r from-green-500 to-green-600 flex items-center px-3"
                    :style="{ width: `${(contribution.ibu / results.total_ibu) * 100}%` }"
                  >
                    <span class="text-xs font-medium text-white">
                      {{ contribution.ibu }} IBU
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex-shrink-0 w-24 text-sm text-gray-600 text-right">
                {{ contribution.utilization }}%
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Contributions Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100">
              <tr>
                <th class="px-4 py-2 text-left">Hop</th>
                <th class="px-4 py-2 text-center">Time</th>
                <th class="px-4 py-2 text-center">Amount</th>
                <th class="px-4 py-2 text-center">IBU</th>
                <th class="px-4 py-2 text-center">Utilization</th>
                <th class="px-4 py-2 text-center">Type</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(contribution, index) in sortedContributions"
                :key="index"
                class="border-b hover:bg-gray-50"
              >
                <td class="px-4 py-3 font-medium">{{ contribution.name }}</td>
                <td class="px-4 py-3 text-center">{{ contribution.time_min }} min</td>
                <td class="px-4 py-3 text-center">{{ contribution.amount_oz }} oz</td>
                <td class="px-4 py-3 text-center font-semibold">{{ contribution.ibu }}</td>
                <td class="px-4 py-3 text-center">{{ contribution.utilization }}%</td>
                <td class="px-4 py-3 text-center">
                  <span
                    class="px-2 py-1 rounded-full text-xs"
                    :class="getTypeColor(contribution.type)"
                  >
                    {{ contribution.type }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Substitution Dialog -->
      <Dialog v-model:open="substitutionDialogOpen">
        <DialogContent class="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Hop Substitutions for {{ currentHopForSubstitution }}</DialogTitle>
            <DialogDescription>
              Similar hop varieties that can substitute for {{ currentHopForSubstitution }}
            </DialogDescription>
          </DialogHeader>

          <div v-if="loadingSubstitutions" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>

          <div v-else-if="substitutions && substitutions.length > 0" class="space-y-3">
            <div
              v-for="(sub, index) in substitutions"
              :key="index"
              class="p-4 border rounded-lg hover:bg-gray-50"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <h4 class="font-semibold">{{ sub.name }}</h4>
                    <span class="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                      {{ sub.alpha_acid_range }} AA
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ sub.characteristics }}</p>
                  <p v-if="sub.origin" class="text-xs text-gray-500 mt-1">
                    Origin: {{ sub.origin }}
                  </p>
                </div>
                <div class="flex-shrink-0 ml-4">
                  <div class="text-center">
                    <div class="text-2xl font-bold text-primary">
                      {{ sub.similarity_score }}
                    </div>
                    <div class="text-xs text-gray-500">Match</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            No substitutions found for this hop variety.
          </div>
        </DialogContent>
      </Dialog>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Plus, Trash2, Calculator, Search } from 'lucide-vue-next'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Button } from '~/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '~/components/ui/dialog'

interface HopAddition {
  name: string
  alpha_acid: number
  amount_oz: number
  time_min: number
  type: string
  form: string
}

interface HopContribution {
  name: string
  time_min: number
  amount_oz: number
  ibu: number
  utilization: number
  type?: string
  form?: string
}

interface HopScheduleResponse {
  total_ibu: number
  hop_contributions: HopContribution[]
}

interface HopSubstitution {
  name: string
  alpha_acid_range: string
  similarity_score: number
  characteristics: string
  origin?: string
}

const batchSize = ref(5.0)
const boilGravity = ref(1.050)
const hops = ref<HopAddition[]>([])
const calculating = ref(false)
const results = ref<HopScheduleResponse | null>(null)

// Substitution dialog
const substitutionDialogOpen = ref(false)
const currentHopForSubstitution = ref('')
const loadingSubstitutions = ref(false)
const substitutions = ref<HopSubstitution[]>([])

const sortedContributions = computed(() => {
  if (!results.value) return []
  return [...results.value.hop_contributions].sort((a, b) => b.time_min - a.time_min)
})

function addHop() {
  hops.value.push({
    name: '',
    alpha_acid: 5.0,
    amount_oz: 1.0,
    time_min: 60,
    type: 'Bittering',
    form: 'Pellet',
  })
}

function removeHop(index: number) {
  hops.value.splice(index, 1)
  // Clear results when hops change
  results.value = null
}

async function calculateSchedule() {
  if (hops.value.length === 0) return

  calculating.value = true
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase || 'http://localhost:8000'

    const response = await fetch(`${apiBase}/api/calculators/hop-schedule`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        hops: hops.value,
        batch_size_gal: batchSize.value,
        boil_gravity: boilGravity.value,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to calculate hop schedule')
    }

    results.value = await response.json()
  } catch (error) {
    console.error('Error calculating hop schedule:', error)
    alert('Failed to calculate hop schedule. Please try again.')
  } finally {
    calculating.value = false
  }
}

async function showSubstitutions(hopName: string, alphaAcid?: number) {
  currentHopForSubstitution.value = hopName
  substitutionDialogOpen.value = true
  loadingSubstitutions.value = true
  substitutions.value = []

  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase || 'http://localhost:8000'

    const response = await fetch(`${apiBase}/api/calculators/hop-substitutions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        hop_name: hopName,
        alpha_acid: alphaAcid,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to fetch substitutions')
    }

    const data = await response.json()
    substitutions.value = data.substitutes
  } catch (error) {
    console.error('Error fetching substitutions:', error)
  } finally {
    loadingSubstitutions.value = false
  }
}

function getTypeColor(type?: string) {
  if (!type) return 'bg-gray-100 text-gray-800'
  
  switch (type.toLowerCase()) {
    case 'bittering':
      return 'bg-orange-100 text-orange-800'
    case 'aroma':
      return 'bg-green-100 text-green-800'
    case 'dual purpose':
      return 'bg-blue-100 text-blue-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
</script>
