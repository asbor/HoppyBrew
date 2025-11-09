<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Button } from '~/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '~/components/ui/tabs'
import HopScheduleOptimizer from '~/components/tools/HopScheduleOptimizer.vue'

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

// Water Adjustment Calculator
const sourceWater = ref({
  calcium: 50,
  magnesium: 10,
  sodium: 15,
  chloride: 60,
  sulfate: 120,
  bicarbonate: 80
})

const targetWater = ref({
  calcium: 100,
  magnesium: 15,
  sodium: 20,
  chloride: 100,
  sulfate: 200,
  bicarbonate: 40
})

const waterVolume = ref<number>(20) // Liters
const mashGrainWeight = ref<number>(5) // kg for mash pH

// Brewing salts molecular weights and ion contributions
const salts = {
  'gypsum': { name: 'Gypsum (CaSO4·2H2O)', calcium: 23.3, sulfate: 55.8, mw: 172.2 },
  'calcium_chloride': { name: 'Calcium Chloride (CaCl2)', calcium: 27.3, chloride: 48.0, mw: 147 },
  'epsom': { name: 'Epsom Salt (MgSO4·7H2O)', magnesium: 9.9, sulfate: 39.0, mw: 246.5 },
  'table_salt': { name: 'Table Salt (NaCl)', sodium: 39.3, chloride: 60.7, mw: 58.4 },
  'baking_soda': { name: 'Baking Soda (NaHCO3)', sodium: 27.4, bicarbonate: 72.6, mw: 84 },
  'chalk': { name: 'Chalk (CaCO3)', calcium: 40.0, bicarbonate: 0, mw: 100 }
}

const waterAdjustments = computed(() => {
  const adjustments: { [key: string]: number } = {}
  const results = { ...sourceWater.value }
  
  // Calculate differences needed
  const deltaCa = targetWater.value.calcium - sourceWater.value.calcium
  const deltaMg = targetWater.value.magnesium - sourceWater.value.magnesium
  const deltaNa = targetWater.value.sodium - sourceWater.value.sodium
  const deltaCl = targetWater.value.chloride - sourceWater.value.chloride
  const deltaSO4 = targetWater.value.sulfate - sourceWater.value.sulfate
  const deltaHCO3 = targetWater.value.bicarbonate - sourceWater.value.bicarbonate
  
  // Initialize salt additions
  adjustments.gypsum = 0
  adjustments.calcium_chloride = 0
  adjustments.epsom = 0
  adjustments.table_salt = 0
  adjustments.baking_soda = 0
  
  // Calculate salt additions (simplified approach - prioritize gypsum for Ca+SO4, CaCl2 for Ca+Cl)
  if (deltaCa > 0 && deltaSO4 > 0) {
    // Use gypsum for calcium and sulfate
    const gypsumNeeded = Math.min(deltaCa / salts.gypsum.calcium, deltaSO4 / salts.gypsum.sulfate)
    adjustments.gypsum = gypsumNeeded * waterVolume.value
    results.calcium += gypsumNeeded * salts.gypsum.calcium
    results.sulfate += gypsumNeeded * salts.gypsum.sulfate
  }
  
  // Remaining calcium needs
  const remainingCa = targetWater.value.calcium - results.calcium
  if (remainingCa > 0 && deltaCl > 0) {
    const cacl2Needed = Math.min(remainingCa / salts.calcium_chloride.calcium, deltaCl / salts.calcium_chloride.chloride)
    adjustments.calcium_chloride = cacl2Needed * waterVolume.value
    results.calcium += cacl2Needed * salts.calcium_chloride.calcium
    results.chloride += cacl2Needed * salts.calcium_chloride.chloride
  }
  
  // Magnesium adjustment
  if (deltaMg > 0) {
    adjustments.epsom = (deltaMg / salts.epsom.magnesium) * waterVolume.value
    results.magnesium += deltaMg
    results.sulfate += (deltaMg / salts.epsom.magnesium) * salts.epsom.sulfate
  }
  
  // Sodium adjustment
  if (deltaNa > 0) {
    if (deltaHCO3 > 0) {
      // Prefer baking soda if bicarbonate is also needed
      const sodaNeeded = Math.min(deltaNa / salts.baking_soda.sodium, deltaHCO3 / salts.baking_soda.bicarbonate)
      adjustments.baking_soda = sodaNeeded * waterVolume.value
      results.sodium += sodaNeeded * salts.baking_soda.sodium
      results.bicarbonate += sodaNeeded * salts.baking_soda.bicarbonate
      
      // Remaining sodium with table salt
      const remainingNa = targetWater.value.sodium - results.sodium
      if (remainingNa > 0) {
        adjustments.table_salt = (remainingNa / salts.table_salt.sodium) * waterVolume.value
        results.sodium += remainingNa
        results.chloride += (remainingNa / salts.table_salt.sodium) * salts.table_salt.chloride
      }
    } else {
      adjustments.table_salt = (deltaNa / salts.table_salt.sodium) * waterVolume.value
      results.sodium += deltaNa
      results.chloride += (deltaNa / salts.table_salt.sodium) * salts.table_salt.chloride
    }
  }
  
  return {
    salts: adjustments,
    finalWater: results
  }
})

