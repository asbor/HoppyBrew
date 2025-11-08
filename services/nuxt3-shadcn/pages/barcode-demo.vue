<template>
  <div class="min-h-screen bg-background text-foreground p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Barcode Scanner Demo</h1>
      <p class="text-muted-foreground">Scan barcodes to look up or manage inventory items</p>
    </div>

    <!-- Scanner Section -->
    <div class="mb-8 bg-card rounded-lg border border-border p-6">
      <h2 class="text-xl font-semibold mb-4">Scan Item</h2>
      
      <BarcodeScanner
        button-text="Scan Barcode/QR Code"
        @scan-success="handleScanSuccess"
        @scan-error="handleScanError"
      />
    </div>

    <!-- Scanned Item Display -->
    <div v-if="scannedItem" class="mb-8 bg-card rounded-lg border border-border p-6">
      <h2 class="text-xl font-semibold mb-4">Scanned Item</h2>
      
      <div class="space-y-3">
        <div class="flex items-center gap-2">
          <span class="font-medium">Type:</span>
          <span class="px-2 py-1 bg-primary/10 text-primary rounded text-sm capitalize">
            {{ scannedItem.type }}
          </span>
        </div>
        
        <div>
          <span class="font-medium">Name:</span>
          <span class="ml-2">{{ scannedItem.item.name }}</span>
        </div>

        <div>
          <span class="font-medium">Barcode:</span>
          <span class="ml-2 font-mono">{{ scannedItem.item.barcode }}</span>
        </div>

        <div v-if="scannedItem.item.amount !== undefined">
          <span class="font-medium">Amount:</span>
          <span class="ml-2">{{ scannedItem.item.amount }}</span>
        </div>

        <div v-if="scannedItem.item.origin">
          <span class="font-medium">Origin:</span>
          <span class="ml-2">{{ scannedItem.item.origin }}</span>
        </div>

        <div v-if="scannedItem.item.notes">
          <span class="font-medium">Notes:</span>
          <span class="ml-2">{{ scannedItem.item.notes }}</span>
        </div>
      </div>

      <div class="mt-4 flex gap-2">
        <button
          @click="viewFullDetails"
          class="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
        >
          View Full Details
        </button>
        <button
          @click="scannedItem = null"
          class="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90"
        >
          Scan Another
        </button>
      </div>
    </div>

    <!-- Item Not Found -->
    <div v-if="itemNotFound" class="mb-8 bg-destructive/10 border border-destructive rounded-lg p-6">
      <h3 class="text-lg font-semibold text-destructive mb-2">Item Not Found</h3>
      <p class="text-destructive/80 mb-4">
        No inventory item found with barcode: <span class="font-mono">{{ lastScannedCode }}</span>
      </p>
      <button
        @click="itemNotFound = false"
        class="px-4 py-2 bg-destructive text-destructive-foreground rounded-lg hover:bg-destructive/90"
      >
        Dismiss
      </button>
    </div>

    <!-- Recent Scans -->
    <div v-if="recentScans.length > 0" class="bg-card rounded-lg border border-border p-6">
      <h2 class="text-xl font-semibold mb-4">Recent Scans</h2>
      
      <div class="space-y-2">
        <div
          v-for="(scan, index) in recentScans"
          :key="index"
          class="flex items-center justify-between p-3 bg-muted/50 rounded-lg"
        >
          <div>
            <div class="font-medium">{{ scan.item?.name || 'Unknown' }}</div>
            <div class="text-sm text-muted-foreground">
              {{ scan.code }} • {{ new Date(scan.timestamp).toLocaleTimeString() }}
            </div>
          </div>
          <div class="text-sm capitalize text-muted-foreground">
            {{ scan.type }}
          </div>
        </div>
      </div>
    </div>

    <!-- Instructions -->
    <div class="mt-8 bg-muted/30 rounded-lg p-6">
      <h3 class="text-lg font-semibold mb-3">How to Use</h3>
      <ol class="list-decimal list-inside space-y-2 text-muted-foreground">
        <li>Click "Scan Barcode/QR Code" to activate your camera</li>
        <li>Point your camera at a barcode or QR code</li>
        <li>The scanner will automatically detect and look up the item</li>
        <li>View item details or scan another item</li>
      </ol>
      
      <div class="mt-4 pt-4 border-t border-border">
        <p class="text-sm text-muted-foreground">
          <strong>Note:</strong> To test this feature, first assign barcodes to your inventory items 
          from the individual inventory pages (Hops, Fermentables, Yeasts, or Miscs).
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BarcodeScanner from '~/components/BarcodeScanner.vue'

const { lookupByBarcode } = useInventory()

const scannedItem = ref<any>(null)
const itemNotFound = ref(false)
const lastScannedCode = ref('')
const recentScans = ref<any[]>([])

const handleScanSuccess = async (scanResult: { code: string; format: string }) => {
  lastScannedCode.value = scanResult.code
  itemNotFound.value = false
  scannedItem.value = null

  console.log('Scanned:', scanResult)

  try {
    // Look up the item by barcode
    const response = await lookupByBarcode(scanResult.code)
    
    if (response.error.value) {
      // Item not found
      itemNotFound.value = true
    } else if (response.data.value) {
      // Item found
      scannedItem.value = response.data.value
      
      // Add to recent scans
      recentScans.value.unshift({
        ...response.data.value,
        code: scanResult.code,
        format: scanResult.format,
        timestamp: new Date().toISOString(),
      })
      
      // Keep only last 5 scans
      if (recentScans.value.length > 5) {
        recentScans.value.pop()
      }
    }
  } catch (error) {
    console.error('Error looking up barcode:', error)
    itemNotFound.value = true
  }
}

const handleScanError = (error: string) => {
  console.error('Scan error:', error)
}

const viewFullDetails = () => {
  if (!scannedItem.value) return
  
  // Navigate to the appropriate inventory page based on item type
  const routes: Record<string, string> = {
    hop: '/inventory/hops',
    fermentable: '/inventory/fermentables',
    yeast: '/inventory/yeasts',
    misc: '/inventory/miscs',
  }
  
  const route = routes[scannedItem.value.type]
  if (route) {
    navigateTo(route)
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
