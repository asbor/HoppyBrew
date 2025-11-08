import { ref } from 'vue'
import type { Ref } from 'vue'

export interface BrewStep {
  id: number
  batch_id: number
  step_name: string
  step_type: string
  duration: number | null
  temperature: number | null
  notes: string | null
  completed: boolean
  started_at: string | null
  completed_at: string | null
  created_at: string
  updated_at: string
  order_index: number
}

export interface BrewStepCreate {
  batch_id: number
  step_name: string
  step_type: string
  duration?: number
  temperature?: number
  notes?: string
  order_index?: number
}

export interface BrewStepUpdate {
  step_name?: string
  step_type?: string
  duration?: number
  temperature?: number
  notes?: string
  completed?: boolean
  started_at?: string
  completed_at?: string
  order_index?: number
}

export const useBrewSteps = () => {
  const apiUrl = useApiUrl()
  const loading = ref(false)
  const error: Ref<string | null> = ref(null)

  const createBrewSteps = async (batchId: number): Promise<BrewStep[]> => {
    loading.value = true
    error.value = null
    try {
      const response = await $fetch<BrewStep[]>(
        `${apiUrl}/batches/${batchId}/brew-steps`,
        {
          method: 'POST',
        }
      )
      return response
    } catch (e: any) {
      error.value = e.message || 'Failed to create brew steps'
      throw e
    } finally {
      loading.value = false
    }
  }

  const getBrewSteps = async (batchId: number): Promise<BrewStep[]> => {
    loading.value = true
    error.value = null
    try {
      const response = await $fetch<BrewStep[]>(
        `${apiUrl}/batches/${batchId}/brew-steps`,
        {
          method: 'GET',
        }
      )
      return response
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch brew steps'
      throw e
    } finally {
      loading.value = false
    }
  }

  const getBrewStep = async (stepId: number): Promise<BrewStep> => {
    loading.value = true
    error.value = null
    try {
      const response = await $fetch<BrewStep>(
        `${apiUrl}/brew-steps/${stepId}`,
        {
          method: 'GET',
        }
      )
      return response
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch brew step'
      throw e
    } finally {
      loading.value = false
    }
  }

  const updateBrewStep = async (
    stepId: number,
    update: BrewStepUpdate
  ): Promise<BrewStep> => {
    loading.value = true
    error.value = null
    try {
      const response = await $fetch<BrewStep>(
        `${apiUrl}/brew-steps/${stepId}`,
        {
          method: 'PATCH',
          body: update,
        }
      )
      return response
    } catch (e: any) {
      error.value = e.message || 'Failed to update brew step'
      throw e
    } finally {
      loading.value = false
    }
  }

  const deleteBrewStep = async (stepId: number): Promise<void> => {
    loading.value = true
    error.value = null
    try {
      await $fetch(`${apiUrl}/brew-steps/${stepId}`, {
        method: 'DELETE',
      })
    } catch (e: any) {
      error.value = e.message || 'Failed to delete brew step'
      throw e
    } finally {
      loading.value = false
    }
  }

  const startBrewDay = async (batchId: number): Promise<BrewStep> => {
    loading.value = true
    error.value = null
    try {
      const response = await $fetch<BrewStep>(
        `${apiUrl}/batches/${batchId}/brew-steps/start`,
        {
          method: 'POST',
        }
      )
      return response
    } catch (e: any) {
      error.value = e.message || 'Failed to start brew day'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    createBrewSteps,
    getBrewSteps,
    getBrewStep,
    updateBrewStep,
    deleteBrewStep,
    startBrewDay,
  }
}
