/**
 * Centralized API Configuration
 * 
 * This composable provides a single source of truth for API configuration.
 * It handles environment detection and provides the correct API base URL
 * for different deployment scenarios (Docker, local development, production).
 * 
 * Usage:
 *   const { apiBaseUrl, buildUrl } = useApiConfig()
 *   const response = await fetch(buildUrl('/recipes'))
 */

export const useApiConfig = () => {
  const config = useRuntimeConfig()
  
  /**
   * Get the API base URL from runtime config
   * Falls back to localhost:8000 for local development
   */
  const getApiBaseUrl = (): string => {
    const baseUrl = config.public.API_URL || 'http://localhost:8000'
    // Remove trailing slash if present
    return baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
  }

  const apiBaseUrl = getApiBaseUrl()

  /**
   * Build a complete API URL from an endpoint path
   * @param path - API endpoint path (with or without leading slash)
   * @returns Complete URL to the API endpoint
   * 
   * @example
   * buildUrl('/recipes') // => 'http://localhost:8000/recipes'
   * buildUrl('batches/123') // => 'http://localhost:8000/batches/123'
   */
  const buildUrl = (path: string): string => {
    const cleanPath = path.startsWith('/') ? path : `/${path}`
    return `${apiBaseUrl}${cleanPath}`
  }

  /**
   * Check if the API is reachable
   * @returns Promise that resolves to true if API is healthy
   */
  const checkHealth = async (): Promise<boolean> => {
    try {
      const response = await fetch(buildUrl('/health'), {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      })
      return response.ok
    } catch (error) {
      console.error('API health check failed:', error)
      return false
    }
  }

  /**
   * Log current API configuration (useful for debugging)
   */
  const logConfig = () => {
    console.group('🔧 API Configuration')
    console.log('Base URL:', apiBaseUrl)
    console.log('Runtime Config API_URL:', config.public.API_URL)
    console.log('Environment:', process.env.NODE_ENV)
    console.groupEnd()
  }

  return {
    /** The configured API base URL */
    apiBaseUrl,
    /** Build a complete URL from a path */
    buildUrl,
    /** Check if API is healthy and reachable */
    checkHealth,
    /** Log current configuration for debugging */
    logConfig,
  }
}
