import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useBatchAnalytics } from '@/composables/useBatchAnalytics'

// Mock fetch
global.fetch = vi.fn()

// Mock useApiUrl
vi.mock('@/composables/useApiUrl', () => ({
  default: () => ({
    value: 'http://localhost:8000'
  }),
  useApiUrl: () => ({
    value: 'http://localhost:8000'
  })
}))

describe('useBatchAnalytics', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize with null analytics', () => {
    const { analytics, loading, error } = useBatchAnalytics()
    
    expect(analytics.value).toBeNull()
    expect(loading.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('should fetch analytics successfully', async () => {
    const mockData = {
      summary: {
        total_batches: 10,
        completed_batches: 8,
        success_rate: 80,
        avg_cost_per_batch: 50,
        avg_cost_per_liter: 2.5,
        avg_cost_per_pint: 5,
        avg_fermentation_days: 14,
        avg_og_accuracy: 95,
        avg_fg_accuracy: 93
      },
      cost_breakdown: [],
      fermentation_times: [],
      og_fg_accuracy: [],
      seasonal_patterns: [],
      success_by_recipe: [],
      success_by_style: []
    }

    ;(global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    })

    const { analytics, fetchAnalytics } = useBatchAnalytics()
    const result = await fetchAnalytics()

    expect(result.data).toEqual(mockData)
    expect(result.error).toBeNull()
    expect(analytics.value).toEqual(mockData)
  })

  it('should handle fetch errors', async () => {
    ;(global.fetch as any).mockResolvedValueOnce({
      ok: false,
      statusText: 'Internal Server Error'
    })

    const { error, fetchAnalytics } = useBatchAnalytics()
    const result = await fetchAnalytics()

    expect(result.error).toBeTruthy()
    expect(error.value).toBeTruthy()
  })

  it('should apply filters when fetching analytics', async () => {
    const mockData = {
      summary: { total_batches: 5 },
      cost_breakdown: [],
      fermentation_times: [],
      og_fg_accuracy: [],
      seasonal_patterns: [],
      success_by_recipe: [],
      success_by_style: []
    }

    ;(global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    })

    const { fetchAnalytics } = useBatchAnalytics()
    await fetchAnalytics({
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      recipe_id: 1
    })

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('start_date=2024-01-01')
    )
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('end_date=2024-12-31')
    )
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('recipe_id=1')
    )
  })
})
