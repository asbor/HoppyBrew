<template>
  <div class="container mx-auto py-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">Equipment Profiles</h1>
        <p class="text-muted-foreground">Manage your brewing equipment configurations</p>
      </div>
      <Button @click="openCreateDialog">
        <Plus class="mr-2 h-4 w-4" />
        New Profile
      </Button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <Loader2 class="h-8 w-8 animate-spin text-primary" />
    </div>

    <!-- Error State -->
    <Alert v-else-if="error" variant="destructive">
      <AlertCircle class="h-4 w-4" />
      <AlertTitle>Error</AlertTitle>
      <AlertDescription>{{ error }}</AlertDescription>
    </Alert>

    <!-- Equipment Profiles Table -->
    <Card v-else>
      <CardHeader>
        <CardTitle>All Equipment Profiles</CardTitle>
        <CardDescription>{{ profiles.length }} profile(s) configured</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead class="text-right">Batch Size</TableHead>
              <TableHead class="text-right">Boil Size</TableHead>
              <TableHead class="text-right">Boil Time</TableHead>
              <TableHead class="text-right">Efficiency</TableHead>
              <TableHead class="text-center">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="profile in profiles" :key="profile.id">
              <TableCell class="font-medium">{{ profile.name }}</TableCell>
              <TableCell class="text-right">
                {{ profile.display_batch_size || formatVolume(profile.batch_size) }}
              </TableCell>
              <TableCell class="text-right">
                {{ profile.display_boil_size || formatVolume(profile.boil_size) }}
              </TableCell>
              <TableCell class="text-right">{{ profile.boil_time }} min</TableCell>
              <TableCell class="text-right">{{ formatPercent(profile.hop_utilization) }}</TableCell>
              <TableCell class="text-center">
                <div class="flex justify-center gap-2">
                  <Button variant="ghost" size="icon" @click="viewProfile(profile)">
                    <Eye class="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" @click="editProfile(profile)">
                    <Pencil class="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" @click="deleteProfile(profile)">
                    <Trash2 class="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>

    <!-- Create/Edit Dialog -->
    <Dialog v-model:open="dialogOpen">
      <DialogContent class="max-w-3xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{{ isEditing ? 'Edit' : 'Create' }} Equipment Profile</DialogTitle>
          <DialogDescription>
            {{ isEditing ? 'Update' : 'Add' }} your brewing equipment specifications
          </DialogDescription>
        </DialogHeader>
        
        <form @submit.prevent="saveProfile" class="space-y-4">
          <!-- Basic Information -->
          <div class="space-y-4">
            <h3 class="font-semibold">Basic Information</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="name">Profile Name*</Label>
                <Input id="name" v-model="formData.name" required />
              </div>
              <div class="space-y-2">
                <Label for="version">Version</Label>
                <Input id="version" v-model="formData.version" type="number" />
              </div>
            </div>
          </div>

          <!-- Volume Settings -->
          <div class="space-y-4">
            <h3 class="font-semibold">Volume Settings</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="batch_size">Batch Size (L)*</Label>
                <Input id="batch_size" v-model.number="formData.batch_size" type="number" step="0.1" required />
              </div>
              <div class="space-y-2">
                <Label for="boil_size">Boil Size (L)*</Label>
                <Input id="boil_size" v-model.number="formData.boil_size" type="number" step="0.1" required />
              </div>
              <div class="space-y-2">
                <Label for="tun_volume">Tun Volume (L)</Label>
                <Input id="tun_volume" v-model.number="formData.tun_volume" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="lauter_deadspace">Lauter Deadspace (L)</Label>
                <Input id="lauter_deadspace" v-model.number="formData.lauter_deadspace" type="number" step="0.1" />
              </div>
            </div>
          </div>

          <!-- Boil Settings -->
          <div class="space-y-4">
            <h3 class="font-semibold">Boil Settings</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="boil_time">Boil Time (min)*</Label>
                <Input id="boil_time" v-model.number="formData.boil_time" type="number" required />
              </div>
              <div class="space-y-2">
                <Label for="evap_rate">Evaporation Rate (%/hr)</Label>
                <Input id="evap_rate" v-model.number="formData.evap_rate" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="hop_utilization">Hop Utilization (%)</Label>
                <Input id="hop_utilization" v-model.number="formData.hop_utilization" type="number" step="0.1" />
              </div>
            </div>
          </div>

          <!-- Loss Settings -->
          <div class="space-y-4">
            <h3 class="font-semibold">Loss Settings</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="trub_chiller_loss">Trub/Chiller Loss (L)</Label>
                <Input id="trub_chiller_loss" v-model.number="formData.trub_chiller_loss" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="top_up_water">Top Up Water (L)</Label>
                <Input id="top_up_water" v-model.number="formData.top_up_water" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="top_up_kettle">Top Up Kettle (L)</Label>
                <Input id="top_up_kettle" v-model.number="formData.top_up_kettle" type="number" step="0.1" />
              </div>
            </div>
          </div>

          <!-- Tun Settings -->
          <div class="space-y-4">
            <h3 class="font-semibold">Tun Specifications</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="tun_weight">Tun Weight (kg)</Label>
                <Input id="tun_weight" v-model.number="formData.tun_weight" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="tun_specific_heat">Tun Specific Heat (cal/g°C)</Label>
                <Input id="tun_specific_heat" v-model.number="formData.tun_specific_heat" type="number" step="0.01" />
              </div>
            </div>
          </div>

          <!-- Notes -->
          <div class="space-y-2">
            <Label for="notes">Notes</Label>
            <Textarea id="notes" v-model="formData.notes" rows="3" />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" @click="dialogOpen = false">Cancel</Button>
            <Button type="submit" :disabled="saving">
              <Loader2 v-if="saving" class="mr-2 h-4 w-4 animate-spin" />
              {{ isEditing ? 'Update' : 'Create' }}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>

    <!-- View Dialog -->
    <Dialog v-model:open="viewDialogOpen">
      <DialogContent class="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{{ selectedProfile?.name }}</DialogTitle>
          <DialogDescription>Equipment Profile Details</DialogDescription>
        </DialogHeader>
        
        <div v-if="selectedProfile" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-semibold text-muted-foreground">Batch Size</h4>
              <p class="text-lg">{{ selectedProfile.display_batch_size || formatVolume(selectedProfile.batch_size) }}</p>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-muted-foreground">Boil Size</h4>
              <p class="text-lg">{{ selectedProfile.display_boil_size || formatVolume(selectedProfile.boil_size) }}</p>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-muted-foreground">Boil Time</h4>
              <p class="text-lg">{{ selectedProfile.boil_time }} minutes</p>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-muted-foreground">Evaporation Rate</h4>
              <p class="text-lg">{{ formatPercent(selectedProfile.evap_rate) }}/hr</p>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-muted-foreground">Hop Utilization</h4>
              <p class="text-lg">{{ formatPercent(selectedProfile.hop_utilization) }}</p>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-muted-foreground">Trub/Chiller Loss</h4>
              <p class="text-lg">{{ formatVolume(selectedProfile.trub_chiller_loss) }}</p>
            </div>
          </div>
          
          <div v-if="selectedProfile.notes">
            <h4 class="text-sm font-semibold text-muted-foreground mb-2">Notes</h4>
            <p class="text-sm whitespace-pre-wrap">{{ selectedProfile.notes }}</p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Eye, Pencil, Trash2, AlertCircle, Loader2 } from 'lucide-vue-next'
