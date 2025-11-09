<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
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
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const {
  summary,
  successRates,
  costAnalysis,
  fermentationTrends,
  ogFgAccuracy,
  seasonalPatterns,
  loading,
  error,
  fetchAllAnalytics,
} = useAnalytics()

// Date range filtering
const startDate = ref('')
const endDate = ref('')
const dateRangePreset = ref<string>('all')

// Apply date filter
const applyDateFilter = () => {
  fetchAllAnalytics(startDate.value || undefined, endDate.value || undefined)
}

// Preset date ranges
const applyPreset = (preset: string) => {
  dateRangePreset.value = preset
  const now = new Date()
  
  switch (preset) {
    case 'last30':
      startDate.value = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
      endDate.value = now.toISOString().split('T')[0]
      break
    case 'last90':
      startDate.value = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
      endDate.value = now.toISOString().split('T')[0]
      break
    case 'thisYear':
      startDate.value = new Date(now.getFullYear(), 0, 1).toISOString().split('T')[0]
      endDate.value = now.toISOString().split('T')[0]
      break
    case 'all':
      startDate.value = ''
      endDate.value = ''
      break
  }
  
  applyDateFilter()
}

// Export data as CSV
const exportCSV = (data: any[], filename: string) => {
  if (!data || data.length === 0) {
    alert('No data to export')
    return
  }
  
  const headers = Object.keys(data[0])
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(header => {
      const value = row[header]
      // Handle values that might contain commas
      if (typeof value === 'string' && value.includes(',')) {
        return `"${value}"`
      }
      return value ?? ''
    }).join(','))
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Charts data preparation
const successRateChartData = computed(() => {
  if (!successRates.value || successRates.value.length === 0) return []
  
  return successRates.value.slice(0, 10).map(item => ({
    name: item.recipe_name.length > 20 ? item.recipe_name.substring(0, 20) + '...' : item.recipe_name,
    successRate: item.success_rate,
    totalBatches: item.total_batches,
  }))
})

const seasonalChartData = computed(() => {
  if (!seasonalPatterns.value || seasonalPatterns.value.length === 0) return []
  
  return seasonalPatterns.value.map(item => ({
    month: `${item.month_name.substring(0, 3)} ${item.year}`,
    batchCount: item.batch_count,
  }))
})

const fermentationTimeStats = computed(() => {
  if (!fermentationTrends.value || fermentationTrends.value.length === 0) return null
  
  const completedWithTime = fermentationTrends.value.filter(f => f.days_in_fermentation !== null)
  if (completedWithTime.length === 0) return null
  
  const times = completedWithTime.map(f => f.days_in_fermentation!)
  const avg = times.reduce((a, b) => a + b, 0) / times.length
  const min = Math.min(...times)
  const max = Math.max(...times)
  
  return { avg: Math.round(avg), min, max }
})

const avgCostPerPint = computed(() => {
  if (!costAnalysis.value || costAnalysis.value.length === 0) return null
  
  const validCosts = costAnalysis.value.filter(c => c.cost_per_pint > 0)
  if (validCosts.length === 0) return null
  
  const avg = validCosts.reduce((sum, c) => sum + c.cost_per_pint, 0) / validCosts.length
  return avg.toFixed(2)
})

const avgOGAccuracy = computed(() => {
  if (!ogFgAccuracy.value || ogFgAccuracy.value.length === 0) return null
  
  const validAccuracies = ogFgAccuracy.value.filter(o => o.og_accuracy !== null)
  if (validAccuracies.length === 0) return null
  
  const avg = validAccuracies.reduce((sum, o) => sum + o.og_accuracy!, 0) / validAccuracies.length
  return avg.toFixed(1)
})

const avgFGAccuracy = computed(() => {
  if (!ogFgAccuracy.value || ogFgAccuracy.value.length === 0) return null
  
  const validAccuracies = ogFgAccuracy.value.filter(o => o.fg_accuracy !== null)
  if (validAccuracies.length === 0) return null
  
  const avg = validAccuracies.reduce((sum, o) => sum + o.fg_accuracy!, 0) / validAccuracies.length
  return avg.toFixed(1)
})

onMounted(() => {
  fetchAllAnalytics()
})
</script>

