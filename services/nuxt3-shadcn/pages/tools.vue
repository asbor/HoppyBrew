<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Button } from '~/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '~/components/ui/tabs'

// ABV Calculator State
const og = ref<number>(1.050)
const fg = ref<number>(1.010)
const abv = computed(() => {
  if (og.value <= fg.value) return 0
  return ((og.value - fg.value) * 131.25).toFixed(2)
})

// IBU Calculator State (Tinseth)
const alphaAcid = ref<number>(12.0)
const hopWeight = ref<number>(1.0)
const boilTime = ref<number>(60)
const batchSize = ref<number>(5.0)
const boilGravity = ref<number>(1.050)

const ibu = computed(() => {
  if (alphaAcid.value === 0 || hopWeight.value === 0 || boilTime.value === 0) return 0
  
  const gravityFactor = 1.65 * Math.pow(0.000125, boilGravity.value - 1.0)
  const timeFactor = (1 - Math.exp(-0.04 * boilTime.value)) / 4.15
  const utilization = gravityFactor * timeFactor
  const alphaFraction = alphaAcid.value / 100.0
  
  // Convert oz/gal to metric (28.35g per oz, 3.785L per gal)
  const weightGrams = hopWeight.value * 28.35
  const volumeLiters = batchSize.value * 3.785
  const ibuValue = (alphaFraction * weightGrams * 1000 * utilization) / volumeLiters
  
  return Math.max(ibuValue, 0).toFixed(1)
})

// SRM Calculator State (Morey)
const grainColor = ref<number>(3.0)
const grainWeight = ref<number>(10.0)
const batchSizeSRM = ref<number>(5.0)

const srm = computed(() => {
  if (grainColor.value === 0 || grainWeight.value === 0) return 0
  
  // Convert lbs/gal to metric (0.454kg per lb, 3.785L per gal)
  const weightKg = grainWeight.value * 0.454
  const volumeLiters = batchSizeSRM.value * 3.785
  const mcu = (weightKg * 2.20462 * grainColor.value) / (volumeLiters / 3.785) // Back to imperial for MCU
  
  return (1.4922 * Math.pow(mcu, 0.6859)).toFixed(1)
})

const srmColor = computed(() => {
  const srmValue = parseFloat(srm.value)
  if (srmValue < 2) return '#FFE699'
  if (srmValue < 4) return '#FFD878'
  if (srmValue < 6) return '#FFCA5A'
  if (srmValue < 8) return '#FFBF42'
  if (srmValue < 10) return '#FBB123'
  if (srmValue < 13) return '#F8A600'
  if (srmValue < 17) return '#F39C00'
  if (srmValue < 20) return '#EA8F00'
  if (srmValue < 24) return '#E58500'
  if (srmValue < 30) return '#DE7C00'
  if (srmValue < 40) return '#D77200'
  return '#8D4C1A'
})

// Priming Sugar Calculator State
const batchVolume = ref<number>(19.0) // Liters
const desiredCO2 = ref<number>(2.4) // volumes
const temperature = ref<number>(20) // Celsius
const sugarType = ref<string>('table')

const primingSugar = computed(() => {
  // Calculate dissolved CO2 at temperature
  const dissolvedCO2 = 3.0378 - (0.050062 * temperature.value) + (0.00026555 * Math.pow(temperature.value, 2))
  
  // CO2 needed
  const co2Needed = desiredCO2.value - dissolvedCO2
  
  if (co2Needed <= 0) return { grams: 0, oz: 0 }
  
  // Sugar conversion factors (grams per liter for 1 volume CO2)
  const sugarFactors: { [key: string]: number } = {
    'table': 4.0,      // Table sugar (sucrose)
    'corn': 4.5,       // Corn sugar (dextrose)
    'dme': 5.3,        // Dry malt extract
    'honey': 3.8       // Honey
  }
  
  const factor = sugarFactors[sugarType.value] || 4.0
  const totalGrams = co2Needed * factor * batchVolume.value
  
  return {
    grams: totalGrams.toFixed(0),
    oz: (totalGrams / 28.35).toFixed(1)
  }
})

