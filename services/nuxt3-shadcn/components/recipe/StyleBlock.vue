<template>
  <div v-if="styleProfile || styleGuideline" class="bg-white rounded-lg border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Style Information</h3>
    
    <!-- Style Profile -->
    <div v-if="styleProfile" class="mb-4 p-4 bg-amber-50 rounded-lg">
      <h4 class="font-medium text-amber-900 mb-2">Style Profile</h4>
      <div class="space-y-2 text-sm">
        <div v-if="styleProfile.name">
          <span class="text-amber-700 font-medium">Style:</span>
          <span class="ml-2">{{ styleProfile.name }}</span>
        </div>
        <div v-if="styleProfile.category">
          <span class="text-amber-700 font-medium">Category:</span>
          <span class="ml-2">{{ styleProfile.category }}</span>
        </div>
        <div v-if="styleProfile.description" class="mt-3">
          <span class="text-amber-700 font-medium">Description:</span>
          <p class="mt-1 text-gray-700 leading-relaxed">{{ styleProfile.description }}</p>
        </div>
      </div>
    </div>

    <!-- Style Guidelines -->
    <div v-if="styleGuideline" class="p-4 bg-blue-50 rounded-lg">
      <h4 class="font-medium text-blue-900 mb-2">Style Guidelines</h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div v-if="styleGuideline.og_min || styleGuideline.og_max">
          <span class="text-blue-700 font-medium">OG Range:</span>
          <div class="text-gray-700">
            {{ formatRange(styleGuideline.og_min, styleGuideline.og_max, 'gravity') }}
          </div>
        </div>
        <div v-if="styleGuideline.fg_min || styleGuideline.fg_max">
          <span class="text-blue-700 font-medium">FG Range:</span>
          <div class="text-gray-700">
            {{ formatRange(styleGuideline.fg_min, styleGuideline.fg_max, 'gravity') }}
          </div>
        </div>
        <div v-if="styleGuideline.ibu_min || styleGuideline.ibu_max">
          <span class="text-blue-700 font-medium">IBU Range:</span>
          <div class="text-gray-700">
            {{ formatRange(styleGuideline.ibu_min, styleGuideline.ibu_max, 'number') }}
          </div>
        </div>
        <div v-if="styleGuideline.srm_min || styleGuideline.srm_max">
          <span class="text-blue-700 font-medium">SRM Range:</span>
          <div class="text-gray-700">
            {{ formatRange(styleGuideline.srm_min, styleGuideline.srm_max, 'number') }}
          </div>
        </div>
        <div v-if="styleGuideline.abv_min || styleGuideline.abv_max">
          <span class="text-blue-700 font-medium">ABV Range:</span>
          <div class="text-gray-700">
            {{ formatRange(styleGuideline.abv_min, styleGuideline.abv_max, 'percent') }}
          </div>
        </div>
      </div>
      
      <div v-if="styleGuideline.profile" class="mt-3">
        <span class="text-blue-700 font-medium">Profile:</span>
        <p class="mt-1 text-gray-700 text-sm leading-relaxed">{{ styleGuideline.profile }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface StyleProfile {
  name?: string
  category?: string
  description?: string
}

interface StyleGuideline {
  og_min?: number
  og_max?: number
  fg_min?: number
  fg_max?: number
  ibu_min?: number
  ibu_max?: number
  srm_min?: number
  srm_max?: number
  abv_min?: number
  abv_max?: number
  profile?: string
}

interface Props {
  styleProfile?: StyleProfile
  styleGuideline?: StyleGuideline
}

defineProps<Props>()

// Format range values
const formatRange = (min?: number, max?: number, type: 'gravity' | 'number' | 'percent' = 'number') => {
  if (!min && !max) return 'Not specified'
  
  if (min && max) {
    switch (type) {
      case 'gravity':
        return `${min.toFixed(3)} - ${max.toFixed(3)}`
      case 'percent':
        return `${min.toFixed(1)}% - ${max.toFixed(1)}%`
      default:
        return `${min.toFixed(0)} - ${max.toFixed(0)}`
    }
  } else if (min) {
    const prefix = type === 'percent' ? `${min.toFixed(1)}%` : min.toFixed(type === 'gravity' ? 3 : 0)
    return `${prefix}+`
  } else if (max) {
    const suffix = type === 'percent' ? `${max.toFixed(1)}%` : max.toFixed(type === 'gravity' ? 3 : 0)
    return `Up to ${suffix}`
  }
  
  return 'Not specified'
}
</script>