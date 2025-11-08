import { randomString, getTimestamp } from './helpers'

/**
 * Generate test recipe data
 */
export function generateRecipeData(overrides?: Partial<{
  name: string
  type: string
  style: string
  brewer: string
  batchSize: number
  boilTime: number
  efficiency: number
}>) {
  return {
    id: `recipe-${randomString(10)}`,
    name: overrides?.name ?? `Test Recipe ${randomString(6)}`,
    type: overrides?.type ?? 'All Grain',
    style: overrides?.style ?? 'American IPA',
    brewer: overrides?.brewer ?? 'Test Brewer',
    batchSize: overrides?.batchSize ?? 19,
    boilTime: overrides?.boilTime ?? 60,
    efficiency: overrides?.efficiency ?? 72,
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate test batch data
 */
export function generateBatchData(overrides?: Partial<{
  name: string
  recipeId: string
  brewDate: string
  status: string
  notes: string
}>) {
  return {
    id: `batch-${randomString(10)}`,
    name: overrides?.name ?? `Test Batch ${randomString(6)}`,
    recipeId: overrides?.recipeId ?? `recipe-${randomString(10)}`,
    brewDate: overrides?.brewDate ?? new Date().toISOString().split('T')[0],
    status: overrides?.status ?? 'planning',
    notes: overrides?.notes ?? 'Test batch notes',
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate fermentation reading data
 */
export function generateFermentationReading(overrides?: Partial<{
  gravity: number
  temperature: number
  pH: number
  date: string
}>) {
  return {
    id: `reading-${randomString(10)}`,
    gravity: overrides?.gravity ?? 1.050,
    temperature: overrides?.temperature ?? 20,
    pH: overrides?.pH ?? 5.2,
    date: overrides?.date ?? new Date().toISOString(),
    createdAt: getTimestamp()
  }
}

/**
 * Generate inventory item data (hops)
 */
export function generateHopData(overrides?: Partial<{
  name: string
  alpha: number
  quantity: number
  unit: string
  form: string
}>) {
  return {
    id: `hop-${randomString(10)}`,
    name: overrides?.name ?? `Test Hop ${randomString(6)}`,
    alpha: overrides?.alpha ?? 12.5,
    quantity: overrides?.quantity ?? 100,
    unit: overrides?.unit ?? 'g',
    form: overrides?.form ?? 'Pellet',
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate inventory item data (fermentable)
 */
export function generateFermentableData(overrides?: Partial<{
  name: string
  type: string
  quantity: number
  unit: string
  ppg: number
  color: number
}>) {
  return {
    id: `fermentable-${randomString(10)}`,
    name: overrides?.name ?? `Test Malt ${randomString(6)}`,
    type: overrides?.type ?? 'Grain',
    quantity: overrides?.quantity ?? 5,
    unit: overrides?.unit ?? 'kg',
    ppg: overrides?.ppg ?? 37,
    color: overrides?.color ?? 4,
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate inventory item data (yeast)
 */
export function generateYeastData(overrides?: Partial<{
  name: string
  type: string
  form: string
  attenuation: number
  quantity: number
}>) {
  return {
    id: `yeast-${randomString(10)}`,
    name: overrides?.name ?? `Test Yeast ${randomString(6)}`,
    type: overrides?.type ?? 'Ale',
    form: overrides?.form ?? 'Dry',
    attenuation: overrides?.attenuation ?? 75,
    quantity: overrides?.quantity ?? 2,
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate water profile data
 */
export function generateWaterProfileData(overrides?: Partial<{
  name: string
  calcium: number
  magnesium: number
  sodium: number
  chloride: number
  sulfate: number
  bicarbonate: number
}>) {
  return {
    id: `water-${randomString(10)}`,
    name: overrides?.name ?? `Test Water Profile ${randomString(6)}`,
    calcium: overrides?.calcium ?? 50,
    magnesium: overrides?.magnesium ?? 10,
    sodium: overrides?.sodium ?? 20,
    chloride: overrides?.chloride ?? 50,
    sulfate: overrides?.sulfate ?? 150,
    bicarbonate: overrides?.bicarbonate ?? 100,
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate mash profile data
 */
export function generateMashProfileData(overrides?: Partial<{
  name: string
  description: string
  steps: Array<{
    name: string
    temperature: number
    time: number
    type: string
  }>
}>) {
  return {
    id: `mash-${randomString(10)}`,
    name: overrides?.name ?? `Test Mash Profile ${randomString(6)}`,
    description: overrides?.description ?? 'Test mash profile description',
    steps: overrides?.steps ?? [
      {
        name: 'Saccharification',
        temperature: 65,
        time: 60,
        type: 'Infusion'
      }
    ],
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate equipment profile data
 */
export function generateEquipmentProfileData(overrides?: Partial<{
  name: string
  batchSize: number
  boilSize: number
  boilTime: number
  efficiency: number
  trubLoss: number
}>) {
  return {
    id: `equipment-${randomString(10)}`,
    name: overrides?.name ?? `Test Equipment ${randomString(6)}`,
    batchSize: overrides?.batchSize ?? 20,
    boilSize: overrides?.boilSize ?? 25,
    boilTime: overrides?.boilTime ?? 60,
    efficiency: overrides?.efficiency ?? 75,
    trubLoss: overrides?.trubLoss ?? 1.0,
    createdAt: getTimestamp(),
    updatedAt: getTimestamp()
  }
}

/**
 * Generate complete recipe with ingredients
 */
export function generateCompleteRecipe() {
  const recipe = generateRecipeData()
  
  return {
    ...recipe,
    fermentables: [
      generateFermentableData({ name: 'Pale Malt', quantity: 5 }),
      generateFermentableData({ name: 'Crystal Malt', quantity: 0.5, color: 60 })
    ],
    hops: [
      generateHopData({ name: 'Cascade', quantity: 50, alpha: 7.5 }),
      generateHopData({ name: 'Centennial', quantity: 30, alpha: 10.0 })
    ],
    yeasts: [
      generateYeastData({ name: 'US-05', type: 'Ale', attenuation: 77 })
    ]
  }
}

/**
 * Generate BeerXML data
 */
export function generateBeerXMLData(recipeName?: string) {
  const name = recipeName ?? `Test Recipe ${randomString(6)}`
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<RECIPES>
  <RECIPE>
    <NAME>${name}</NAME>
    <VERSION>1</VERSION>
    <TYPE>All Grain</TYPE>
    <BREWER>Test Brewer</BREWER>
    <BATCH_SIZE>19.0</BATCH_SIZE>
    <BOIL_SIZE>25.0</BOIL_SIZE>
    <BOIL_TIME>60.0</BOIL_TIME>
    <EFFICIENCY>72.0</EFFICIENCY>
    <HOPS>
      <HOP>
        <NAME>Cascade</NAME>
        <VERSION>1</VERSION>
        <ALPHA>7.5</ALPHA>
        <AMOUNT>0.050</AMOUNT>
        <USE>Boil</USE>
        <TIME>60.0</TIME>
      </HOP>
    </HOPS>
    <FERMENTABLES>
      <FERMENTABLE>
        <NAME>Pale Malt</NAME>
        <VERSION>1</VERSION>
        <TYPE>Grain</TYPE>
        <AMOUNT>5.0</AMOUNT>
        <YIELD>80.0</YIELD>
        <COLOR>4.0</COLOR>
      </FERMENTABLE>
    </FERMENTABLES>
    <YEASTS>
      <YEAST>
        <NAME>US-05</NAME>
        <VERSION>1</VERSION>
        <TYPE>Ale</TYPE>
        <FORM>Dry</FORM>
        <ATTENUATION>77.0</ATTENUATION>
      </YEAST>
    </YEASTS>
    <STYLE>
      <NAME>American IPA</NAME>
      <CATEGORY>IPA</CATEGORY>
    </STYLE>
  </RECIPE>
</RECIPES>`
}
