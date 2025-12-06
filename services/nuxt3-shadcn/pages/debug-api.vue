<script setup lang="ts">
const { apiBaseUrl, buildUrl, checkHealth, logConfig } = useApiConfig()
const { get } = useApi()

const healthStatus = ref<any>(null)
const recipesTest = ref<any>(null)
const batchesTest = ref<any>(null)
const error = ref<string | null>(null)

// Log configuration on mount
onMounted(async () => {
  logConfig()
  
  try {
    // Test 1: Health check
    const isHealthy = await checkHealth()
    healthStatus.value = { ok: isHealthy, url: buildUrl('/health') }
    
    // Test 2: Recipes endpoint
    const { data: recipesData, error: recipesError } = await get('/recipes')
    recipesTest.value = {
      success: !recipesError.value,
      error: recipesError.value,
      count: recipesData.value?.length || 0,
      url: buildUrl('/recipes')
    }
    
    // Test 3: Batches endpoint
    const { data: batchesData, error: batchesError } = await get('/batches')
    batchesTest.value = {
      success: !batchesError.value,
      error: batchesError.value,
      count: batchesData.value?.length || 0,
      url: buildUrl('/batches')
    }
    
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  }
})
</script>

<template>
  <div class="container mx-auto p-8">
    <h1 class="text-3xl font-bold mb-6">API Debug Page</h1>
    
    <div class="space-y-6">
      <!-- Configuration -->
      <div class="border p-4 rounded bg-card text-card-foreground">
        <h2 class="text-xl font-bold mb-2">Configuration</h2>
        <p><strong>API Base URL:</strong> {{ apiBaseUrl }}</p>
        <p class="text-sm text-muted-foreground">Check browser console for full config</p>
      </div>
      
      <!-- Health Check -->
      <div
        class="border p-4 rounded"
        :class="healthStatus?.ok
          ? 'bg-green-50 text-slate-900 dark:bg-green-900/30 dark:text-green-50'
          : 'bg-red-50 text-slate-900 dark:bg-red-900/30 dark:text-red-50'"
      >
        <h2 class="text-xl font-bold mb-2">Health Check</h2>
        <p><strong>URL:</strong> {{ healthStatus?.url }}</p>
        <p><strong>Status:</strong> {{ healthStatus?.ok ? '✅ OK' : '❌ Failed' }}</p>
      </div>
      
      <!-- Recipes Test -->
      <div
        class="border p-4 rounded"
        :class="recipesTest?.success
          ? 'bg-green-50 text-slate-900 dark:bg-green-900/30 dark:text-green-50'
          : 'bg-red-50 text-slate-900 dark:bg-red-900/30 dark:text-red-50'"
      >
        <h2 class="text-xl font-bold mb-2">Recipes Endpoint</h2>
        <p><strong>URL:</strong> {{ recipesTest?.url }}</p>
        <p><strong>Status:</strong> {{ recipesTest?.success ? '✅ OK' : '❌ Failed' }}</p>
        <p><strong>Count:</strong> {{ recipesTest?.count }}</p>
        <p v-if="recipesTest?.error" class="text-red-600"><strong>Error:</strong> {{ recipesTest.error }}</p>
      </div>
      
      <!-- Batches Test -->
      <div
        class="border p-4 rounded"
        :class="batchesTest?.success
          ? 'bg-green-50 text-slate-900 dark:bg-green-900/30 dark:text-green-50'
          : 'bg-red-50 text-slate-900 dark:bg-red-900/30 dark:text-red-50'"
      >
        <h2 class="text-xl font-bold mb-2">Batches Endpoint</h2>
        <p><strong>URL:</strong> {{ batchesTest?.url }}</p>
        <p><strong>Status:</strong> {{ batchesTest?.success ? '✅ OK' : '❌ Failed' }}</p>
        <p><strong>Count:</strong> {{ batchesTest?.count }}</p>
        <p v-if="batchesTest?.error" class="text-red-600"><strong>Error:</strong> {{ batchesTest.error }}</p>
      </div>
      
      <!-- General Error -->
      <div v-if="error" class="border p-4 rounded bg-red-100 text-red-900 dark:bg-red-900/40 dark:text-red-50">
        <h2 class="text-xl font-bold mb-2">General Error</h2>
        <p class="text-red-600">{{ error }}</p>
      </div>
      
      <!-- Instructions -->
      <div class="border p-4 rounded bg-blue-50 text-slate-900 dark:bg-blue-900/30 dark:text-blue-50">
        <h2 class="text-xl font-bold mb-2">Instructions</h2>
        <ol class="list-decimal list-inside space-y-2">
          <li>Open browser DevTools (F12)</li>
          <li>Check Console tab for detailed logs</li>
          <li>Check Network tab for failed requests</li>
          <li>If all tests show ✅ OK, API connection is working</li>
          <li>If tests show ❌ Failed, check backend is running: <code>curl http://localhost:8000/health</code></li>
        </ol>
      </div>
    </div>
  </div>
</template>
