<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Download, TrendingUp, DollarSign, Clock, Target, Calendar } from 'lucide-vue-next'

const {
  analytics,
  loading,
  error,
  fetchAnalytics,
  exportCSV,
  getSuccessRateByRecipeChartData,
  getSuccessRateByStyleChartData,
  getSeasonalPatternsChartData,
  getFermentationTimesChartData,
  getCostBreakdownChartData,
} = useBatchAnalytics()

// Filter state
const startDate = ref('')
const endDate = ref('')
const selectedRecipe = ref<number | undefined>(undefined)
const selectedStyle = ref('')

// Load recipes and styles for filters
const { recipes } = useRecipes()
const beerStyles = ref<string[]>([])

onMounted(async () => {
  // Set default date range (last 6 months)
  const now = new Date()
  const sixMonthsAgo = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate())
  startDate.value = sixMonthsAgo.toISOString().split('T')[0]
  endDate.value = now.toISOString().split('T')[0]

  // Fetch initial data
  await fetchAnalytics({
    start_date: startDate.value,
    end_date: endDate.value,
  })

  // Load recipes for filter
  await recipes.fetchAll?.()

  // Extract unique styles from analytics data
  if (analytics.value) {
    beerStyles.value = [...new Set(analytics.value.success_by_style.map(s => s.style || ''))].filter(Boolean)
  }
})

// Apply filters
const applyFilters = async () => {
  await fetchAnalytics({
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined,
    recipe_id: selectedRecipe.value,
    style: selectedStyle.value || undefined,
  })
}

// Clear filters
const clearFilters = () => {
  startDate.value = ''
  endDate.value = ''
  selectedRecipe.value = undefined
  selectedStyle.value = ''
  fetchAnalytics()
}

// Export data
const handleExportCSV = async () => {
  const result = await exportCSV({
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined,
    recipe_id: selectedRecipe.value,
    style: selectedStyle.value || undefined,
  })

  if (result.error) {
    alert(`Export failed: ${result.error}`)
  }
}

// Chart options for Highcharts
const barChartOptions = (title: string, categories: string[], series: any[]) => ({
  chart: { type: 'column' },
  title: { text: title },
  xAxis: { categories },
  yAxis: { title: { text: 'Percentage (%)' } },
  series,
  plotOptions: {
    column: {
      dataLabels: {
        enabled: true,
        format: '{y:.1f}%'
      }
    }
  }
})

const lineChartOptions = (title: string, categories: string[], series: any[]) => ({
  chart: { type: 'line' },
  title: { text: title },
  xAxis: { categories },
  yAxis: { title: { text: 'Days' } },
  series,
})

const columnChartOptions = (title: string, categories: string[], series: any[]) => ({
  chart: { type: 'column' },
  title: { text: title },
  xAxis: { categories },
  yAxis: { title: { text: 'Count' } },
  series,
})

