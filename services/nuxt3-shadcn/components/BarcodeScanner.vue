<template>
  <div class="barcode-scanner">
    <div v-if="!isScanning" class="scanner-controls">
      <button
        @click="startScanning"
        class="btn-primary flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        <Icon name="lucide:scan-line" class="w-5 h-5" />
        {{ buttonText }}
      </button>
    </div>

    <div v-if="isScanning" class="scanner-active">
      <div id="barcode-reader" class="barcode-reader"></div>
      
      <div class="scanner-actions mt-4 flex gap-2">
        <button
          @click="stopScanning"
          class="btn-secondary px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          <Icon name="lucide:x" class="w-5 h-5 inline mr-2" />
          Cancel
        </button>
      </div>
      
      <div v-if="lastScannedCode" class="scanned-result mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-sm text-green-800">
          <strong>Scanned:</strong> {{ lastScannedCode }}
        </p>
      </div>
    </div>

    <div v-if="error" class="error-message mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-sm text-red-800">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

const props = defineProps({
  buttonText: {
    type: String,
    default: 'Scan Barcode/QR Code'
  },
  // Supported formats: QR_CODE, UPC_A, UPC_E, EAN_8, EAN_13, CODE_128, etc.
  supportedFormats: {
    type: Array,
    default: () => [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] // All formats
  }
})

const emit = defineEmits(['scan-success', 'scan-error'])

const isScanning = ref(false)
const lastScannedCode = ref('')
const error = ref('')
let html5QrCode: Html5Qrcode | null = null

const startScanning = async () => {
  error.value = ''
  isScanning.value = true
  
  try {
    // Initialize scanner
    html5QrCode = new Html5Qrcode('barcode-reader')
    
    // Start scanning
    await html5QrCode.start(
      { facingMode: 'environment' }, // Use back camera on mobile
      {
        fps: 10, // Frame rate
        qrbox: { width: 250, height: 250 }, // Scanner box size
        formatsToSupport: props.supportedFormats
      },
      onScanSuccess,
      onScanFailure
    )
  } catch (err: any) {
    error.value = `Failed to start scanner: ${err.message || 'Unknown error'}`
    isScanning.value = false
    console.error('Scanner error:', err)
  }
}

const stopScanning = async () => {
  if (html5QrCode) {
    try {
      await html5QrCode.stop()
      html5QrCode.clear()
    } catch (err) {
      console.error('Error stopping scanner:', err)
    }
  }
  isScanning.value = false
  lastScannedCode.value = ''
}

const onScanSuccess = (decodedText: string, decodedResult: any) => {
  lastScannedCode.value = decodedText
  emit('scan-success', {
    code: decodedText,
    format: decodedResult.result.format?.formatName || 'unknown'
  })
  
  // Auto-stop after successful scan
  setTimeout(() => {
    stopScanning()
  }, 1000)
}

const onScanFailure = (errorMessage: string) => {
  // Scan failures are common and expected during scanning
  // We don't need to show these to the user
  // console.log('Scan failure:', errorMessage)
}

// Cleanup on unmount
onUnmounted(() => {
  if (isScanning.value) {
    stopScanning()
  }
})
</script>

<style scoped>
.barcode-scanner {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.barcode-reader {
  width: 100%;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.scanner-controls,
.scanner-actions {
  display: flex;
  justify-content: center;
}

.btn-primary,
.btn-secondary {
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
