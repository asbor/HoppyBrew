/**
 * Recipe management composable
 * Handles all recipe CRUD operations with backend API
 */

export interface Recipe {
  id: string
  name: string
  type: string
  brewer?: string
  asst_brewer?: string
  batch_size: number
  boil_size: number
  boil_time: number
  efficiency: number
  notes?: string
  taste_notes?: string
  taste_rating?: number
  og?: number
  fg?: number
  est_og?: number
  est_fg?: number
  est_color?: number
  ibu?: number
  ibu_method?: string
  est_abv?: number
  abv?: number
  actual_efficiency?: number
  calories?: number
  fermentation_stages?: number
  primary_age?: number
  primary_temp?: number
  secondary_age?: number
  secondary_temp?: number
  tertiary_age?: number
  age?: number
  age_temp?: number
  carbonation_used?: string
  carbonation_date?: string
  display_batch_size?: string
  display_boil_size?: string
  display_og?: string
  display_fg?: string
  display_primary_temp?: string
  display_secondary_temp?: string
  display_tertiary_temp?: string
  display_age_temp?: string
  created_at?: string
  updated_at?: string
}

export interface RecipeCreate {
  name: string
  type: string
  batch_size: number
  boil_size: number
  boil_time: number
  efficiency: number
  brewer?: string
  notes?: string
  [key: string]: any
}

export const useRecipes = () => {
  const api = useApi()
  
  const recipes = ref<Recipe[]>([])
  const currentRecipe = ref<Recipe | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Fetch all recipes from backend
   */
  async function fetchAll() {
    loading.value = true
    error.value = null
    
    const response = await api.get<Recipe[]>('/recipes')
    
    if (response.error.value) {
      error.value = response.error.value
    } else {
      recipes.value = response.data.value || []
    }
    
    loading.value = false
    return { data: recipes, loading, error }
  }

  /**
   * Fetch single recipe by ID
   */
  async function fetchOne(id: string) {
    loading.value = true
    error.value = null
    
    const response = await api.get<Recipe>(`/recipes/${id}`)
    
    if (response.error.value) {
      error.value = response.error.value
    } else {
      currentRecipe.value = response.data.value
    }
    
    loading.value = false
    return { data: currentRecipe, loading, error }
  }

  /**
   * Create new recipe
   */
  async function create(recipeData: RecipeCreate) {
    loading.value = true
    error.value = null
    
    const response = await api.post<Recipe>('/recipes', recipeData)
    
    if (response.error.value) {
      error.value = response.error.value
      loading.value = false
      return { data: null, error }
    }
    
    // Add to local list
    if (response.data.value) {
      recipes.value.push(response.data.value)
    }
    
    loading.value = false
    return { data: response.data, error }
  }

  /**
   * Update existing recipe
   */
  async function update(id: string, recipeData: Partial<Recipe>) {
    loading.value = true
    error.value = null
    
    const response = await api.put<Recipe>(`/recipes/${id}`, recipeData)
    
    if (response.error.value) {
      error.value = response.error.value
      loading.value = false
      return { data: null, error }
    }
    
    // Update local list
    if (response.data.value) {
      const index = recipes.value.findIndex(r => r.id === id)
      if (index !== -1) {
        recipes.value[index] = response.data.value
      }
      currentRecipe.value = response.data.value
    }
    
    loading.value = false
    return { data: response.data, error }
  }

  /**
   * Delete recipe
   */
  async function remove(id: string) {
    loading.value = true
    error.value = null
    
    const response = await api.delete(`/recipes/${id}`)
    
    if (response.error.value) {
      error.value = response.error.value
      loading.value = false
      return { success: false, error }
    }
    
    // Remove from local list
    recipes.value = recipes.value.filter(r => r.id !== id)
    if (currentRecipe.value?.id === id) {
      currentRecipe.value = null
    }
    
    loading.value = false
    return { success: true, error: null }
  }

  return {
    recipes,
    currentRecipe,
    loading,
    error,
    fetchAll,
    fetchOne,
    create,
    update,
    remove,
  }
}
