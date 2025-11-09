// composables/useAnalytics.ts

import { ref } from 'vue'
import type { Ref } from 'vue'

export interface AnalyticsSummary {
  total_batches: number
  completed_batches: number
  active_batches: number
  total_recipes_used: number
  average_batch_size: number
  most_brewed_recipe: {
    id: number
    name: string
    count: number
  } | null
  most_brewed_style: {
    name: string
    count: number
  } | null
}

export interface SuccessRateByRecipe {
  recipe_id: number
  recipe_name: string
  style_name: string | null
  total_batches: number
  completed_batches: number
  success_rate: number
}

export interface CostAnalysis {
  batch_id: number
  batch_name: string
  recipe_name: string
  total_cost: number
  batch_size: number
  cost_per_liter: number
  cost_per_pint: number
}

export interface FermentationTimeTrend {
  batch_id: number
  batch_name: string
  recipe_name: string
  brew_date: string
  days_in_fermentation: number | null
  status: string
}

export interface OGFGAccuracy {
  batch_id: number
  batch_name: string
  recipe_name: string
  target_og: number | null
  actual_og: number | null
  target_fg: number | null
  actual_fg: number | null
  og_accuracy: number | null
  fg_accuracy: number | null
}

export interface SeasonalPattern {
  month: number
  month_name: string
  year: number
  batch_count: number
}

export function useAnalytics() {
  const apiUrl = useApiUrl()
  
  const summary: Ref<AnalyticsSummary | null> = ref(null)
  const successRates: Ref<SuccessRateByRecipe[]> = ref([])
  const costAnalysis: Ref<CostAnalysis[]> = ref([])
  const fermentationTrends: Ref<FermentationTimeTrend[]> = ref([])
  const ogFgAccuracy: Ref<OGFGAccuracy[]> = ref([])
  const seasonalPatterns: Ref<SeasonalPattern[]> = ref([])
  
  const loading = ref(false)
  const error: Ref<string | null> = ref(null)

  const buildQueryString = (params: Record<string, string | undefined>) => {
    const filtered = Object.entries(params)
      .filter(([_, value]) => value !== undefined && value !== '')
      .map(([key, value]) => `${key}=${encodeURIComponent(value!)}`)
      .join('&')
    return filtered ? `?${filtered}` : ''
  }

  const fetchSummary = async (startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const queryString = buildQueryString({ start_date: startDate, end_date: endDate })
      const response = await fetch(`${apiUrl}/analytics/summary${queryString}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      summary.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch summary'
      console.error('Error fetching analytics summary:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchSuccessRates = async (startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const queryString = buildQueryString({ start_date: startDate, end_date: endDate })
      const response = await fetch(`${apiUrl}/analytics/success-rate${queryString}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      successRates.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch success rates'
      console.error('Error fetching success rates:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchCostAnalysis = async (startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const queryString = buildQueryString({ start_date: startDate, end_date: endDate })
      const response = await fetch(`${apiUrl}/analytics/cost-analysis${queryString}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      costAnalysis.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch cost analysis'
      console.error('Error fetching cost analysis:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchFermentationTrends = async (startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const queryString = buildQueryString({ start_date: startDate, end_date: endDate })
      const response = await fetch(`${apiUrl}/analytics/fermentation-time${queryString}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      fermentationTrends.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch fermentation trends'
      console.error('Error fetching fermentation trends:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchOGFGAccuracy = async (startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const queryString = buildQueryString({ start_date: startDate, end_date: endDate })
      const response = await fetch(`${apiUrl}/analytics/og-fg-accuracy${queryString}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      ogFgAccuracy.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch OG/FG accuracy'
      console.error('Error fetching OG/FG accuracy:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchSeasonalPatterns = async (startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const queryString = buildQueryString({ start_date: startDate, end_date: endDate })
      const response = await fetch(`${apiUrl}/analytics/seasonal-patterns${queryString}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      seasonalPatterns.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch seasonal patterns'
      console.error('Error fetching seasonal patterns:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchAllAnalytics = async (startDate?: string, endDate?: string) => {
    await Promise.all([
      fetchSummary(startDate, endDate),
      fetchSuccessRates(startDate, endDate),
      fetchCostAnalysis(startDate, endDate),
      fetchFermentationTrends(startDate, endDate),
      fetchOGFGAccuracy(startDate, endDate),
      fetchSeasonalPatterns(startDate, endDate),
    ])
  }

  return {
    // State
    summary,
    successRates,
    costAnalysis,
    fermentationTrends,
    ogFgAccuracy,
    seasonalPatterns,
    loading,
    error,
    
    // Methods
    fetchSummary,
    fetchSuccessRates,
    fetchCostAnalysis,
    fetchFermentationTrends,
    fetchOGFGAccuracy,
    fetchSeasonalPatterns,
    fetchAllAnalytics,
  }
}
