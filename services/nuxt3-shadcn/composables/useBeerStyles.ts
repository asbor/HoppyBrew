/**
 * Beer Styles API composable
 * Provides methods for interacting with the beer styles management API
 */

export interface BeerStyle {
  id?: number
  guideline_source_id?: number
  category_id?: number
  name: string
  style_code?: string
  subcategory?: string
  
  // Basic Parameters
  abv_min?: number
  abv_max?: number
  og_min?: number
  og_max?: number
  fg_min?: number
  fg_max?: number
  ibu_min?: number
  ibu_max?: number
  color_min_ebc?: number
  color_max_ebc?: number
  color_min_srm?: number
  color_max_srm?: number
  
  // Descriptions
  description?: string
  aroma?: string
  appearance?: string
  flavor?: string
  mouthfeel?: string
  overall_impression?: string
  comments?: string
  history?: string
  ingredients?: string
  comparison?: string
  examples?: string
  
  is_custom?: boolean
  created_at?: string
  updated_at?: string
}

export interface StyleGuidelineSource {
  id?: number
  name: string
  year?: number
  abbreviation?: string
  description?: string
  is_active?: boolean
  created_at?: string
  updated_at?: string
}

export interface StyleCategory {
  id?: number
  guideline_source_id: number
  name: string
  code?: string
  description?: string
  parent_category_id?: number
}

export interface BeerStyleSearchParams {
  query?: string
  guideline_source_id?: number
  category_id?: number
  abv_min?: number
  abv_max?: number
  ibu_min?: number
  ibu_max?: number
  color_min_srm?: number
  color_max_srm?: number
  is_custom?: boolean
  limit?: number
  offset?: number
}

export const useBeerStyles = () => {
  const api = useApi()

  /**
   * Get all beer styles with optional filters
   */
  const getStyles = async (params?: {
    guideline_source_id?: number
    category_id?: number
    is_custom?: boolean
    limit?: number
    offset?: number
  }) => {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value))
        }
      })
    }
    const endpoint = `/beer-styles${queryParams.toString() ? '?' + queryParams.toString() : ''}`
    return api.get<BeerStyle[]>(endpoint)
  }

  /**
   * Search beer styles with advanced criteria
   */
  const searchStyles = async (params: BeerStyleSearchParams) => {
    const queryParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        queryParams.append(key, String(value))
      }
    })
    const endpoint = `/beer-styles/search?${queryParams.toString()}`
    return api.get<BeerStyle[]>(endpoint)
  }

  /**
   * Get a specific beer style by ID
   */
  const getStyle = async (id: number) => {
    return api.get<BeerStyle>(`/beer-styles/${id}`)
  }

  /**
   * Create a new custom beer style
   */
  const createStyle = async (style: Omit<BeerStyle, 'id' | 'created_at' | 'updated_at'>) => {
    return api.post<BeerStyle, typeof style>('/beer-styles', style)
  }

  /**
   * Update an existing custom beer style
   */
  const updateStyle = async (id: number, style: Partial<BeerStyle>) => {
    return api.put<BeerStyle, typeof style>(`/beer-styles/${id}`, style)
  }

  /**
   * Delete a custom beer style
   */
  const deleteStyle = async (id: number) => {
    return api.delete(`/beer-styles/${id}`)
  }

  /**
   * Get all style guideline sources
   */
  const getGuidelineSources = async (is_active?: boolean) => {
    const endpoint = is_active !== undefined 
      ? `/style-guideline-sources?is_active=${is_active}`
      : '/style-guideline-sources'
    return api.get<StyleGuidelineSource[]>(endpoint)
  }

  /**
   * Get a specific guideline source
   */
  const getGuidelineSource = async (id: number) => {
    return api.get<StyleGuidelineSource>(`/style-guideline-sources/${id}`)
  }

  /**
   * Create a new guideline source
   */
  const createGuidelineSource = async (source: Omit<StyleGuidelineSource, 'id' | 'created_at' | 'updated_at'>) => {
    return api.post<StyleGuidelineSource, typeof source>('/style-guideline-sources', source)
  }

  /**
   * Get all style categories
   */
  const getCategories = async (params?: {
    guideline_source_id?: number
    parent_category_id?: number
  }) => {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value))
        }
      })
    }
    const endpoint = `/style-categories${queryParams.toString() ? '?' + queryParams.toString() : ''}`
    return api.get<StyleCategory[]>(endpoint)
  }

  /**
   * Get a specific category
   */
  const getCategory = async (id: number) => {
    return api.get<StyleCategory>(`/style-categories/${id}`)
  }

  /**
   * Create a new category
   */
  const createCategory = async (category: Omit<StyleCategory, 'id'>) => {
    return api.post<StyleCategory, typeof category>('/style-categories', category)
  }

  return {
    // Beer Styles
    getStyles,
    searchStyles,
    getStyle,
    createStyle,
    updateStyle,
    deleteStyle,
    
    // Guideline Sources
    getGuidelineSources,
    getGuidelineSource,
    createGuidelineSource,
    
    // Categories
    getCategories,
    getCategory,
    createCategory,
  }
}
