/**
 * Batch Analytics composable
 * Handles fetching and managing batch analytics data
 */

import type { Ref } from 'vue'

export interface AnalyticsSummary {
  total_batches: number
  completed_batches: number
  success_rate: number
  avg_cost_per_batch: number
  avg_cost_per_liter: number
  avg_cost_per_pint: number
  avg_fermentation_days: number
  avg_og_accuracy: number
  avg_fg_accuracy: number
}

export interface BatchCost {
  batch_id: number
  batch_name: string
  total_cost: number
  cost_per_liter: number
  cost_per_pint: number
}

export interface FermentationTime {
  batch_id: number
  batch_name: string
  recipe_name: string
  duration_days: number
}

export interface OGFGAccuracy {
  batch_id: number
  batch_name: string
  estimated_og: number
  actual_og: number
  og_accuracy_percent: number
  estimated_fg: number
  actual_fg: number
  fg_accuracy_percent: number
}

export interface SeasonalPattern {
  season: string
  batch_count: number
  total_volume: number
}

export interface SuccessRate {
  recipe_name?: string
  recipe_id?: number
  style?: string
  total_batches: number
  completed_batches: number
  success_rate: number
}

export interface BatchAnalytics {
  summary: AnalyticsSummary
  cost_breakdown: BatchCost[]
  fermentation_times: FermentationTime[]
  og_fg_accuracy: OGFGAccuracy[]
  seasonal_patterns: SeasonalPattern[]
  success_by_recipe: SuccessRate[]
  success_by_style: SuccessRate[]
}

export interface AnalyticsFilters {
  start_date?: string
  end_date?: string
  recipe_id?: number
  style?: string
}

export const useBatchAnalytics = () => {
  const apiUrl = useApiUrl()
  const analytics: Ref<BatchAnalytics | null> = ref(null)
  const loading = ref(false)
  const error: Ref<string | null> = ref(null)

  /**
   * Fetch batch analytics with optional filters
   */
  const fetchAnalytics = async (filters: AnalyticsFilters = {}) => {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams()
      if (filters.start_date) params.append('start_date', filters.start_date)
      if (filters.end_date) params.append('end_date', filters.end_date)
      if (filters.recipe_id) params.append('recipe_id', filters.recipe_id.toString())
      if (filters.style) params.append('style', filters.style)

      const url = `${apiUrl.value}/analytics/batches/summary${params.toString() ? '?' + params.toString() : ''}`
      
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`Failed to fetch analytics: ${response.statusText}`)
      }

      analytics.value = await response.json()
      return { data: analytics.value, error: null }
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch analytics'
      console.error('Error fetching analytics:', e)
      return { data: null, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * Export analytics as CSV
   */
  const exportCSV = async (filters: AnalyticsFilters = {}) => {
    try {
      const params = new URLSearchParams()
      if (filters.start_date) params.append('start_date', filters.start_date)
      if (filters.end_date) params.append('end_date', filters.end_date)
      if (filters.recipe_id) params.append('recipe_id', filters.recipe_id.toString())
      if (filters.style) params.append('style', filters.style)

      const url = `${apiUrl.value}/analytics/batches/export/csv${params.toString() ? '?' + params.toString() : ''}`
      
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`Failed to export CSV: ${response.statusText}`)
      }

      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = `batch_analytics_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(downloadUrl)

      return { success: true, error: null }
    } catch (e: any) {
      const errorMsg = e.message || 'Failed to export CSV'
      console.error('Error exporting CSV:', e)
      return { success: false, error: errorMsg }
    }
  }

  /**
   * Get chart data for success rate by recipe
   */
  const getSuccessRateByRecipeChartData = computed(() => {
    if (!analytics.value) return null

    return {
      categories: analytics.value.success_by_recipe.map(r => r.recipe_name || 'Unknown'),
      series: [
        {
          name: 'Success Rate',
          data: analytics.value.success_by_recipe.map(r => r.success_rate),
        }
      ]
    }
  })

  /**
   * Get chart data for success rate by style
   */
  const getSuccessRateByStyleChartData = computed(() => {
    if (!analytics.value) return null

    return {
      categories: analytics.value.success_by_style.map(s => s.style || 'Unknown'),
      series: [
        {
          name: 'Success Rate',
          data: analytics.value.success_by_style.map(s => s.success_rate),
        }
      ]
    }
  })

  /**
   * Get chart data for seasonal brewing patterns
   */
  const getSeasonalPatternsChartData = computed(() => {
    if (!analytics.value) return null

    const seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    const data = seasons.map(season => {
      const pattern = analytics.value?.seasonal_patterns.find(p => p.season === season)
      return pattern ? pattern.batch_count : 0
    })

    return {
      categories: seasons,
      series: [
        {
          name: 'Batches Brewed',
          data: data,
        }
      ]
    }
  })

  /**
   * Get chart data for fermentation times
   */
  const getFermentationTimesChartData = computed(() => {
    if (!analytics.value) return null

    return {
      categories: analytics.value.fermentation_times.map(f => f.batch_name),
      series: [
        {
          name: 'Fermentation Days',
          data: analytics.value.fermentation_times.map(f => f.duration_days),
        }
      ]
    }
  })

  /**
   * Get chart data for cost breakdown
   */
  const getCostBreakdownChartData = computed(() => {
    if (!analytics.value) return null

    return {
      categories: analytics.value.cost_breakdown.map(c => c.batch_name),
      series: [
        {
          name: 'Cost per Batch',
          data: analytics.value.cost_breakdown.map(c => c.total_cost),
        },
        {
          name: 'Cost per Liter',
          data: analytics.value.cost_breakdown.map(c => c.cost_per_liter),
        }
      ]
    }
  })

  return {
    analytics: readonly(analytics),
    loading: readonly(loading),
    error: readonly(error),
    fetchAnalytics,
    exportCSV,
    getSuccessRateByRecipeChartData,
    getSuccessRateByStyleChartData,
    getSeasonalPatternsChartData,
    getFermentationTimesChartData,
    getCostBreakdownChartData,
  }
}
