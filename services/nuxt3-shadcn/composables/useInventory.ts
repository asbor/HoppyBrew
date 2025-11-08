/**
 * Inventory management composable
 * Handles ingredient stock tracking for homebrewing
 */

export interface InventoryHop {
  id: string
  name: string
  alpha_acid: number
  amount: number
  unit: string
  type: string // pellet, leaf, plug
  form?: string
  use?: string
  origin?: string
  supplier?: string
  cost_per_unit?: number
  purchase_date?: string
  expiry_date?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface InventoryFermentable {
  id: string
  name: string
  type: string // grain, extract, sugar
  amount: number
  unit: string
  color: number // Lovibond or SRM
  yield_potential?: number
  supplier?: string
  cost_per_unit?: number
  origin?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface InventoryYeast {
  id: string
  name: string
  type: string // ale, lager, wild
  form: string // liquid, dry
  laboratory?: string
  product_id?: string
  amount: number
  unit: string
  min_temperature?: number
  max_temperature?: number
  attenuation?: number
  flocculation?: string
  supplier?: string
  cost_per_unit?: number
  manufacture_date?: string
  expiry_date?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface InventoryMisc {
  id: string
  name: string
  type: string // spice, fining, water agent, herb, flavor, other
  use: string // boil, mash, primary, secondary, bottling
  amount: number
  unit: string
  use_for?: string
  supplier?: string
  cost_per_unit?: number
  notes?: string
  created_at?: string
  updated_at?: string
}

export const useInventory = () => {
  const api = useApi()

  // Hops
  const hops = ref<InventoryHop[]>([])
  const hopsLoading = ref(false)
  const hopsError = ref<string | null>(null)

  async function fetchHops() {
    hopsLoading.value = true
    hopsError.value = null
    
    const response = await api.get<InventoryHop[]>('/inventory/hops')
    
    if (response.error.value) {
      hopsError.value = response.error.value
    } else {
      hops.value = response.data.value || []
    }
    
    hopsLoading.value = false
    return { data: hops, loading: hopsLoading, error: hopsError }
  }

  async function addHop(hopData: Partial<InventoryHop>) {
    hopsLoading.value = true
    const response = await api.post<InventoryHop>('/inventory/hops', hopData)
    
    if (!response.error.value && response.data.value) {
      hops.value.push(response.data.value)
    }
    
    hopsLoading.value = false
    return response
  }

  async function updateHop(id: string, hopData: Partial<InventoryHop>) {
    hopsLoading.value = true
    const response = await api.put<InventoryHop>(`/inventory/hops/${id}`, hopData)
    
    if (!response.error.value && response.data.value) {
      const index = hops.value.findIndex(h => h.id === id)
      if (index !== -1) hops.value[index] = response.data.value
    }
    
    hopsLoading.value = false
    return response
  }

  async function removeHop(id: string) {
    hopsLoading.value = true
    const response = await api.delete(`/inventory/hops/${id}`)
    
    if (!response.error.value) {
      hops.value = hops.value.filter(h => h.id !== id)
    }
    
    hopsLoading.value = false
    return response
  }

  // Fermentables
  const fermentables = ref<InventoryFermentable[]>([])
  const fermentablesLoading = ref(false)
  const fermentablesError = ref<string | null>(null)

  async function fetchFermentables() {
    fermentablesLoading.value = true
    fermentablesError.value = null
    
    const response = await api.get<InventoryFermentable[]>('/inventory/fermentables')
    
    if (response.error.value) {
      fermentablesError.value = response.error.value
    } else {
      fermentables.value = response.data.value || []
    }
    
    fermentablesLoading.value = false
    return { data: fermentables, loading: fermentablesLoading, error: fermentablesError }
  }

  async function addFermentable(fermentableData: Partial<InventoryFermentable>) {
    fermentablesLoading.value = true
    const response = await api.post<InventoryFermentable>('/inventory/fermentables', fermentableData)
    
    if (!response.error.value && response.data.value) {
      fermentables.value.push(response.data.value)
    }
    
    fermentablesLoading.value = false
    return response
  }

  async function updateFermentable(id: string, fermentableData: Partial<InventoryFermentable>) {
    fermentablesLoading.value = true
    const response = await api.put<InventoryFermentable>(`/inventory/fermentables/${id}`, fermentableData)
    
    if (!response.error.value && response.data.value) {
      const index = fermentables.value.findIndex(f => f.id === id)
      if (index !== -1) fermentables.value[index] = response.data.value
    }
    
    fermentablesLoading.value = false
    return response
  }

  async function removeFermentable(id: string) {
    fermentablesLoading.value = true
    const response = await api.delete(`/inventory/fermentables/${id}`)
    
    if (!response.error.value) {
      fermentables.value = fermentables.value.filter(f => f.id !== id)
    }
    
    fermentablesLoading.value = false
    return response
  }

  // Yeasts
  const yeasts = ref<InventoryYeast[]>([])
  const yeastsLoading = ref(false)
  const yeastsError = ref<string | null>(null)

  async function fetchYeasts() {
    yeastsLoading.value = true
    yeastsError.value = null
    
    const response = await api.get<InventoryYeast[]>('/inventory/yeasts')
    
    if (response.error.value) {
      yeastsError.value = response.error.value
    } else {
      yeasts.value = response.data.value || []
    }
    
    yeastsLoading.value = false
    return { data: yeasts, loading: yeastsLoading, error: yeastsError }
  }

  async function addYeast(yeastData: Partial<InventoryYeast>) {
    yeastsLoading.value = true
    const response = await api.post<InventoryYeast>('/inventory/yeasts', yeastData)
    
    if (!response.error.value && response.data.value) {
      yeasts.value.push(response.data.value)
    }
    
    yeastsLoading.value = false
    return response
  }

  async function updateYeast(id: string, yeastData: Partial<InventoryYeast>) {
    yeastsLoading.value = true
    const response = await api.put<InventoryYeast>(`/inventory/yeasts/${id}`, yeastData)
    
    if (!response.error.value && response.data.value) {
      const index = yeasts.value.findIndex(y => y.id === id)
      if (index !== -1) yeasts.value[index] = response.data.value
    }
    
    yeastsLoading.value = false
    return response
  }

  async function removeYeast(id: string) {
    yeastsLoading.value = true
    const response = await api.delete(`/inventory/yeasts/${id}`)
    
    if (!response.error.value) {
      yeasts.value = yeasts.value.filter(y => y.id !== id)
    }
    
    yeastsLoading.value = false
    return response
  }

  // Miscs
  const miscs = ref<InventoryMisc[]>([])
  const miscsLoading = ref(false)
  const miscsError = ref<string | null>(null)

  async function fetchMiscs() {
    miscsLoading.value = true
    miscsError.value = null
    
    const response = await api.get<InventoryMisc[]>('/inventory/miscs')
    
    if (response.error.value) {
      miscsError.value = response.error.value
    } else {
      miscs.value = response.data.value || []
    }
    
    miscsLoading.value = false
    return { data: miscs, loading: miscsLoading, error: miscsError }
  }

  async function addMisc(miscData: Partial<InventoryMisc>) {
    miscsLoading.value = true
    const response = await api.post<InventoryMisc>('/inventory/miscs', miscData)
    
    if (!response.error.value && response.data.value) {
      miscs.value.push(response.data.value)
    }
    
    miscsLoading.value = false
    return response
  }

  async function updateMisc(id: string, miscData: Partial<InventoryMisc>) {
    miscsLoading.value = true
    const response = await api.put<InventoryMisc>(`/inventory/miscs/${id}`, miscData)
    
    if (!response.error.value && response.data.value) {
      const index = miscs.value.findIndex(m => m.id === id)
      if (index !== -1) miscs.value[index] = response.data.value
    }
    
    miscsLoading.value = false
    return response
  }

  async function removeMisc(id: string) {
    miscsLoading.value = true
    const response = await api.delete(`/inventory/miscs/${id}`)
    
    if (!response.error.value) {
      miscs.value = miscs.value.filter(m => m.id !== id)
    }
    
    miscsLoading.value = false
    return response
  }

  // Get low stock items (amount < threshold)
  function getLowStockItems(threshold: number = 100) {
    const lowHops = hops.value.filter(h => h.amount < threshold)
    const lowFermentables = fermentables.value.filter(f => f.amount < threshold)
    const lowYeasts = yeasts.value.filter(y => y.amount < threshold)
    const lowMiscs = miscs.value.filter(m => m.amount < threshold)
    
    return {
      hops: lowHops,
      fermentables: lowFermentables,
      yeasts: lowYeasts,
      miscs: lowMiscs,
      total: lowHops.length + lowFermentables.length + lowYeasts.length + lowMiscs.length,
    }
  }

  // Check inventory availability for a recipe
  async function checkInventoryAvailability(recipeId: string) {
    const response = await api.get(`/batches/check-inventory-availability/${recipeId}`)
    return response
  }

  // Consume ingredients for a batch
  async function consumeIngredients(batchId: string, ingredients: any[]) {
    const response = await api.post(`/batches/${batchId}/consume-ingredients`, { ingredients })
    return response
  }

  // Get ingredient tracking for a batch
  async function getIngredientTracking(batchId: string) {
    const response = await api.get(`/batches/${batchId}/ingredient-tracking`)
    return response
  }

  // Barcode functions
  async function lookupByBarcode(barcode: string) {
    const response = await api.get(`/inventory/barcode/${barcode}`)
    return response
  }

  async function updateBarcode(itemType: string, itemId: string, barcode: string | null) {
    const response = await api.put(`/inventory/${itemType}/${itemId}/barcode`, null, {
      params: { barcode }
    })
    return response
  }

  return {
    // Hops
    hops,
    hopsLoading,
    hopsError,
    fetchHops,
    addHop,
    updateHop,
    removeHop,
    
    // Fermentables
    fermentables,
    fermentablesLoading,
    fermentablesError,
    fetchFermentables,
    addFermentable,
    updateFermentable,
    removeFermentable,
    
    // Yeasts
    yeasts,
    yeastsLoading,
    yeastsError,
    fetchYeasts,
    addYeast,
    updateYeast,
    removeYeast,
    
    // Miscs
    miscs,
    miscsLoading,
    miscsError,
    fetchMiscs,
    addMisc,
    updateMisc,
    removeMisc,
    
    // Utility
    getLowStockItems,
    checkInventoryAvailability,
    consumeIngredients,
    getIngredientTracking,
    
    // Barcode
    lookupByBarcode,
    updateBarcode,
  }
}