<template>
  <div class="container mx-auto py-6 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Batch Analytics Dashboard</h1>
        <p class="text-muted-foreground">
          Comprehensive insights into your brewing performance
        </p>
      </div>
    </div>

    <!-- Date Range Filter -->
    <Card>
      <CardHeader>
        <CardTitle>Filter by Date Range</CardTitle>
        <CardDescription>Select a time period to analyze</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="space-y-2">
            <Label for="startDate">Start Date</Label>
            <Input id="startDate" v-model="startDate" type="date" />
          </div>
          <div class="space-y-2">
            <Label for="endDate">End Date</Label>
            <Input id="endDate" v-model="endDate" type="date" />
          </div>
          <div class="space-y-2">
            <Label for="preset">Preset</Label>
            <Select v-model="dateRangePreset" @update:model-value="applyPreset">
              <SelectTrigger>
                <SelectValue placeholder="Select preset" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Time</SelectItem>
                <SelectItem value="last30">Last 30 Days</SelectItem>
                <SelectItem value="last90">Last 90 Days</SelectItem>
                <SelectItem value="thisYear">This Year</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="flex items-end">
            <Button @click="applyDateFilter" :disabled="loading" class="w-full">
              Apply Filter
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-muted-foreground">Loading analytics...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="text-center py-8">
      <p class="text-red-500">Error: {{ error }}</p>
    </div>

    <!-- Summary Cards -->
    <div v-if="summary" class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Total Batches</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ summary.total_batches }}</div>
          <p class="text-xs text-muted-foreground">
            {{ summary.active_batches }} active
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Completion Rate</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">
            {{ summary.total_batches > 0 
                ? Math.round((summary.completed_batches / summary.total_batches) * 100) 
                : 0 }}%
          </div>
          <p class="text-xs text-muted-foreground">
            {{ summary.completed_batches }} completed
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Avg Batch Size</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ summary.average_batch_size }} L</div>
          <p class="text-xs text-muted-foreground">
            {{ summary.total_recipes_used }} recipes used
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Avg Cost/Pint</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">
            {{ avgCostPerPint ? `$${avgCostPerPint}` : 'N/A' }}
          </div>
          <p class="text-xs text-muted-foreground">
            Based on ingredient costs
          </p>
        </CardContent>
      </Card>
    </div>

    <!-- Most Brewed -->
    <div v-if="summary" class="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Most Brewed Recipe</CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="summary.most_brewed_recipe">
            <p class="text-lg font-semibold">{{ summary.most_brewed_recipe.name }}</p>
            <p class="text-sm text-muted-foreground">
              Brewed {{ summary.most_brewed_recipe.count }} times
            </p>
          </div>
          <p v-else class="text-muted-foreground">No data available</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Most Brewed Style</CardTitle>
        </CardHeader>
        <CardContent>
          <div v-if="summary.most_brewed_style">
            <p class="text-lg font-semibold">{{ summary.most_brewed_style.name }}</p>
            <p class="text-sm text-muted-foreground">
              Brewed {{ summary.most_brewed_style.count }} times
            </p>
          </div>
          <p v-else class="text-muted-foreground">No data available</p>
        </CardContent>
      </Card>
    </div>

    <!-- Success Rate by Recipe -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Success Rate by Recipe</CardTitle>
            <CardDescription>Completion rate for each recipe</CardDescription>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            @click="exportCSV(successRates, 'success_rates')"
            :disabled="!successRates || successRates.length === 0"
          >
            Export CSV
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Table v-if="successRates && successRates.length > 0">
          <TableHeader>
            <TableRow>
              <TableHead>Recipe Name</TableHead>
              <TableHead>Style</TableHead>
              <TableHead class="text-right">Total Batches</TableHead>
              <TableHead class="text-right">Completed</TableHead>
              <TableHead class="text-right">Success Rate</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="rate in successRates" :key="rate.recipe_id">
              <TableCell class="font-medium">{{ rate.recipe_name }}</TableCell>
              <TableCell>{{ rate.style_name || 'N/A' }}</TableCell>
              <TableCell class="text-right">{{ rate.total_batches }}</TableCell>
              <TableCell class="text-right">{{ rate.completed_batches }}</TableCell>
              <TableCell class="text-right font-semibold">{{ rate.success_rate }}%</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center text-muted-foreground py-8">No data available</p>
      </CardContent>
    </Card>

    <!-- Cost Analysis -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Cost Analysis</CardTitle>
            <CardDescription>Batch costs breakdown</CardDescription>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            @click="exportCSV(costAnalysis, 'cost_analysis')"
            :disabled="!costAnalysis || costAnalysis.length === 0"
          >
            Export CSV
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Table v-if="costAnalysis && costAnalysis.length > 0">
          <TableHeader>
            <TableRow>
              <TableHead>Batch Name</TableHead>
              <TableHead>Recipe</TableHead>
              <TableHead class="text-right">Total Cost</TableHead>
              <TableHead class="text-right">Cost/Liter</TableHead>
              <TableHead class="text-right">Cost/Pint</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="cost in costAnalysis.slice(0, 10)" :key="cost.batch_id">
              <TableCell class="font-medium">{{ cost.batch_name }}</TableCell>
              <TableCell>{{ cost.recipe_name }}</TableCell>
              <TableCell class="text-right">${{ cost.total_cost.toFixed(2) }}</TableCell>
              <TableCell class="text-right">${{ cost.cost_per_liter.toFixed(2) }}</TableCell>
              <TableCell class="text-right">${{ cost.cost_per_pint.toFixed(2) }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center text-muted-foreground py-8">No cost data available</p>
      </CardContent>
    </Card>

    <!-- Fermentation Time Trends -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Fermentation Time Trends</CardTitle>
            <CardDescription>Days in fermentation for batches</CardDescription>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            @click="exportCSV(fermentationTrends, 'fermentation_trends')"
            :disabled="!fermentationTrends || fermentationTrends.length === 0"
          >
            Export CSV
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="fermentationTimeStats" class="grid grid-cols-3 gap-4 mb-4">
          <div class="text-center">
            <p class="text-sm text-muted-foreground">Average</p>
            <p class="text-2xl font-bold">{{ fermentationTimeStats.avg }} days</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-muted-foreground">Minimum</p>
            <p class="text-2xl font-bold">{{ fermentationTimeStats.min }} days</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-muted-foreground">Maximum</p>
            <p class="text-2xl font-bold">{{ fermentationTimeStats.max }} days</p>
          </div>
        </div>
        
        <Table v-if="fermentationTrends && fermentationTrends.length > 0">
          <TableHeader>
            <TableRow>
              <TableHead>Batch Name</TableHead>
              <TableHead>Recipe</TableHead>
              <TableHead>Status</TableHead>
              <TableHead class="text-right">Days in Fermentation</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="trend in fermentationTrends.slice(0, 10)" :key="trend.batch_id">
              <TableCell class="font-medium">{{ trend.batch_name }}</TableCell>
              <TableCell>{{ trend.recipe_name }}</TableCell>
              <TableCell>{{ trend.status }}</TableCell>
              <TableCell class="text-right">
                {{ trend.days_in_fermentation !== null ? `${trend.days_in_fermentation} days` : 'N/A' }}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center text-muted-foreground py-8">No fermentation data available</p>
      </CardContent>
    </Card>

    <!-- OG/FG Accuracy -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>OG/FG Accuracy</CardTitle>
            <CardDescription>How close actual gravity readings match targets</CardDescription>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            @click="exportCSV(ogFgAccuracy, 'og_fg_accuracy')"
            :disabled="!ogFgAccuracy || ogFgAccuracy.length === 0"
          >
            Export CSV
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="avgOGAccuracy || avgFGAccuracy" class="grid grid-cols-2 gap-4 mb-4">
          <div class="text-center">
            <p class="text-sm text-muted-foreground">Avg OG Accuracy</p>
            <p class="text-2xl font-bold">{{ avgOGAccuracy || 'N/A' }}%</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-muted-foreground">Avg FG Accuracy</p>
            <p class="text-2xl font-bold">{{ avgFGAccuracy || 'N/A' }}%</p>
          </div>
        </div>
        
        <Table v-if="ogFgAccuracy && ogFgAccuracy.length > 0">
          <TableHeader>
            <TableRow>
              <TableHead>Batch Name</TableHead>
              <TableHead class="text-right">Target OG</TableHead>
              <TableHead class="text-right">Actual OG</TableHead>
              <TableHead class="text-right">Target FG</TableHead>
              <TableHead class="text-right">Actual FG</TableHead>
              <TableHead class="text-right">OG Accuracy</TableHead>
              <TableHead class="text-right">FG Accuracy</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="accuracy in ogFgAccuracy.slice(0, 10)" :key="accuracy.batch_id">
              <TableCell class="font-medium">{{ accuracy.batch_name }}</TableCell>
              <TableCell class="text-right">{{ accuracy.target_og?.toFixed(3) || 'N/A' }}</TableCell>
              <TableCell class="text-right">{{ accuracy.actual_og?.toFixed(3) || 'N/A' }}</TableCell>
              <TableCell class="text-right">{{ accuracy.target_fg?.toFixed(3) || 'N/A' }}</TableCell>
              <TableCell class="text-right">{{ accuracy.actual_fg?.toFixed(3) || 'N/A' }}</TableCell>
              <TableCell class="text-right">{{ accuracy.og_accuracy?.toFixed(1) || 'N/A' }}%</TableCell>
              <TableCell class="text-right">{{ accuracy.fg_accuracy?.toFixed(1) || 'N/A' }}%</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center text-muted-foreground py-8">No gravity data available</p>
      </CardContent>
    </Card>

    <!-- Seasonal Patterns -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Seasonal Brewing Patterns</CardTitle>
            <CardDescription>Batch production by month</CardDescription>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            @click="exportCSV(seasonalPatterns, 'seasonal_patterns')"
            :disabled="!seasonalPatterns || seasonalPatterns.length === 0"
          >
            Export CSV
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Table v-if="seasonalPatterns && seasonalPatterns.length > 0">
          <TableHeader>
            <TableRow>
              <TableHead>Month</TableHead>
              <TableHead>Year</TableHead>
              <TableHead class="text-right">Batch Count</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="pattern in seasonalPatterns" :key="`${pattern.year}-${pattern.month}`">
              <TableCell class="font-medium">{{ pattern.month_name }}</TableCell>
              <TableCell>{{ pattern.year }}</TableCell>
              <TableCell class="text-right">{{ pattern.batch_count }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <p v-else class="text-center text-muted-foreground py-8">No seasonal data available</p>
      </CardContent>
    </Card>
  </div>
</template>
