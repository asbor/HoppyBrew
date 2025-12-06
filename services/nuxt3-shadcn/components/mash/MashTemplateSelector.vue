<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card'
import { Button } from '~/components/ui/button'
import { Badge } from '~/components/ui/badge'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'

// Emits
const emit = defineEmits<{
  'template-selected': [template: MashTemplate, customName: string]
  'close': []
}>()

// Types
interface MashTemplate {
  id: string
  name: string
  description: string
  grain_temp: number
  tun_temp: number
  sparge_temp: number
  ph: number
  notes: string
  steps: any[]
}

// State
const templates = ref<MashTemplate[]>([])
const selectedTemplate = ref<MashTemplate | null>(null)
const customName = ref('')
const loading = ref(false)
const error = ref('')

// Fetch templates
const fetchTemplates = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await fetch('http://localhost:8000/mash/templates/list', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch templates')
    }
    
    const data = await response.json()
    templates.value = data
  } catch (err: any) {
    error.value = err.message || 'Failed to load templates'
    console.error('Error fetching templates:', err)
  } finally {
    loading.value = false
  }
}

// Select template
const selectTemplate = (template: MashTemplate) => {
  selectedTemplate.value = template
  customName.value = template.name
}

// Use template
const useTemplate = () => {
  if (!selectedTemplate.value) {
    alert('Please select a template')
    return
  }
  
  if (!customName.value.trim()) {
    alert('Please provide a name for your mash profile')
    return
  }
  
  emit('template-selected', selectedTemplate.value, customName.value.trim())
}

// Get badge color for step count
const getStepCountColor = (count: number) => {
  if (count <= 2) return 'bg-green-100 text-green-800'
  if (count <= 3) return 'bg-blue-100 text-blue-800'
  return 'bg-purple-100 text-purple-800'
}

onMounted(() => {
  fetchTemplates()
})
</script>

<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <Card class="max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <CardHeader>
        <div class="flex justify-between items-start">
          <div>
            <CardTitle>Choose Mash Profile Template</CardTitle>
            <CardDescription>
              Start with a pre-configured mash profile and customize it to your needs
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" @click="$emit('close')">✕</Button>
        </div>
      </CardHeader>
      
      <CardContent class="space-y-6">
        <!-- Loading state -->
        <div v-if="loading" class="text-center py-8">
          <p class="text-muted-foreground">Loading templates...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="text-center py-8">
          <p class="text-destructive">{{ error }}</p>
          <Button class="mt-4" variant="outline" @click="fetchTemplates">Retry</Button>
        </div>

        <!-- Templates list -->
        <div v-else class="space-y-4">
          <!-- Skip template option -->
          <Card 
            class="cursor-pointer transition-all hover:shadow-md border-2"
            :class="selectedTemplate === null ? 'border-primary' : 'border-transparent'"
            @click="selectedTemplate = null"
          >
            <CardContent class="pt-6">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-semibold text-lg">Start from Scratch</h4>
                  <p class="text-sm text-muted-foreground mt-1">
                    Create a custom mash profile without using a template
                  </p>
                </div>
                <div v-if="selectedTemplate === null" class="text-primary">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Template cards -->
          <Card 
            v-for="template in templates" 
            :key="template.id"
            class="cursor-pointer transition-all hover:shadow-md border-2"
            :class="selectedTemplate?.id === template.id ? 'border-primary' : 'border-transparent'"
            @click="selectTemplate(template)"
          >
            <CardContent class="pt-6">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-2">
                    <h4 class="font-semibold text-lg">{{ template.name }}</h4>
                    <Badge :class="getStepCountColor(template.steps.length)">
                      {{ template.steps.length }} steps
                    </Badge>
                  </div>
                  
                  <p class="text-sm text-muted-foreground mb-3">
                    {{ template.description }}
                  </p>

                  <!-- Template stats -->
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div>
                      <span class="text-muted-foreground">Sparge:</span>
                      <span class="font-semibold ml-1">{{ template.sparge_temp }}°C</span>
                    </div>
                    <div>
                      <span class="text-muted-foreground">pH:</span>
                      <span class="font-semibold ml-1">{{ template.ph }}</span>
                    </div>
                    <div>
                      <span class="text-muted-foreground">Grain Temp:</span>
                      <span class="font-semibold ml-1">{{ template.grain_temp }}°C</span>
                    </div>
                    <div>
                      <span class="text-muted-foreground">Total Time:</span>
                      <span class="font-semibold ml-1">
                        {{ template.steps.reduce((sum, s) => sum + (s.step_time || 0) + (s.ramp_time || 0), 0) }} min
                      </span>
                    </div>
                  </div>

                  <!-- Step preview -->
                  <div class="mt-3 space-y-1">
                    <p class="text-xs font-semibold text-muted-foreground uppercase">Steps:</p>
                    <div class="space-y-1">
                      <div 
                        v-for="(step, idx) in template.steps" 
                        :key="idx"
                        class="text-xs flex items-center gap-2"
                      >
                        <span class="font-mono text-muted-foreground">{{ idx + 1 }}.</span>
                        <span>{{ step.name }}</span>
                        <Badge variant="outline" class="text-xs px-1 py-0">{{ step.type }}</Badge>
                        <span class="text-muted-foreground">{{ step.step_temp }}°C / {{ step.step_time }}min</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Selection indicator -->
                <div v-if="selectedTemplate?.id === template.id" class="flex-shrink-0 ml-4 text-primary">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Custom name input (only shown when a template is selected) -->
        <div v-if="selectedTemplate" class="space-y-2 pt-4 border-t">
          <Label for="customName">Profile Name *</Label>
          <Input
            id="customName"
            v-model="customName"
            placeholder="Enter a name for your mash profile"
          />
          <p class="text-xs text-muted-foreground">
            Give your profile a unique name or use the default
          </p>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-2 pt-4 border-t">
          <Button variant="outline" @click="$emit('close')">Cancel</Button>
          <Button :disabled="!selectedTemplate && selectedTemplate !== null" @click="useTemplate">
            {{ selectedTemplate ? 'Use Template' : 'Continue' }}
          </Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
