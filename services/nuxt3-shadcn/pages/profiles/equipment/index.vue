<script setup lang="ts">
import { 
  Settings, 
  Plus, 
  Edit3, 
  Trash2, 
  Copy, 
  Beaker, 
  Thermometer, 
  Droplets,
  Calculator,
  FlaskConical,
  Gauge
} from 'lucide-vue-next'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { Separator } from '@/components/ui/separator'
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog'

interface EquipmentProfile {
  id: number
  name: string
  description?: string
  notes?: string
  version?: string
  
  // Volume settings
  batch_size: number
  boil_size: number
  tun_volume: number
  
  // Loss calculations
  trub_chiller_loss: number
  lauter_deadspace: number
  top_up_water: number
  top_up_kettle: number
  
  // Efficiency & timing
  hop_utilization: number
  boil_time: number
  calc_boil_volume: boolean
  
  // Physical properties
  tun_weight: number
  tun_specific_heat: number
  evap_rate: number
  
  // Display settings
  display_batch_size?: string
  display_boil_size?: string
  display_tun_volume?: string
  display_tun_weight?: string
  display_tun_specific_heat?: string
  display_top_up_water?: string
  display_top_up_kettle?: string
  display_trub_chiller_loss?: string
  display_lauter_deadspace?: string
}

const api = useApi()
const router = useRouter()

// State
const equipment = ref<EquipmentProfile[]>([])
const selectedEquipment = ref<EquipmentProfile | null>(null)
const editDialogOpen = ref(false)
const deleteDialogOpen = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

// New equipment form
const newEquipmentDialog = ref(false)
const newEquipment = ref<Partial<EquipmentProfile>>({
  name: '',
  description: '',
  notes: '',
  batch_size: 20,
  boil_size: 25,
  tun_volume: 30,
  trub_chiller_loss: 1.3,
  lauter_deadspace: 2.5,
  top_up_water: 0,
  top_up_kettle: 0,
  hop_utilization: 100,
  boil_time: 60,
  calc_boil_volume: true,
  tun_weight: 5,
  tun_specific_heat: 0.38,
  evap_rate: 8
})

// Load equipment profiles
const fetchEquipment = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch('http://localhost:8000/equipment', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch equipment profiles')
    }
    
    equipment.value = await response.json()
  } catch (err) {
    error.value = 'Failed to load equipment profiles'
    console.error('Error fetching equipment:', err)
  } finally {
    loading.value = false
  }
}

// Create new equipment profile
const createEquipment = async () => {
  try {
    const response = await fetch('http://localhost:8000/equipment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(newEquipment.value)
    })
    
    if (!response.ok) {
      throw new Error('Failed to create equipment profile')
    }
    
    await fetchEquipment()
    newEquipmentDialog.value = false
    resetNewEquipmentForm()
  } catch (err) {
    error.value = 'Failed to create equipment profile'
    console.error('Error creating equipment:', err)
  }
}

// Update equipment profile
const updateEquipment = async () => {
  if (!selectedEquipment.value?.id) return
  
  try {
    const response = await fetch(`http://localhost:8000/equipment/${selectedEquipment.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(selectedEquipment.value)
    })
    
    if (!response.ok) {
      throw new Error('Failed to update equipment profile')
    }
    
    await fetchEquipment()
    editDialogOpen.value = false
  } catch (err) {
    error.value = 'Failed to update equipment profile'
    console.error('Error updating equipment:', err)
  }
}

// Delete equipment profile
const deleteEquipment = async () => {
  if (!selectedEquipment.value?.id) return
  
  try {
    const response = await fetch(`http://localhost:8000/equipment/${selectedEquipment.value.id}`, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to delete equipment profile')
    }
    
    await fetchEquipment()
    deleteDialogOpen.value = false
    selectedEquipment.value = null
  } catch (err) {
    error.value = 'Failed to delete equipment profile'
    console.error('Error deleting equipment:', err)
  }
}