import { useApi } from '@/composables/useApi'

interface EquipmentProfile {
  id: number
  name: string
  version?: number
  batch_size: number
  boil_size: number
  tun_volume?: number
  tun_weight?: number
  tun_specific_heat?: number
  top_up_water?: number
  trub_chiller_loss?: number
  evap_rate?: number
  boil_time: number
  calc_boil_volume?: boolean
  lauter_deadspace?: number
  top_up_kettle?: number
  hop_utilization?: number
  notes?: string
  display_batch_size?: string
  display_boil_size?: string
  display_tun_volume?: string
  display_tun_weight?: string
  display_top_up_water?: string
  display_trub_chiller_loss?: string
  display_lauter_deadspace?: string
  display_top_up_kettle?: string
}

const api = useApi()
const profiles = ref<EquipmentProfile[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const dialogOpen = ref(false)
const viewDialogOpen = ref(false)
const saving = ref(false)
const isEditing = ref(false)
const selectedProfile = ref<EquipmentProfile | null>(null)

const formData = ref({
  name: '',
  version: 1,
  batch_size: 0,
  boil_size: 0,
  tun_volume: 0,
  tun_weight: 0,
  tun_specific_heat: 0.3,
  top_up_water: 0,
  trub_chiller_loss: 0,
  evap_rate: 10,
  boil_time: 60,
  lauter_deadspace: 0,
  top_up_kettle: 0,
  hop_utilization: 100,
  notes: ''
})

const formatVolume = (value: number | undefined) => {
  if (!value) return '0 L'
  return `${value.toFixed(1)} L`
}

const formatPercent = (value: number | undefined) => {
  if (!value) return '0%'
  return `${value.toFixed(1)}%`
}

const fetchProfiles = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get<EquipmentProfile[]>('/equipment')

    if (response.error.value) {
      error.value = response.error.value
      profiles.value = []
    } else {
      profiles.value = response.data.value || []
    }
  } catch (e: any) {
    error.value = e.message || 'Failed to load equipment profiles'
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  formData.value = {
    name: '',
    version: 1,
    batch_size: 0,
    boil_size: 0,
    tun_volume: 0,
    tun_weight: 0,
    tun_specific_heat: 0.3,
    top_up_water: 0,
    trub_chiller_loss: 0,
    evap_rate: 10,
    boil_time: 60,
    lauter_deadspace: 0,
    top_up_kettle: 0,
    hop_utilization: 100,
    notes: ''
  }
  dialogOpen.value = true
}

