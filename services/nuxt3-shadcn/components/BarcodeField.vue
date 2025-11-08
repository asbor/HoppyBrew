<template>
  <div class="barcode-field">
    <div class="mb-4">
      <label class="block text-sm font-medium mb-2">
        Barcode / QR Code
      </label>
      
      <div class="flex gap-2">
        <input
          v-model="localBarcode"
          type="text"
          placeholder="Enter or scan barcode"
          class="flex-1 px-3 py-2 border border-input rounded-lg bg-background"
          :disabled="scanning"
        />
        
        <button
          @click="toggleScanner"
          :disabled="scanning"
          class="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 flex items-center gap-2"
          type="button"
        >
          <Icon v-if="!scanning" name="lucide:scan-line" class="w-4 h-4" />
          <Icon v-else name="lucide:loader-2" class="w-4 h-4 animate-spin" />
          {{ scanning ? 'Scanning...' : 'Scan' }}
        </button>
      </div>
      
      <p v-if="hint" class="text-sm text-muted-foreground mt-1">
        {{ hint }}
      </p>
    </div>

    <!-- Inline Scanner -->
    <div v-if="showScanner" class="mb-4">
      <BarcodeScanner
        button-text="Start Scanner"
        @scan-success="handleScanSuccess"
        @scan-error="handleScanError"
      />
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mb-4 p-3 bg-destructive/10 border border-destructive rounded-lg">
      <p class="text-sm text-destructive">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BarcodeScanner from './BarcodeScanner.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: 'Optional: Assign a unique barcode or QR code to this item'
  }
})

const emit = defineEmits(['update:modelValue'])

const localBarcode = ref(props.modelValue)
const showScanner = ref(false)
const scanning = ref(false)
const error = ref('')

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  localBarcode.value = newValue
})

// Watch for local changes and emit
watch(localBarcode, (newValue) => {
  emit('update:modelValue', newValue)
})

const toggleScanner = () => {
  showScanner.value = !showScanner.value
  error.value = ''
}

const handleScanSuccess = (scanResult: { code: string; format: string }) => {
  localBarcode.value = scanResult.code
  scanning.value = false
  showScanner.value = false
  error.value = ''
}

const handleScanError = (errorMessage: string) => {
  error.value = errorMessage
  scanning.value = false
}
</script>

<style scoped>
/* Additional styling if needed */
</style>