const costChartOptions = (title: string, categories: string[], series: any[]) => ({
  chart: { type: 'column' },
  title: { text: title },
  xAxis: { categories },
  yAxis: { title: { text: 'Cost ($)' } },
  series,
})
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">Batch Analytics Dashboard</h1>
        <p class="text-muted-foreground">
          Comprehensive analytics for batch performance, costs, and trends
        </p>
      </div>
      <Button @click="handleExportCSV" :disabled="loading || !analytics">
        <Download class="w-4 h-4 mr-2" />
        Export CSV
      </Button>
    </div>

    <!-- Filters -->
    <Card>
      <CardHeader>
        <CardTitle>Filters</CardTitle>
        <CardDescription>Filter analytics by date range, recipe, or style</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="space-y-2">
            <Label for="start-date">Start Date</Label>
            <Input
              id="start-date"
              v-model="startDate"
              type="date"
              placeholder="Start date"
            />
          </div>
          <div class="space-y-2">
            <Label for="end-date">End Date</Label>
            <Input
              id="end-date"
              v-model="endDate"
              type="date"
              placeholder="End date"
            />
          </div>
          <div class="space-y-2">
            <Label for="recipe">Recipe</Label>
            <Select v-model="selectedRecipe">
              <SelectTrigger id="recipe">
                <SelectValue placeholder="All recipes" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem :value="undefined">All recipes</SelectItem>
                <SelectItem
                  v-for="recipe in recipes.value"
                  :key="recipe.id"
                  :value="recipe.id"
                >
                  {{ recipe.name }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="space-y-2">
            <Label for="style">Beer Style</Label>
            <Select v-model="selectedStyle">
              <SelectTrigger id="style">
                <SelectValue placeholder="All styles" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All styles</SelectItem>
                <SelectItem
                  v-for="style in beerStyles"
                  :key="style"
                  :value="style"
                >
                  {{ style }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        <div class="flex gap-2 mt-4">
          <Button @click="applyFilters" :disabled="loading">
            Apply Filters
          </Button>
          <Button variant="outline" @click="clearFilters" :disabled="loading">
            Clear
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>

    <!-- Error State -->
    <Card v-if="error && !loading" class="border-destructive">
      <CardContent class="pt-6">
        <p class="text-destructive">Error: {{ error }}</p>
      </CardContent>
    </Card>

    <!-- Analytics Content -->
    <div v-if="analytics && !loading" class="space-y-6">
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Total Batches</CardTitle>
            <TrendingUp class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ analytics.summary.total_batches }}</div>
            <p class="text-xs text-muted-foreground">
              {{ analytics.summary.completed_batches }} completed
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Success Rate</CardTitle>
            <Target class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ analytics.summary.success_rate.toFixed(1) }}%</div>
            <p class="text-xs text-muted-foreground">
              Batch completion rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Avg Cost per Batch</CardTitle>
            <DollarSign class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">${{ analytics.summary.avg_cost_per_batch.toFixed(2) }}</div>
            <p class="text-xs text-muted-foreground">
              ${{ analytics.summary.avg_cost_per_pint.toFixed(2) }} per pint
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">Avg Fermentation</CardTitle>
            <Clock class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ analytics.summary.avg_fermentation_days.toFixed(1) }}</div>
            <p class="text-xs text-muted-foreground">
              days average
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">OG Accuracy</CardTitle>
            <Target class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ analytics.summary.avg_og_accuracy.toFixed(1) }}%</div>
            <p class="text-xs text-muted-foreground">
              Original gravity accuracy
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">FG Accuracy</CardTitle>
            <Target class="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div class="text-2xl font-bold">{{ analytics.summary.avg_fg_accuracy.toFixed(1) }}%</div>
            <p class="text-xs text-muted-foreground">
              Final gravity accuracy
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- Charts -->
      <Tabs default-value="success-rate" class="space-y-4">
        <TabsList>
          <TabsTrigger value="success-rate">Success Rate</TabsTrigger>
          <TabsTrigger value="costs">Costs</TabsTrigger>
          <TabsTrigger value="fermentation">Fermentation</TabsTrigger>
          <TabsTrigger value="seasonal">Seasonal</TabsTrigger>
        </TabsList>

        <TabsContent value="success-rate" class="space-y-4">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card v-if="getSuccessRateByRecipeChartData">
              <CardHeader>
                <CardTitle>Success Rate by Recipe</CardTitle>
              </CardHeader>
              <CardContent>
                <highchart
                  :options="barChartOptions(
                    'Success Rate by Recipe',
                    getSuccessRateByRecipeChartData.categories,
                    getSuccessRateByRecipeChartData.series
                  )"
                />
              </CardContent>
            </Card>

            <Card v-if="getSuccessRateByStyleChartData">
              <CardHeader>
                <CardTitle>Success Rate by Style</CardTitle>
              </CardHeader>
              <CardContent>
                <highchart
                  :options="barChartOptions(
                    'Success Rate by Style',
                    getSuccessRateByStyleChartData.categories,
                    getSuccessRateByStyleChartData.series
                  )"
                />
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="costs" class="space-y-4">
          <Card v-if="getCostBreakdownChartData">
            <CardHeader>
              <CardTitle>Cost Breakdown</CardTitle>
              <CardDescription>Cost analysis per batch</CardDescription>
            </CardHeader>
            <CardContent>
              <highchart
                :options="costChartOptions(
                  'Batch Costs',
                  getCostBreakdownChartData.categories,
                  getCostBreakdownChartData.series
                )"
              />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="fermentation" class="space-y-4">
          <Card v-if="getFermentationTimesChartData">
            <CardHeader>
              <CardTitle>Fermentation Times</CardTitle>
              <CardDescription>Duration in days for each batch</CardDescription>
            </CardHeader>
            <CardContent>
              <highchart
                :options="lineChartOptions(
                  'Fermentation Duration',
                  getFermentationTimesChartData.categories,
                  getFermentationTimesChartData.series
                )"
              />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="seasonal" class="space-y-4">
          <Card v-if="getSeasonalPatternsChartData">
            <CardHeader>
              <CardTitle>Seasonal Brewing Patterns</CardTitle>
              <CardDescription>Batches brewed by season</CardDescription>
            </CardHeader>
            <CardContent>
              <highchart
                :options="columnChartOptions(
                  'Seasonal Patterns',
                  getSeasonalPatternsChartData.categories,
                  getSeasonalPatternsChartData.series
                )"
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>

    <!-- No Data State -->
    <Card v-if="!analytics && !loading && !error">
      <CardContent class="pt-6">
        <div class="text-center py-12">
          <Calendar class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold mb-2">No Analytics Data</h3>
          <p class="text-muted-foreground">
            No batch data available for the selected filters.
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