const viewProfile = (profile: EquipmentProfile) => {
  selectedProfile.value = profile
  viewDialogOpen.value = true
}

const editProfile = (profile: EquipmentProfile) => {
  isEditing.value = true
  selectedProfile.value = profile
  formData.value = {
    name: profile.name,
    version: profile.version || 1,
    batch_size: profile.batch_size,
    boil_size: profile.boil_size,
    tun_volume: profile.tun_volume || 0,
    tun_weight: profile.tun_weight || 0,
    tun_specific_heat: profile.tun_specific_heat || 0.3,
    top_up_water: profile.top_up_water || 0,
    trub_chiller_loss: profile.trub_chiller_loss || 0,
    evap_rate: profile.evap_rate || 10,
    boil_time: profile.boil_time,
    lauter_deadspace: profile.lauter_deadspace || 0,
    top_up_kettle: profile.top_up_kettle || 0,
    hop_utilization: profile.hop_utilization || 100,
    notes: profile.notes || ''
  }
  dialogOpen.value = true
}

const saveProfile = async () => {
  saving.value = true
  
  try {
    if (isEditing.value && selectedProfile.value) {
      const response = await api.put<EquipmentProfile>(`/equipment/${selectedProfile.value.id}`, formData.value)
      
      if (response.error.value) {
        error.value = response.error.value
        return
      }
    } else {
      const response = await api.post<EquipmentProfile>('/equipment', formData.value)
      
      if (response.error.value) {
        error.value = response.error.value
        return
      }
    }
    
    dialogOpen.value = false
    await fetchProfiles()
  } catch (e: any) {
    error.value = e.message || 'Failed to save equipment profile'
  } finally {
    saving.value = false
  }
}

const deleteProfile = async (profile: EquipmentProfile) => {
  if (!confirm(`Are you sure you want to delete "${profile.name}"?`)) {
    return
  }
  
  try {
    const response = await api.delete(`/equipment/${profile.id}`)
    
    if (response.error.value) {
      error.value = response.error.value
      return
    }
    
    await fetchProfiles()
  } catch (e: any) {
    error.value = e.message || 'Failed to delete equipment profile'
  }
}

onMounted(() => {
  fetchProfiles()
})
</script>
