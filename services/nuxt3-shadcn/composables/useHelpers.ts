/**
 * Helper utilities for common operations
 */
export default function useHelpers() {
  let loading = ref(false);
  let open = ref(false);
  
  return {
    loading,
    open,
  };
}

/**
 * Format utilities for consistent formatting across the app
 */
export function useFormatters() {
  /**
   * Generate a batch name from a recipe name and current date
   */
  function generateBatchName(recipeName: string): string {
    const date = new Date().toLocaleDateString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
    return `${recipeName} - ${date}`
  }

  /**
   * Format a date string consistently
   */
  function formatDate(dateString: string | undefined, locale: string = 'en-GB'): string {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString(locale, {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  /**
   * Format a number with specified decimal places
   */
  function formatNumber(value: number | undefined | null, decimals: number = 1): string {
    if (value === undefined || value === null) return 'N/A'
    return value.toFixed(decimals)
  }

  return {
    generateBatchName,
    formatDate,
    formatNumber
  }
}