// Duplicate equipment profile
const duplicateEquipment = async (equipment: EquipmentProfile) => {
  const duplicate = {
    ...equipment,
    name: `${equipment.name} (Copy)`,
    id: undefined
  }
  delete duplicate.id
  
  try {
    const response = await fetch('http://localhost:8000/equipment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(duplicate)
    })
    
    if (!response.ok) {
      throw new Error('Failed to duplicate equipment profile')
    }
    
    await fetchEquipment()
  } catch (err) {
    error.value = 'Failed to duplicate equipment profile'
    console.error('Error duplicating equipment:', err)
  }
}

// Open edit dialog
const openEditDialog = (equipmentItem: EquipmentProfile) => {
  selectedEquipment.value = { ...equipmentItem }
  editDialogOpen.value = true
}

// Open delete dialog
const openDeleteDialog = (equipmentItem: EquipmentProfile) => {
  selectedEquipment.value = equipmentItem
  deleteDialogOpen.value = true
}

// Reset new equipment form
const resetNewEquipmentForm = () => {
  newEquipment.value = {
    name: '',
    description: '',
    notes: '',
    batch_size: 20,
    boil_size: 25,
    tun_volume: 30,
    trub_chiller_loss: 1.3,
    lauter_deadspace: 2.5,
    top_up_water: 0,
    top_up_kettle: 0,
    hop_utilization: 100,
    boil_time: 60,
    calc_boil_volume: true,
    tun_weight: 5,
    tun_specific_heat: 0.38,
    evap_rate: 8
  }
}

// Calculate efficiency percentage
const calculateEfficiency = (equipment: EquipmentProfile) => {
  const baseEfficiency = 75
  const lossAdjustment = (equipment.trub_chiller_loss + equipment.lauter_deadspace) * 0.5
  return Math.max(65, Math.min(95, baseEfficiency - lossAdjustment))
}

// Calculate total volume capacity
const calculateTotalCapacity = (equipment: EquipmentProfile) => {
  return equipment.boil_size + equipment.trub_chiller_loss + equipment.lauter_deadspace
}

