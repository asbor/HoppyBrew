<template>
  <Dialog v-model:open="isOpen">
    <DialogContent class="max-w-3xl">
      <DialogHeader>
        <DialogTitle>Generate Bottle Labels</DialogTitle>
        <DialogDescription>
          Create printable labels for your bottled batch
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-6">
        <!-- Label Preview -->
        <div class="border rounded-lg p-6 bg-white text-black" ref="labelPreview">
          <div class="space-y-4">
            <div class="text-center border-b pb-4">
              <h2 class="text-2xl font-bold">{{ batchName }}</h2>
              <p class="text-sm text-gray-600">Batch #{{ batchNumber }}</p>
            </div>

            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p class="font-semibold">Packaged:</p>
                <p>{{ formatDate(packagingDetails?.date) }}</p>
              </div>
              <div>
                <p class="font-semibold">ABV:</p>
                <p>{{ abv || 'N/A' }}%</p>
              </div>
              <div>
                <p class="font-semibold">Style:</p>
                <p>{{ style || 'N/A' }}</p>
              </div>
              <div>
                <p class="font-semibold">Volume:</p>
                <p>{{ volume || 'N/A' }}L</p>
              </div>
            </div>

            <div v-if="packagingDetails?.carbonation_method" class="border-t pt-4">
              <p class="text-xs text-gray-600">
                <span class="font-semibold">Carbonation:</span>
                {{ packagingDetails.volumes }} volumes CO2
                ({{ packagingDetails.carbonation_method }})
              </p>
            </div>

            <div v-if="notes" class="border-t pt-4">
              <p class="text-xs">
                <span class="font-semibold">Notes:</span> {{ notes }}
              </p>
            </div>

            <div class="text-center text-xs text-gray-500 pt-2 border-t">
              <p>Brewed with ❤️ by {{ brewer }}</p>
            </div>
          </div>
        </div>

        <!-- Label Options -->
        <Card>
          <CardHeader>
            <CardTitle>Label Options</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div>
              <Label for="label-count">Number of Labels</Label>
              <Input
                id="label-count"
                v-model.number="labelCount"
                type="number"
                min="1"
                :max="packagingDetails?.container_count || 100"
                placeholder="48"
              />
              <p class="text-sm text-muted-foreground mt-1">
                Maximum: {{ packagingDetails?.container_count || 'N/A' }} (container count)
              </p>
            </div>

            <div class="flex items-center space-x-2">
              <input
                type="checkbox"
                id="include-qr"
                v-model="includeQR"
                class="rounded"
              />
              <Label for="include-qr">Include QR code with batch details</Label>
            </div>

            <div class="flex items-center space-x-2">
              <input
                type="checkbox"
                id="include-date"
                v-model="includeDate"
                class="rounded"
                checked
              />
              <Label for="include-date">Include packaging date</Label>
            </div>
          </CardContent>
        </Card>
      </div>

      <DialogFooter class="flex gap-2">
        <Button @click="closeDialog" variant="ghost">Cancel</Button>
        <Button @click="downloadLabels" variant="outline">
          <Icon name="mdi:download" class="mr-2 h-4 w-4" />
          Download PDF
        </Button>
        <Button @click="printLabels">
          <Icon name="mdi:printer" class="mr-2 h-4 w-4" />
          Print Labels
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Icon } from '#components'

const props = defineProps<{
  open: boolean
  batchId: number
  batchName: string
  batchNumber: number
  brewer: string
  packagingDetails: any
  abv?: number
  style?: string
  volume?: number
  notes?: string
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value)
})

const labelPreview = ref<HTMLElement | null>(null)
const labelCount = ref(props.packagingDetails?.container_count || 48)
const includeQR = ref(false)
const includeDate = ref(true)

const formatDate = (dateStr: string | undefined) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const closeDialog = () => {
  isOpen.value = false
}

const printLabels = () => {
  // Create a print window with multiple labels
  const printContent = generateLabelHTML()
  const printWindow = window.open('', '', 'width=800,height=600')
  
  if (printWindow) {
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>Beer Labels - ${props.batchName}</title>
          <style>
            @page {
              size: letter;
              margin: 0.5in;
            }
            body {
              font-family: Arial, sans-serif;
              margin: 0;
              padding: 0;
            }
            .label {
              width: 3.5in;
              height: 2.5in;
              border: 1px solid #ccc;
              padding: 0.25in;
              margin: 0.25in;
              page-break-inside: avoid;
              float: left;
              box-sizing: border-box;
            }
            .label h2 {
              font-size: 16pt;
              margin: 0 0 4pt 0;
              border-bottom: 1px solid #000;
              padding-bottom: 4pt;
            }
            .label .batch-number {
              font-size: 9pt;
              color: #666;
              margin-bottom: 8pt;
            }
            .label .details {
              font-size: 9pt;
              margin-bottom: 8pt;
            }
            .label .footer {
              font-size: 8pt;
              color: #888;
              border-top: 1px solid #ccc;
              padding-top: 4pt;
              margin-top: 4pt;
            }
            @media print {
              .label {
                border: 1px solid #000;
              }
            }
          </style>
        </head>
        <body>
          ${printContent}
        </body>
      </html>
    `)
    printWindow.document.close()
    
    // Wait for content to load before printing
    setTimeout(() => {
      printWindow.print()
      printWindow.close()
    }, 500)
  }
}

const generateLabelHTML = () => {
  let html = ''
  
  for (let i = 0; i < labelCount.value; i++) {
    html += `
      <div class="label">
        <h2>${props.batchName}</h2>
        <div class="batch-number">Batch #${props.batchNumber}</div>
        <div class="details">
          ${includeDate.value ? `<div>Packaged: ${formatDate(props.packagingDetails?.date)}</div>` : ''}
          ${props.abv ? `<div>ABV: ${props.abv}%</div>` : ''}
          ${props.style ? `<div>Style: ${props.style}</div>` : ''}
          ${props.volume ? `<div>Volume: ${props.volume}L</div>` : ''}
          ${props.packagingDetails?.volumes ? `<div>CO2: ${props.packagingDetails.volumes} vol</div>` : ''}
        </div>
        <div class="footer">
          Brewed by ${props.brewer}
        </div>
      </div>
    `
  }
  
  return html
}

const downloadLabels = () => {
  // In a real implementation, this would use a library like jsPDF
  // For now, we'll trigger the print dialog which allows "Save as PDF"
  alert('Use your browser\'s print dialog and select "Save as PDF" to download the labels.')
  printLabels()
}
</script>
