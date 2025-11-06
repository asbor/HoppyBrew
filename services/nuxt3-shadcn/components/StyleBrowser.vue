<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useBeerStyles, type BeerStyle, type StyleGuidelineSource, type StyleCategory } from '~/composables/useBeerStyles'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const beerStylesApi = useBeerStyles()

// State
const loading = ref(false)
const error = ref<string | null>(null)
const guidelineSources = ref<StyleGuidelineSource[]>([])
const categories = ref<StyleCategory[]>([])
const styles = ref<BeerStyle[]>([])
const selectedGuideline = ref<number | null>(null)
const selectedCategory = ref<number | null>(null)
const searchQuery = ref('')

// Fetch guideline sources
const fetchGuidelineSources = async () => {
  loading.value = true
  const response = await beerStylesApi.getGuidelineSources(true)
  if (response.error.value) {
    error.value = response.error.value
  } else if (response.data.value) {
    guidelineSources.value = response.data.value
    // Auto-select first guideline if available
    if (guidelineSources.value.length > 0 && !selectedGuideline.value) {
      selectedGuideline.value = guidelineSources.value[0].id || null
    }
  }
  loading.value = response.loading.value
}

// Fetch categories for selected guideline
const fetchCategories = async (guidelineId: number) => {
  const response = await beerStylesApi.getCategories({ guideline_source_id: guidelineId })
  if (response.error.value) {
    error.value = response.error.value
  } else if (response.data.value) {
    categories.value = response.data.value
  }
}

// Fetch styles for selected guideline/category
const fetchStyles = async () => {
  loading.value = true
  const params: any = {}
  
  if (selectedGuideline.value) {
    params.guideline_source_id = selectedGuideline.value
  }
  
  if (selectedCategory.value) {
    params.category_id = selectedCategory.value
  }
  
  const response = searchQuery.value 
    ? await beerStylesApi.searchStyles({ query: searchQuery.value, ...params })
    : await beerStylesApi.getStyles(params)
    
  if (response.error.value) {
    error.value = response.error.value
  } else if (response.data.value) {
    styles.value = response.data.value
  }
  loading.value = response.loading.value
}

// Watchers
watch(selectedGuideline, (newVal) => {
  if (newVal) {
    fetchCategories(newVal)
    selectedCategory.value = null
    fetchStyles()
  }
})

watch(selectedCategory, () => {
  fetchStyles()
})

watch(searchQuery, () => {
  fetchStyles()
})

// Computed
const filteredCategories = computed(() => {
  return categories.value.filter(cat => !cat.parent_category_id)
})

// Format helpers
const formatRange = (min?: number, max?: number, unit: string = '') => {
  if (min === undefined && max === undefined) return 'N/A'
  if (min === max || max === undefined) return `${min}${unit}`
  if (min === undefined) return `${max}${unit}`
  return `${min}-${max}${unit}`
}

