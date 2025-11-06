/**
 * Utility composable for getting the API base URL from runtime config
 * Use this instead of hard-coding 'http://localhost:8000'
 */

export const useApiUrl = () => {
  const config = useRuntimeConfig()
  const baseUrl = config.public.API_URL || 'http://localhost:8000'
  
  // Remove trailing slash if present
  const apiUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
  
  return {
    /**
     * Base API URL (e.g., 'http://localhost:8000')
     */
    apiUrl,
    
    /**
     * Build a full API endpoint URL
     * @param path - API endpoint path (e.g., '/recipes' or 'recipes')
     * @returns Full URL (e.g., 'http://localhost:8000/recipes')
     */
    url: (path: string): string => {
      const cleanPath = path.startsWith('/') ? path : `/${path}`
      return `${apiUrl}${cleanPath}`
    }
  }
}
