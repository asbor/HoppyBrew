/**
 * Composable for batch status color coding
 * Following Home Assistant design system principles
 */

import type { BatchStatus } from './useBatches'

/**
 * Get Tailwind CSS color class for a batch status badge
 * Colors follow Home Assistant design system:
 * - Slate/Gray: inactive or planning states
 * - Amber/Yellow: warnings or active work in progress
 * - Sky/Blue: informational and active states
 * - Purple: special or unique states
 * - Emerald/Green: success and completed states
 */
export function getBatchStatusColor(status: BatchStatus | string): string {
  // Colors matching Home Assistant design system
  const colors: Record<string, string> = {
    // Standard batch statuses
    planning: 'bg-slate-500',        // Gray for planning/inactive
    brew_day: 'bg-amber-500',        // Amber for warning/in-progress
    primary_fermentation: 'bg-sky-500',     // Blue for active states
    secondary_fermentation: 'bg-blue-500',  // Deeper blue for secondary fermentation
    conditioning: 'bg-purple-500',   // Purple for special states
    packaged: 'bg-emerald-500',      // Green for success/completed
    completed: 'bg-green-600',       // Darker green for final completion
    archived: 'bg-gray-400',         // Light gray for archived
    
    // Alternative status names used in timeline component
    design: 'bg-slate-400',          // Gray for design/planning
    brewing: 'bg-amber-500',         // Amber for active brewing
    fermenting: 'bg-purple-500',     // Purple for fermentation
    packaging: 'bg-emerald-500',     // Green for packaging
    complete: 'bg-green-700',        // Dark green for completion
  }
  
  return colors[status] || 'bg-slate-500' // Default to slate for unknown statuses
}

export default function useStatusColors() {
  return {
    getBatchStatusColor,
  }
}
