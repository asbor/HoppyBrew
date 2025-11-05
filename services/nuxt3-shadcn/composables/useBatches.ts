/**
 * Batch management composable
 * Handles brewing batch lifecycle and fermentation tracking
 */

export type BatchStatus = 
  | 'planning'
  | 'brew_day'
  | 'primary_fermentation'
  | 'secondary_fermentation'
  | 'conditioning'
  | 'packaged'
  | 'completed'
  | 'archived'

export interface Batch {
  id: string
  recipe_id: string
  batch_name: string
  batch_number?: string
  batch_size: number
  boil_size?: number
  status: BatchStatus
  brew_date?: string
  fermentation_start_date?: string
  packaging_date?: string
  completion_date?: string
  og?: number
  fg?: number
  abv?: number
  ibu?: number
  srm_color?: number
  notes?: string
  created_at: string
  updated_at?: string
}

export interface BatchCreate {
  recipe_id: string
  batch_name: string
  batch_size: number
  brew_date?: string
  notes?: string
  [key: string]: any
}

export interface BatchReading {
  id?: string
  batch_id: string
  reading_date: string
  gravity: number
  temperature: number
  ph?: number
  notes?: string
}

export const useBatches = () => {
  const api = useApi()
  
  const batches = ref<Batch[]>([])
  const currentBatch = ref<Batch | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Fetch all batches from backend
   */
  async function fetchAll() {
    loading.value = true
    error.value = null
    
    const response = await api.get<Batch[]>('/batches')
    
    if (response.error.value) {
      error.value = response.error.value
    } else {
      batches.value = response.data.value || []
    }
    
    loading.value = false
    return { data: batches, loading, error }
  }

  /**
   * Fetch single batch by ID
   */
  async function fetchOne(id: string) {
    loading.value = true
    error.value = null
    
    const response = await api.get<Batch>(`/batches/${id}`)
    
    if (response.error.value) {
      error.value = response.error.value
    } else {
      currentBatch.value = response.data.value
    }
    
    loading.value = false
    return { data: currentBatch, loading, error }
  }

  /**
   * Create new batch from recipe
   */
  async function create(batchData: BatchCreate) {
    loading.value = true
    error.value = null
    
    const response = await api.post<Batch>('/batches', batchData)
    
    if (response.error.value) {
      error.value = response.error.value
      loading.value = false
      return { data: null, error }
    }
    
    if (response.data.value) {
      batches.value.push(response.data.value)
    }
    
    loading.value = false
    return { data: response.data, error }
  }

  /**
   * Update batch details
   */
  async function update(id: string, batchData: Partial<Batch>) {
    loading.value = true
    error.value = null
    
    const response = await api.put<Batch>(`/batches/${id}`, batchData)
    
    if (response.error.value) {
      error.value = response.error.value
      loading.value = false
      return { data: null, error }
    }
    
    if (response.data.value) {
      const index = batches.value.findIndex(b => b.id === id)
      if (index !== -1) {
        batches.value[index] = response.data.value
      }
      currentBatch.value = response.data.value
    }
    
    loading.value = false
    return { data: response.data, error }
  }

  /**
   * Update batch status (workflow progression)
   */
  async function updateStatus(id: string, newStatus: BatchStatus) {
    return update(id, { status: newStatus })
  }

  /**
   * Delete batch
   */
  async function remove(id: string) {
    loading.value = true
    error.value = null
    
    const response = await api.delete(`/batches/${id}`)
    
    if (response.error.value) {
      error.value = response.error.value
      loading.value = false
      return { success: false, error }
    }
    
    batches.value = batches.value.filter(b => b.id !== id)
    if (currentBatch.value?.id === id) {
      currentBatch.value = null
    }
    
    loading.value = false
    return { success: true, error: null }
  }

  /**
   * Get active batches (in fermentation/conditioning)
   */
  function getActiveBatches() {
    return batches.value.filter(b => 
      ['brew_day', 'primary_fermentation', 'secondary_fermentation', 'conditioning'].includes(b.status)
    )
  }

  /**
   * Get batches by status
   */
  function getBatchesByStatus(status: BatchStatus) {
    return batches.value.filter(b => b.status === status)
  }

  return {
    batches,
    currentBatch,
    loading,
    error,
    fetchAll,
    fetchOne,
    create,
    update,
    updateStatus,
    remove,
    getActiveBatches,
    getBatchesByStatus,
  }
}