const mashPH = computed(() => {
  // Simplified mash pH calculation based on alkalinity and grain weight
  const alkalinity = waterAdjustments.value.finalWater.bicarbonate * 0.819 // Convert to CaCO3 equivalent
  const grainAlkalinity = mashGrainWeight.value * 30 // Estimated grain contribution (varies by grain type)
  const residualAlkalinity = alkalinity - (waterAdjustments.value.finalWater.calcium / 3.5 + waterAdjustments.value.finalWater.magnesium / 7)
  
  // Rough pH estimation (actual depends on grain bill, water composition, etc.)
  const estimatedPH = 5.8 - ((residualAlkalinity - grainAlkalinity) / 50)
  
  return Math.max(4.5, Math.min(6.5, estimatedPH)).toFixed(2)
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
      <TabsList class="grid w-full grid-cols-4 lg:grid-cols-9">
        <TabsTrigger value="abv">ABV</TabsTrigger>
        <TabsTrigger value="ibu">IBU</TabsTrigger>
        <TabsTrigger value="srm">SRM</TabsTrigger>
        <TabsTrigger value="priming">Priming</TabsTrigger>
        <TabsTrigger value="strike">Strike Water</TabsTrigger>
        <TabsTrigger value="dilution">Dilution</TabsTrigger>
        <TabsTrigger value="yeast">Yeast</TabsTrigger>
        <TabsTrigger value="water">Water Adjust</TabsTrigger>
        <TabsTrigger value="hop-schedule">Hop Schedule</TabsTrigger>
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

      <!-- Water Adjustment Calculator -->
      <TabsContent value="water">
        <Card>
          <CardHeader>
            <CardTitle>Water Adjustment Calculator</CardTitle>
            <CardDescription>Calculate brewing salt additions to achieve target water profile</CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Source Water Profile -->
              <div>
                <h3 class="text-lg font-semibold mb-3">Source Water Profile (ppm)</h3>
                <div class="grid grid-cols-2 gap-3">
                  <div class="space-y-2">
                    <Label for="srcCa">Calcium (Ca²⁺)</Label>
                    <Input id="srcCa" type="number" min="0" v-model.number="sourceWater.calcium" />
                  </div>
                  <div class="space-y-2">
                    <Label for="srcMg">Magnesium (Mg²⁺)</Label>
                    <Input id="srcMg" type="number" min="0" v-model.number="sourceWater.magnesium" />
                  </div>
                  <div class="space-y-2">
                    <Label for="srcNa">Sodium (Na⁺)</Label>
                    <Input id="srcNa" type="number" min="0" v-model.number="sourceWater.sodium" />
                  </div>
                  <div class="space-y-2">
                    <Label for="srcCl">Chloride (Cl⁻)</Label>
                    <Input id="srcCl" type="number" min="0" v-model.number="sourceWater.chloride" />
                  </div>
                  <div class="space-y-2">
                    <Label for="srcSO4">Sulfate (SO₄²⁻)</Label>
                    <Input id="srcSO4" type="number" min="0" v-model.number="sourceWater.sulfate" />
                  </div>
                  <div class="space-y-2">
                    <Label for="srcHCO3">Bicarbonate (HCO₃⁻)</Label>
                    <Input id="srcHCO3" type="number" min="0" v-model.number="sourceWater.bicarbonate" />
                  </div>
                </div>
              </div>

              <!-- Target Water Profile -->
              <div>
                <h3 class="text-lg font-semibold mb-3">Target Water Profile (ppm)</h3>
                <div class="grid grid-cols-2 gap-3">
                  <div class="space-y-2">
                    <Label for="tgtCa">Calcium (Ca²⁺)</Label>
                    <Input id="tgtCa" type="number" min="0" v-model.number="targetWater.calcium" />
                  </div>
                  <div class="space-y-2">
                    <Label for="tgtMg">Magnesium (Mg²⁺)</Label>
                    <Input id="tgtMg" type="number" min="0" v-model.number="targetWater.magnesium" />
                  </div>
                  <div class="space-y-2">
                    <Label for="tgtNa">Sodium (Na⁺)</Label>
                    <Input id="tgtNa" type="number" min="0" v-model.number="targetWater.sodium" />
                  </div>
                  <div class="space-y-2">
                    <Label for="tgtCl">Chloride (Cl⁻)</Label>
                    <Input id="tgtCl" type="number" min="0" v-model.number="targetWater.chloride" />
                  </div>
                  <div class="space-y-2">
                    <Label for="tgtSO4">Sulfate (SO₄²⁻)</Label>
                    <Input id="tgtSO4" type="number" min="0" v-model.number="targetWater.sulfate" />
                  </div>
                  <div class="space-y-2">
                    <Label for="tgtHCO3">Bicarbonate (HCO₃⁻)</Label>
                    <Input id="tgtHCO3" type="number" min="0" v-model.number="targetWater.bicarbonate" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Batch Parameters -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
              <div class="space-y-2">
                <Label for="waterVolume">Water Volume (L)</Label>
                <Input id="waterVolume" type="number" step="0.1" min="1" v-model.number="waterVolume" />
              </div>
              <div class="space-y-2">
                <Label for="mashGrainWeight">Grain Weight (kg) - for pH estimation</Label>
                <Input id="mashGrainWeight" type="number" step="0.1" min="0" v-model.number="mashGrainWeight" />
              </div>
            </div>

            <!-- Results -->
            <div class="pt-4 border-t space-y-4">
              <h3 class="text-lg font-semibold">Salt Additions Required</h3>
              
              <!-- Salt Additions Table -->
              <div class="bg-gray-50 p-4 rounded-lg">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div v-for="(amount, salt) in waterAdjustments.salts" :key="salt" 
                       class="bg-white p-3 rounded border">
                    <div class="font-semibold text-sm">{{ salts[salt as keyof typeof salts].name }}</div>
                    <div class="text-2xl font-bold text-primary">
                      {{ amount.toFixed(2) }} g
                    </div>
                    <div class="text-sm text-muted-foreground">
                      {{ (amount * 1000 / waterVolume).toFixed(1) }} mg/L
                    </div>
                  </div>
                </div>
              </div>

              <!-- Final Water Profile -->
              <div class="space-y-3">
                <h4 class="font-semibold">Calculated Final Water Profile</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 text-sm">
                  <div class="text-center p-2 bg-blue-50 rounded">
                    <div class="font-medium">Ca²⁺</div>
                    <div class="text-xl font-bold">{{ waterAdjustments.finalWater.calcium.toFixed(0) }}</div>
                    <div class="text-xs text-muted-foreground">ppm</div>
                  </div>
                  <div class="text-center p-2 bg-green-50 rounded">
                    <div class="font-medium">Mg²⁺</div>
                    <div class="text-xl font-bold">{{ waterAdjustments.finalWater.magnesium.toFixed(0) }}</div>
                    <div class="text-xs text-muted-foreground">ppm</div>
                  </div>
                  <div class="text-center p-2 bg-yellow-50 rounded">
                    <div class="font-medium">Na⁺</div>
                    <div class="text-xl font-bold">{{ waterAdjustments.finalWater.sodium.toFixed(0) }}</div>
                    <div class="text-xs text-muted-foreground">ppm</div>
                  </div>
                  <div class="text-center p-2 bg-orange-50 rounded">
                    <div class="font-medium">Cl⁻</div>
                    <div class="text-xl font-bold">{{ waterAdjustments.finalWater.chloride.toFixed(0) }}</div>
                    <div class="text-xs text-muted-foreground">ppm</div>
                  </div>
                  <div class="text-center p-2 bg-red-50 rounded">
                    <div class="font-medium">SO₄²⁻</div>
                    <div class="text-xl font-bold">{{ waterAdjustments.finalWater.sulfate.toFixed(0) }}</div>
                    <div class="text-xs text-muted-foreground">ppm</div>
                  </div>
                  <div class="text-center p-2 bg-purple-50 rounded">
                    <div class="font-medium">HCO₃⁻</div>
                    <div class="text-xl font-bold">{{ waterAdjustments.finalWater.bicarbonate.toFixed(0) }}</div>
                    <div class="text-xs text-muted-foreground">ppm</div>
                  </div>
                </div>

                <!-- Key Ratios & pH -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                  <div class="text-center p-3 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
                    <div class="font-medium text-sm">SO₄:Cl Ratio</div>
                    <div class="text-2xl font-bold text-blue-700">
                      {{ waterAdjustments.finalWater.chloride > 0 ? 
                           (waterAdjustments.finalWater.sulfate / waterAdjustments.finalWater.chloride).toFixed(2) : 
                           '∞' }}
                    </div>
                    <div class="text-xs text-blue-600">
                      {{ waterAdjustments.finalWater.sulfate / waterAdjustments.finalWater.chloride > 1.5 ? 'Hoppy/Bitter' : 
                         waterAdjustments.finalWater.sulfate / waterAdjustments.finalWater.chloride < 0.6 ? 'Malty/Sweet' : 'Balanced' }}
                    </div>
                  </div>
                  <div class="text-center p-3 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
                    <div class="font-medium text-sm">Estimated Mash pH</div>
                    <div class="text-2xl font-bold text-green-700">{{ mashPH }}</div>
                    <div class="text-xs text-green-600">
                      {{ parseFloat(mashPH) >= 5.2 && parseFloat(mashPH) <= 5.6 ? 'Optimal' : 'Check Recipe' }}
                    </div>
                  </div>
                  <div class="text-center p-3 bg-gradient-to-br from-amber-50 to-amber-100 rounded-lg">
                    <div class="font-medium text-sm">Total Hardness</div>
                    <div class="text-2xl font-bold text-amber-700">
                      {{ (waterAdjustments.finalWater.calcium * 2.5 + waterAdjustments.finalWater.magnesium * 4.1).toFixed(0) }}
                    </div>
                    <div class="text-xs text-amber-600">ppm CaCO₃</div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Hop Schedule Optimizer -->
      <TabsContent value="hop-schedule">
        <HopScheduleOptimizer />
      </TabsContent>

    </Tabs>
  </div>
</template>