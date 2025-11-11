/**
 * Base API composable for HoppyBrew backend communication
 * Provides consistent error handling, loading states, and request management
 */

interface ApiResponse<T> {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<string | null>
}

export const useApi = () => {
  const { apiBaseUrl } = useApiConfig()
  const API_BASE_URL = apiBaseUrl

  /**
   * Generic GET request
   */
  async function get<T>(endpoint: string): Promise<ApiResponse<T>> {
    const data = ref<T | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      data.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error occurred'
      console.error(`API GET ${endpoint} failed:`, e)
    } finally {
      loading.value = false
    }

    return { data, loading, error }
  }

  /**
   * Generic POST request
   */
  async function post<T, D = any>(endpoint: string, body: D): Promise<ApiResponse<T>> {
    const data = ref<T | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }

      data.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error occurred'
      console.error(`API POST ${endpoint} failed:`, e)
    } finally {
      loading.value = false
    }

    return { data, loading, error }
  }

  /**
   * Generic PUT request
   */
  async function put<T, D = any>(endpoint: string, body: D): Promise<ApiResponse<T>> {
    const data = ref<T | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }

      data.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error occurred'
      console.error(`API PUT ${endpoint} failed:`, e)
    } finally {
      loading.value = false
    }

    return { data, loading, error }
  }

  /**
   * Generic DELETE request
   */
  async function del<T>(endpoint: string): Promise<ApiResponse<T>> {
    const data = ref<T | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      // DELETE may return 204 No Content or a response body
      if (response.status !== 204) {
        data.value = await response.json()
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error occurred'
      console.error(`API DELETE ${endpoint} failed:`, e)
    } finally {
      loading.value = false
    }

    return { data, loading, error }
  }

  return {
    get,
    post,
    put,
    delete: del,
  }
}