// Lifecycle
onMounted(() => {
  fetchGuidelineSources()
})
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Beer Style Browser</h2>
        <p class="text-muted-foreground">
          Browse and search beer styles from multiple guidelines
        </p>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="bg-destructive/15 text-destructive px-4 py-3 rounded-md">
      {{ error }}
    </div>

    <!-- Main Content -->
    <div class="grid gap-4 md:grid-cols-12">
      <!-- Sidebar - Guideline & Category Selection -->
      <Card class="md:col-span-3">
        <CardHeader>
          <CardTitle class="text-lg">Guidelines</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <!-- Guideline Sources -->
          <div class="space-y-2">
            <div 
              v-for="source in guidelineSources" 
              :key="source.id"
              @click="selectedGuideline = source.id || null"
              :class="[
                'p-2 rounded-md cursor-pointer transition-colors',
                selectedGuideline === source.id 
                  ? 'bg-primary text-primary-foreground' 
                  : 'hover:bg-muted'
              ]"
            >
              <div class="font-medium">{{ source.abbreviation || source.name }}</div>
              <div class="text-xs opacity-80">{{ source.year }}</div>
            </div>
          </div>

          <!-- Categories -->
          <div v-if="selectedGuideline" class="border-t pt-4">
            <h4 class="font-medium mb-2">Categories</h4>
            <ScrollArea class="h-[400px]">
              <div class="space-y-1">
                <div
                  @click="selectedCategory = null"
                  :class="[
                    'px-2 py-1.5 rounded-md cursor-pointer transition-colors text-sm',
                    selectedCategory === null
                      ? 'bg-secondary text-secondary-foreground'
                      : 'hover:bg-muted'
                  ]"
                >
                  All Categories
                </div>
                <div 
                  v-for="category in filteredCategories" 
                  :key="category.id"
                  @click="selectedCategory = category.id || null"
                  :class="[
                    'px-2 py-1.5 rounded-md cursor-pointer transition-colors text-sm',
                    selectedCategory === category.id
                      ? 'bg-secondary text-secondary-foreground'
                      : 'hover:bg-muted'
                  ]"
                >
                  <span class="font-medium">{{ category.code }}</span> {{ category.name }}
                </div>
              </div>
            </ScrollArea>
          </div>
        </CardContent>
      </Card>

      <!-- Main Content - Style List -->
      <div class="md:col-span-9 space-y-4">
        <!-- Search Bar -->
        <Card>
          <CardContent class="pt-6">
            <Input
              v-model="searchQuery"
              placeholder="Search styles by name, description, or examples..."
              class="w-full"
            />
          </CardContent>
        </Card>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <p class="text-muted-foreground">Loading styles...</p>
        </div>

        <!-- Styles Grid -->
        <div v-else-if="styles.length > 0" class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Card 
            v-for="style in styles" 
            :key="style.id"
            class="hover:shadow-md transition-shadow cursor-pointer"
          >
            <CardHeader>
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <CardTitle class="text-lg">{{ style.name }}</CardTitle>
                  <CardDescription>{{ style.style_code }}</CardDescription>
                </div>
                <Badge v-if="style.is_custom" variant="secondary">Custom</Badge>
              </div>
            </CardHeader>
            <CardContent class="space-y-2">
              <!-- Parameters -->
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span class="text-muted-foreground">ABV:</span>
                  <span class="ml-1 font-medium">{{ formatRange(style.abv_min, style.abv_max, '%') }}</span>
                </div>
                <div>
                  <span class="text-muted-foreground">IBU:</span>
                  <span class="ml-1 font-medium">{{ formatRange(style.ibu_min, style.ibu_max) }}</span>
                </div>
                <div>
                  <span class="text-muted-foreground">OG:</span>
                  <span class="ml-1 font-medium">{{ formatRange(style.og_min, style.og_max) }}</span>
                </div>
                <div>
                  <span class="text-muted-foreground">FG:</span>
                  <span class="ml-1 font-medium">{{ formatRange(style.fg_min, style.fg_max) }}</span>
                </div>
              </div>

              <!-- Color Bar -->
              <div v-if="style.color_min_srm !== undefined || style.color_max_srm !== undefined" class="pt-2">
                <div class="text-xs text-muted-foreground mb-1">
                  Color: {{ formatRange(style.color_min_srm, style.color_max_srm, ' SRM') }}
                </div>
                <div class="h-2 rounded-full bg-gradient-to-r from-yellow-200 via-amber-600 to-gray-900"></div>
              </div>

              <!-- Description Preview -->
              <p v-if="style.description" class="text-sm text-muted-foreground line-clamp-2 pt-2">
                {{ style.description }}
              </p>
            </CardContent>
          </Card>
        </div>

        <!-- Empty State -->
        <Card v-else>
          <CardContent class="py-12 text-center">
            <p class="text-muted-foreground">
              No styles found. Try adjusting your filters or search query.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