// Load data on mount
onMounted(() => {
  fetchEquipment()
})
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
          <Settings class="h-8 w-8 text-primary" />
          Equipment Profiles
        </h1>
        <p class="text-muted-foreground">
          Manage your brewing equipment configurations and volume calculations
        </p>
      </div>
      
      <Dialog v-model:open="newEquipmentDialog">
        <DialogTrigger as-child>
          <Button class="flex items-center gap-2">
            <Plus class="h-4 w-4" />
            New Profile
          </Button>
        </DialogTrigger>
        <DialogContent class="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Create Equipment Profile</DialogTitle>
            <DialogDescription>
              Set up a new brewing equipment configuration
            </DialogDescription>
          </DialogHeader>
          
          <div class="grid gap-6">
            <!-- Basic Information -->
            <div class="space-y-4">
              <h3 class="text-lg font-medium flex items-center gap-2">
                <Beaker class="h-5 w-5" />
                Basic Information
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label for="new-name">Equipment Name</Label>
                  <Input 
                    id="new-name" 
                    v-model="newEquipment.name" 
                    placeholder="e.g., Brewster Beacon 70L"
                  />
                </div>
                
                <div>
                  <Label for="new-version">Version</Label>
                  <Input 
                    id="new-version" 
                    v-model="newEquipment.version" 
                    placeholder="e.g., v1.0"
                  />
                </div>
              </div>
              
              <div>
                <Label for="new-description">Description</Label>
                <Textarea 
                  id="new-description" 
                  v-model="newEquipment.description"
                  placeholder="Brief description of this equipment setup"
                  rows="3"
                />
              </div>
            </div>

            <Separator />

            <!-- Volume Management -->
            <div class="space-y-4">
              <h3 class="text-lg font-medium flex items-center gap-2">
                <FlaskConical class="h-5 w-5" />
                Volume Management
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label for="new-batch-size">Batch Size (L)</Label>
                  <Input 
                    id="new-batch-size" 
                    v-model.number="newEquipment.batch_size" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div>
                  <Label for="new-boil-size">Boil Size (L)</Label>
                  <Input 
                    id="new-boil-size" 
                    v-model.number="newEquipment.boil_size" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div>
                  <Label for="new-tun-volume">Tun Volume (L)</Label>
                  <Input 
                    id="new-tun-volume" 
                    v-model.number="newEquipment.tun_volume" 
                    type="number"
                    step="0.1"
                  />
                </div>
              </div>
            </div>

            <Separator />

            <!-- Loss Calculations -->
            <div class="space-y-4">
              <h3 class="text-lg font-medium flex items-center gap-2">
                <Droplets class="h-5 w-5" />
                Loss Calculations
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <Label for="new-trub-loss">Trub/Chiller Loss (L)</Label>
                  <Input 
                    id="new-trub-loss" 
                    v-model.number="newEquipment.trub_chiller_loss" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div>
                  <Label for="new-lauter-deadspace">Lauter Deadspace (L)</Label>
                  <Input 
                    id="new-lauter-deadspace" 
                    v-model.number="newEquipment.lauter_deadspace" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div>
                  <Label for="new-top-up-water">Top-up Water (L)</Label>
                  <Input 
                    id="new-top-up-water" 
                    v-model.number="newEquipment.top_up_water" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div>
                  <Label for="new-top-up-kettle">Top-up Kettle (L)</Label>
                  <Input 
                    id="new-top-up-kettle" 
                    v-model.number="newEquipment.top_up_kettle" 
                    type="number"
                    step="0.1"
                  />
                </div>
              </div>
            </div>

            <Separator />

            <!-- Efficiency & Advanced -->
            <div class="space-y-4">
              <h3 class="text-lg font-medium flex items-center gap-2">
                <Gauge class="h-5 w-5" />
                Efficiency & Advanced Settings
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <Label for="new-hop-util">Hop Utilization (%)</Label>
                  <Input 
                    id="new-hop-util" 
                    v-model.number="newEquipment.hop_utilization" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div>
                  <Label for="new-boil-time">Boil Time (min)</Label>
                  <Input 
                    id="new-boil-time" 
                    v-model.number="newEquipment.boil_time"
                    type="number"
                  />
                </div>
                
                <div>
                  <Label for="new-evap-rate">Evaporation Rate (%/hr)</Label>
                  <Input 
                    id="new-evap-rate" 
                    v-model.number="newEquipment.evap_rate" 
                    type="number"
                    step="0.1"
                  />
                </div>
                
                <div class="flex items-center space-x-2 pt-6">
                  <Checkbox 
                    id="new-calc-boil" 
                    v-model:checked="newEquipment.calc_boil_volume"
                  />
                  <Label for="new-calc-boil">Calculate boil volume</Label>
                </div>
              </div>
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" @click="newEquipmentDialog = false">
              Cancel
            </Button>
            <Button :disabled="!newEquipment.name" @click="createEquipment">
              Create Profile
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
      <p class="mt-4 text-muted-foreground">Loading equipment profiles...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-destructive">{{ error }}</p>
      <Button class="mt-4" @click="fetchEquipment()">Try Again</Button>
    </div>

    <!-- Equipment Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card 
        v-for="equipmentItem in equipment" 
        :key="equipmentItem.id"
        class="hover:shadow-lg transition-shadow"
      >
        <CardHeader>
          <div class="flex justify-between items-start">
            <div>
              <CardTitle class="flex items-center gap-2">
                {{ equipmentItem.name }}
                <Badge v-if="equipmentItem.version" variant="secondary">
                  {{ equipmentItem.version }}
                </Badge>
              </CardTitle>
              <CardDescription v-if="equipmentItem.description">
                {{ equipmentItem.description }}
              </CardDescription>
            </div>
            
            <div class="flex gap-1">
              <Button 
                variant="ghost" 
                size="sm"
                title="Duplicate"
                @click="duplicateEquipment(equipmentItem)"
              >
                <Copy class="h-3 w-3" />
              </Button>
              <Button 
                variant="ghost" 
                size="sm"
                title="Edit"
                @click="openEditDialog(equipmentItem)"
              >
                <Edit3 class="h-3 w-3" />
              </Button>
              <Button 
                variant="ghost" 
                size="sm"
                title="Delete"
                @click="openDeleteDialog(equipmentItem)"
              >
                <Trash2 class="h-3 w-3 text-destructive" />
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent class="space-y-4">
          <!-- Volume Summary -->
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div class="text-muted-foreground">Batch Size</div>
              <div class="font-medium">{{ equipmentItem.batch_size }}L</div>
            </div>
            <div>
              <div class="text-muted-foreground">Boil Size</div>
              <div class="font-medium">{{ equipmentItem.boil_size }}L</div>
            </div>
            <div>
              <div class="text-muted-foreground">Total Capacity</div>
              <div class="font-medium">{{ calculateTotalCapacity(equipmentItem) }}L</div>
            </div>
            <div>
              <div class="text-muted-foreground">Est. Efficiency</div>
              <div class="font-medium">{{ calculateEfficiency(equipmentItem).toFixed(1) }}%</div>
            </div>
          </div>

          <!-- Loss Summary -->
          <div class="pt-2 border-t">
            <div class="text-sm text-muted-foreground mb-2">Loss Profile</div>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div>Trub/Chiller: {{ equipmentItem.trub_chiller_loss }}L</div>
              <div>Deadspace: {{ equipmentItem.lauter_deadspace }}L</div>
              <div>Hop Utilization: {{ equipmentItem.hop_utilization }}%</div>
              <div>Boil Time: {{ equipmentItem.boil_time }}min</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && equipment.length === 0" class="text-center py-12">
      <Settings class="h-12 w-12 text-muted-foreground mx-auto mb-4" />
      <h3 class="text-lg font-medium">No equipment profiles</h3>
      <p class="text-muted-foreground mt-2">Create your first equipment profile to get started</p>
      <Button class="mt-4" @click="newEquipmentDialog = true">
        <Plus class="h-4 w-4 mr-2" />
        Create First Profile
      </Button>
    </div>

    <!-- Edit Dialog (simplified for brevity - similar structure to create dialog) -->
    <Dialog v-model:open="editDialogOpen">
      <DialogContent class="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Edit Equipment Profile</DialogTitle>
          <DialogDescription>Update your equipment configuration</DialogDescription>
        </DialogHeader>
        
        <div v-if="selectedEquipment" class="grid gap-4">
          <div>
            <Label for="edit-name">Equipment Name</Label>
            <Input 
              id="edit-name" 
              v-model="selectedEquipment.name"
            />
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <Label for="edit-batch-size">Batch Size (L)</Label>
              <Input 
                id="edit-batch-size" 
                v-model.number="selectedEquipment.batch_size" 
                type="number"
                step="0.1"
              />
            </div>
            <div>
              <Label for="edit-boil-size">Boil Size (L)</Label>
              <Input 
                id="edit-boil-size" 
                v-model.number="selectedEquipment.boil_size" 
                type="number"
                step="0.1"
              />
            </div>
          </div>
        </div>
        
        <DialogFooter>
          <Button variant="outline" @click="editDialogOpen = false">
            Cancel
          </Button>
          <Button @click="updateEquipment">
            Update Profile
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog v-model:open="deleteDialogOpen">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Equipment Profile</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "{{ selectedEquipment?.name }}"? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        
        <DialogFooter>
          <Button variant="outline" @click="deleteDialogOpen = false">
            Cancel
          </Button>
          <Button variant="destructive" @click="deleteEquipment">
            Delete Profile
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>