// Strike Water Calculator State
const grainTemp = ref<number>(20) // Celsius
const targetTemp = ref<number>(67) // Celsius
const grainWeightKg = ref<number>(5.0)
const waterToGrainRatio = ref<number>(3.0) // L/kg

const strikeWater = computed(() => {
  // Simplified infusion equation
  const waterVolume = grainWeightKg.value * waterToGrainRatio.value
  const tempDiff = targetTemp.value - grainTemp.value
  const strikeTemp = targetTemp.value + (0.41 / waterToGrainRatio.value) * tempDiff
  
  return {
    volume: waterVolume.toFixed(1),
    temperature: strikeTemp.toFixed(1)
  }
})

// Dilution Calculator State
const currentGravity = ref<number>(1.060)
const currentVolume = ref<number>(20)
const targetGravityDilute = ref<number>(1.050)

const dilutionWater = computed(() => {
  if (currentGravity.value <= targetGravityDilute.value) return { volume: 0, finalVolume: currentVolume.value }
  
  const gravityPoints = (currentGravity.value - 1) * 1000
  const targetPoints = (targetGravityDilute.value - 1) * 1000
  
  const finalVolume = (gravityPoints * currentVolume.value) / targetPoints
  const waterToAdd = finalVolume - currentVolume.value
  
  return {
    volume: waterToAdd.toFixed(1),
    finalVolume: finalVolume.toFixed(1)
  }
})

// Yeast Pitch Rate Calculator
const targetGravity = ref<number>(1.050)
const batchVolumeYeast = ref<number>(20) // Liters
const yeastType = ref<string>('ale')

const yeastCells = computed(() => {
  const gravityPoints = (targetGravity.value - 1) * 1000
  
  // Pitch rate: million cells per mL per degree Plato
  const pitchRates: { [key: string]: number } = {
    'ale': 0.75,
    'lager': 1.5,
    'high-gravity': 1.5
  }
  
  const rate = pitchRates[yeastType.value] || 0.75
  const plato = gravityPoints / 4 // Rough conversion
  const totalCells = rate * (batchVolumeYeast.value * 1000) * plato
  
  return {
    billion: (totalCells / 1000).toFixed(0),
    packages: Math.ceil(totalCells / 100000) // Assuming 100B cells per package
  }
})
</script>

<template>
  <div class="container mx-auto py-6 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Brewing Calculators</h1>
        <p class="text-muted-foreground">Essential tools for recipe design and brew day</p>
      </div>
    </div>

    <Tabs default-value="abv" class="w-full">
      <TabsList class="grid w-full grid-cols-3 lg:grid-cols-7">
        <TabsTrigger value="abv">ABV</TabsTrigger>
        <TabsTrigger value="ibu">IBU</TabsTrigger>
        <TabsTrigger value="srm">SRM</TabsTrigger>
        <TabsTrigger value="priming">Priming</TabsTrigger>
        <TabsTrigger value="strike">Strike Water</TabsTrigger>
        <TabsTrigger value="dilution">Dilution</TabsTrigger>
        <TabsTrigger value="yeast">Yeast</TabsTrigger>
      </TabsList>

      <!-- ABV Calculator -->
      <TabsContent value="abv">
        <Card>
          <CardHeader>
            <CardTitle>ABV Calculator</CardTitle>
            <CardDescription>Calculate alcohol by volume from gravity readings</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="og">Original Gravity (OG)</Label>
                <Input id="og" type="number" step="0.001" v-model.number="og" />
              </div>
              <div class="space-y-2">
                <Label for="fg">Final Gravity (FG)</Label>
                <Input id="fg" type="number" step="0.001" v-model.number="fg" />
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center">
                <p class="text-sm text-muted-foreground mb-2">Alcohol by Volume</p>
                <p class="text-4xl font-bold text-primary">{{ abv }}%</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- IBU Calculator -->
      <TabsContent value="ibu">
        <Card>
          <CardHeader>
            <CardTitle>IBU Calculator (Tinseth)</CardTitle>
            <CardDescription>Calculate bitterness from hop additions</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="alpha">Alpha Acid (%)</Label>
                <Input id="alpha" type="number" step="0.1" v-model.number="alphaAcid" />
              </div>
              <div class="space-y-2">
                <Label for="hopWeight">Hop Weight (oz)</Label>
                <Input id="hopWeight" type="number" step="0.1" v-model.number="hopWeight" />
              </div>
              <div class="space-y-2">
                <Label for="boilTime">Boil Time (min)</Label>
                <Input id="boilTime" type="number" v-model.number="boilTime" />
              </div>
              <div class="space-y-2">
                <Label for="batchSize">Batch Size (gal)</Label>
                <Input id="batchSize" type="number" step="0.1" v-model.number="batchSize" />
              </div>
              <div class="space-y-2">
                <Label for="boilGravity">Boil Gravity</Label>
                <Input id="boilGravity" type="number" step="0.001" v-model.number="boilGravity" />
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center">
                <p class="text-sm text-muted-foreground mb-2">International Bitterness Units</p>
                <p class="text-4xl font-bold text-primary">{{ ibu }} IBU</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- SRM Calculator -->
      <TabsContent value="srm">
        <Card>
          <CardHeader>
            <CardTitle>SRM Color Calculator (Morey)</CardTitle>
            <CardDescription>Estimate beer color from grain bill</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="space-y-2">
                <Label for="grainColor">Grain Color (°L)</Label>
                <Input id="grainColor" type="number" step="0.1" v-model.number="grainColor" />
              </div>
              <div class="space-y-2">
                <Label for="grainWeight">Grain Weight (lbs)</Label>
                <Input id="grainWeight" type="number" step="0.1" v-model.number="grainWeight" />
              </div>
              <div class="space-y-2">
                <Label for="batchSizeSRM">Batch Size (gal)</Label>
                <Input id="batchSizeSRM" type="number" step="0.1" v-model.number="batchSizeSRM" />
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center space-y-3">
                <p class="text-sm text-muted-foreground">Standard Reference Method</p>
                <p class="text-4xl font-bold text-primary">{{ srm }} SRM</p>
                <div class="flex justify-center">
                  <div 
                    class="w-32 h-32 rounded-lg border-2 border-gray-300" 
                    :style="{ backgroundColor: srmColor }"
                  ></div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Priming Sugar Calculator -->
      <TabsContent value="priming">
        <Card>
          <CardHeader>
            <CardTitle>Priming Sugar Calculator</CardTitle>
            <CardDescription>Calculate priming sugar for carbonation</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="batchVolume">Batch Volume (L)</Label>
                <Input id="batchVolume" type="number" step="0.1" v-model.number="batchVolume" />
              </div>
              <div class="space-y-2">
                <Label for="desiredCO2">Desired CO₂ (volumes)</Label>
                <Input id="desiredCO2" type="number" step="0.1" v-model.number="desiredCO2" />
              </div>
              <div class="space-y-2">
                <Label for="temperature">Beer Temperature (°C)</Label>
                <Input id="temperature" type="number" v-model.number="temperature" />
              </div>
              <div class="space-y-2">
                <Label for="sugarType">Sugar Type</Label>
                <select id="sugarType" v-model="sugarType" class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                  <option value="table">Table Sugar (Sucrose)</option>
                  <option value="corn">Corn Sugar (Dextrose)</option>
                  <option value="dme">Dry Malt Extract</option>
                  <option value="honey">Honey</option>
                </select>
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center space-y-2">
                <p class="text-sm text-muted-foreground">Required Priming Sugar</p>
                <div class="flex justify-center gap-8">
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ primingSugar.grams }}</p>
                    <p class="text-sm text-muted-foreground">grams</p>
                  </div>
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ primingSugar.oz }}</p>
                    <p class="text-sm text-muted-foreground">oz</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Strike Water Calculator -->
      <TabsContent value="strike">
        <Card>
          <CardHeader>
            <CardTitle>Strike Water Calculator</CardTitle>
            <CardDescription>Calculate strike water temperature for mashing</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="grainTemp">Grain Temperature (°C)</Label>
                <Input id="grainTemp" type="number" v-model.number="grainTemp" />
              </div>
              <div class="space-y-2">
                <Label for="targetTemp">Target Mash Temperature (°C)</Label>
                <Input id="targetTemp" type="number" v-model.number="targetTemp" />
              </div>
              <div class="space-y-2">
                <Label for="grainWeightKg">Grain Weight (kg)</Label>
                <Input id="grainWeightKg" type="number" step="0.1" v-model.number="grainWeightKg" />
              </div>
              <div class="space-y-2">
                <Label for="waterToGrainRatio">Water to Grain Ratio (L/kg)</Label>
                <Input id="waterToGrainRatio" type="number" step="0.1" v-model.number="waterToGrainRatio" />
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center space-y-3">
                <p class="text-sm text-muted-foreground">Strike Water Requirements</p>
                <div class="flex justify-center gap-8">
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ strikeWater.volume }}</p>
                    <p class="text-sm text-muted-foreground">Liters</p>
                  </div>
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ strikeWater.temperature }}</p>
                    <p class="text-sm text-muted-foreground">°C</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Dilution Calculator -->
      <TabsContent value="dilution">
        <Card>
          <CardHeader>
            <CardTitle>Dilution Calculator</CardTitle>
            <CardDescription>Calculate water needed to dilute wort</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="space-y-2">
                <Label for="currentGravity">Current Gravity</Label>
                <Input id="currentGravity" type="number" step="0.001" v-model.number="currentGravity" />
              </div>
              <div class="space-y-2">
                <Label for="currentVolume">Current Volume (L)</Label>
                <Input id="currentVolume" type="number" step="0.1" v-model.number="currentVolume" />
              </div>
              <div class="space-y-2">
                <Label for="targetGravityDilute">Target Gravity</Label>
                <Input id="targetGravityDilute" type="number" step="0.001" v-model.number="targetGravityDilute" />
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center space-y-3">
                <p class="text-sm text-muted-foreground">Water to Add</p>
                <div class="flex justify-center gap-8">
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ dilutionWater.volume }}</p>
                    <p class="text-sm text-muted-foreground">Liters</p>
                  </div>
                  <div>
                    <p class="text-sm text-muted-foreground mt-2">Final Volume: {{ dilutionWater.finalVolume }} L</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Yeast Pitch Rate Calculator -->
      <TabsContent value="yeast">
        <Card>
          <CardHeader>
            <CardTitle>Yeast Pitch Rate Calculator</CardTitle>
            <CardDescription>Calculate required yeast cells for healthy fermentation</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="space-y-2">
                <Label for="targetGravity">Target Gravity</Label>
                <Input id="targetGravity" type="number" step="0.001" v-model.number="targetGravity" />
              </div>
              <div class="space-y-2">
                <Label for="batchVolumeYeast">Batch Volume (L)</Label>
                <Input id="batchVolumeYeast" type="number" step="0.1" v-model.number="batchVolumeYeast" />
              </div>
              <div class="space-y-2">
                <Label for="yeastType">Yeast Type</Label>
                <select id="yeastType" v-model="yeastType" class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                  <option value="ale">Ale</option>
                  <option value="lager">Lager</option>
                  <option value="high-gravity">High Gravity</option>
                </select>
              </div>
            </div>
            <div class="pt-4 border-t">
              <div class="text-center space-y-3">
                <p class="text-sm text-muted-foreground">Required Yeast Cells</p>
                <div class="flex justify-center gap-8">
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ yeastCells.billion }}</p>
                    <p class="text-sm text-muted-foreground">Billion Cells</p>
                  </div>
                  <div>
                    <p class="text-3xl font-bold text-primary">{{ yeastCells.packages }}</p>
                    <p class="text-sm text-muted-foreground">Packages (≈100B each)</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  </div>
</template>