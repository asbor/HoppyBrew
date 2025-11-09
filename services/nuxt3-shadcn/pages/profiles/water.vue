<template>
  <div class="container mx-auto py-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">Water Profiles</h1>
        <p class="text-muted-foreground">Manage source and target water chemistry profiles</p>
      </div>
      <Button @click="openCreateDialog">
        <Plus class="mr-2 h-4 w-4" />
        New Profile
      </Button>
    </div>

    <!-- Filter Tabs -->
    <Tabs default-value="all" class="w-full">
      <TabsList>
        <TabsTrigger value="all" @click="filterType = null">All Profiles</TabsTrigger>
        <TabsTrigger value="source" @click="filterType = 'source'">Source Water</TabsTrigger>
        <TabsTrigger value="target" @click="filterType = 'target'">Target Profiles</TabsTrigger>
      </TabsList>
    </Tabs>

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

    <!-- Water Profiles Table -->
    <Card v-else>
      <CardHeader>
        <CardTitle>Water Chemistry Profiles</CardTitle>
        <CardDescription>{{ filteredProfiles.length }} profile(s) available</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Type</TableHead>
              <TableHead class="text-right">Ca²⁺</TableHead>
              <TableHead class="text-right">Mg²⁺</TableHead>
              <TableHead class="text-right">Na⁺</TableHead>
              <TableHead class="text-right">Cl⁻</TableHead>
              <TableHead class="text-right">SO₄²⁻</TableHead>
              <TableHead class="text-right">HCO₃⁻</TableHead>
              <TableHead class="text-center">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="profile in filteredProfiles" :key="profile.id">
              <TableCell class="font-medium">
                {{ profile.name }}
                <Badge v-if="profile.is_default" variant="outline" class="ml-2">Default</Badge>
              </TableCell>
              <TableCell>
                <Badge :variant="profile.profile_type === 'source' ? 'secondary' : 'default'">
                  {{ profile.profile_type }}
                </Badge>
              </TableCell>
              <TableCell class="text-right">{{ profile.calcium }}</TableCell>
              <TableCell class="text-right">{{ profile.magnesium }}</TableCell>
              <TableCell class="text-right">{{ profile.sodium }}</TableCell>
              <TableCell class="text-right">{{ profile.chloride }}</TableCell>
              <TableCell class="text-right">{{ profile.sulfate }}</TableCell>
              <TableCell class="text-right">{{ profile.bicarbonate }}</TableCell>
              <TableCell class="text-center">
                <div class="flex justify-center gap-2">
                  <Button variant="ghost" size="icon" @click="viewProfile(profile)">
                    <Eye class="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" @click="editProfile(profile)" :disabled="profile.is_default">
                    <Pencil class="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" @click="deleteProfile(profile)" :disabled="profile.is_default">
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
      <DialogContent class="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{{ isEditing ? 'Edit' : 'Create' }} Water Profile</DialogTitle>
          <DialogDescription>
            {{ isEditing ? 'Update' : 'Add' }} water chemistry profile for brewing calculations
          </DialogDescription>
        </DialogHeader>

        <form @submit.prevent="saveProfile" class="space-y-4">
          <!-- Basic Information -->
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="name">Profile Name*</Label>
                <Input id="name" v-model="formData.name" required />
              </div>
              <div class="space-y-2">
                <Label for="profile_type">Profile Type*</Label>
                <Select v-model="formData.profile_type" required>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="source">Source Water</SelectItem>
                    <SelectItem value="target">Target Profile</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>

          <!-- Ion Concentrations -->
          <div class="space-y-4">
            <h3 class="font-semibold">Ion Concentrations (ppm)</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="calcium">Calcium (Ca²⁺)</Label>
                <Input id="calcium" v-model.number="formData.calcium" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="magnesium">Magnesium (Mg²⁺)</Label>
                <Input id="magnesium" v-model.number="formData.magnesium" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="sodium">Sodium (Na⁺)</Label>
                <Input id="sodium" v-model.number="formData.sodium" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="chloride">Chloride (Cl⁻)</Label>
                <Input id="chloride" v-model.number="formData.chloride" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="sulfate">Sulfate (SO₄²⁻)</Label>
                <Input id="sulfate" v-model.number="formData.sulfate" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="bicarbonate">Bicarbonate (HCO₃⁻)</Label>
                <Input id="bicarbonate" v-model.number="formData.bicarbonate" type="number" step="0.1" />
              </div>
            </div>
          </div>

          <!-- Optional Fields -->
          <div class="space-y-4">
            <h3 class="font-semibold">Additional Information</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label for="ph">pH</Label>
                <Input id="ph" v-model.number="formData.ph" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="alkalinity">Alkalinity (ppm as CaCO₃)</Label>
                <Input id="alkalinity" v-model.number="formData.alkalinity" type="number" step="0.1" />
              </div>
              <div class="space-y-2">
                <Label for="style_category">Style Category</Label>
                <Input id="style_category" v-model="formData.style_category" placeholder="e.g., IPA, Stout" />
              </div>
            </div>
          </div>

          <!-- Notes -->
          <div class="space-y-2">
            <Label for="notes">Notes</Label>
            <Textarea id="notes" v-model="formData.notes" rows="3" placeholder="Brewing notes, recommendations..." />
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
          <DialogDescription>
            <Badge :variant="selectedProfile?.profile_type === 'source' ? 'secondary' : 'default'">
              {{ selectedProfile?.profile_type }}
            </Badge>
            <Badge v-if="selectedProfile?.is_default" variant="outline" class="ml-2">Default</Badge>
          </DialogDescription>
        </DialogHeader>

        <div v-if="selectedProfile" class="space-y-4">
          <div>
            <h4 class="text-sm font-semibold text-muted-foreground mb-3">Ion Concentrations (ppm)</h4>
            <div class="grid grid-cols-3 gap-4">
              <div>
                <p class="text-xs text-muted-foreground">Calcium (Ca²⁺)</p>
                <p class="text-lg font-semibold">{{ selectedProfile.calcium }}</p>
              </div>
              <div>
                <p class="text-xs text-muted-foreground">Magnesium (Mg²⁺)</p>
                <p class="text-lg font-semibold">{{ selectedProfile.magnesium }}</p>
              </div>
              <div>
                <p class="text-xs text-muted-foreground">Sodium (Na⁺)</p>
                <p class="text-lg font-semibold">{{ selectedProfile.sodium }}</p>
              </div>
              <div>
                <p class="text-xs text-muted-foreground">Chloride (Cl⁻)</p>
                <p class="text-lg font-semibold">{{ selectedProfile.chloride }}</p>
              </div>
              <div>
                <p class="text-xs text-muted-foreground">Sulfate (SO₄²⁻)</p>
                <p class="text-lg font-semibold">{{ selectedProfile.sulfate }}</p>
              </div>
              <div>
                <p class="text-xs text-muted-foreground">Bicarbonate (HCO₃⁻)</p>
                <p class="text-lg font-semibold">{{ selectedProfile.bicarbonate }}</p>
              </div>
            </div>
          </div>

          <div v-if="selectedProfile.ph || selectedProfile.alkalinity" class="grid grid-cols-2 gap-4">
            <div v-if="selectedProfile.ph">
              <h4 class="text-sm font-semibold text-muted-foreground">pH</h4>
              <p class="text-lg">{{ selectedProfile.ph }}</p>
            </div>
            <div v-if="selectedProfile.alkalinity">
              <h4 class="text-sm font-semibold text-muted-foreground">Alkalinity</h4>
              <p class="text-lg">{{ selectedProfile.alkalinity }} ppm</p>
            </div>
          </div>

          <!-- Calculated Ratios -->
          <div v-if="selectedProfile.chloride && selectedProfile.sulfate">
            <h4 class="text-sm font-semibold text-muted-foreground mb-2">Water Ratios</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-muted-foreground">Cl⁻ : SO₄²⁻ Ratio</p>
                <p class="text-lg font-semibold">
                  {{ (selectedProfile.chloride / selectedProfile.sulfate).toFixed(2) }}
                </p>
                <p class="text-xs text-muted-foreground mt-1">
                  {{ getWaterCharacter(selectedProfile.chloride / selectedProfile.sulfate) }}
                </p>
              </div>
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
import { ref, computed, onMounted } from 'vue'
import { Plus, Eye, Pencil, Trash2, AlertCircle, Loader2 } from 'lucide-vue-next'

interface WaterProfile {
  id: number
  name: string
  profile_type: 'source' | 'target'
  calcium: number
  magnesium: number
  sodium: number
  chloride: number
  sulfate: number
  bicarbonate: number
  ph?: number
  alkalinity?: number
  style_category?: string
  notes?: string
  is_default: boolean
}

const profiles = ref<WaterProfile[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const dialogOpen = ref(false)
const viewDialogOpen = ref(false)
const saving = ref(false)
const isEditing = ref(false)
const selectedProfile = ref<WaterProfile | null>(null)
const filterType = ref<'source' | 'target' | null>(null)

const filteredProfiles = computed(() => {
  if (!filterType.value) return profiles.value
  return profiles.value.filter(p => p.profile_type === filterType.value)
})

const formData = ref({
  name: '',
  profile_type: 'source' as 'source' | 'target',
  calcium: 0,
  magnesium: 0,
  sodium: 0,
  chloride: 0,
  sulfate: 0,
  bicarbonate: 0,
  ph: 7.0,
  alkalinity: 0,
  style_category: '',
  notes: ''
})

const getWaterCharacter = (ratio: number) => {
  if (ratio < 0.5) return 'Hoppy/Bitter (High Sulfate)'
  if (ratio < 1.5) return 'Balanced'
  return 'Malty/Sweet (High Chloride)'
}

const fetchProfiles = async () => {
  loading.value = true
  error.value = null

  try {
    const { data, error: fetchError } = await useApi('/water-profiles')

    if (fetchError && fetchError.value) {
      error.value = fetchError.value.message || 'Failed to load water profiles'
    } else if (data && data.value) {
      profiles.value = data.value
    }
  } catch (e: any) {
    error.value = e.message || 'Failed to load water profiles'
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  formData.value = {
    name: '',
    profile_type: 'source',
    calcium: 0,
    magnesium: 0,
    sodium: 0,
    chloride: 0,
    sulfate: 0,
    bicarbonate: 0,
    ph: 7.0,
    alkalinity: 0,
    style_category: '',
    notes: ''
  }
  dialogOpen.value = true
}

const viewProfile = (profile: WaterProfile) => {
  selectedProfile.value = profile
  viewDialogOpen.value = true
}

const editProfile = (profile: WaterProfile) => {
  if (profile.is_default) return

  isEditing.value = true
  selectedProfile.value = profile
  formData.value = {
    name: profile.name,
    profile_type: profile.profile_type,
    calcium: profile.calcium,
    magnesium: profile.magnesium,
    sodium: profile.sodium,
    chloride: profile.chloride,
    sulfate: profile.sulfate,
    bicarbonate: profile.bicarbonate,
    ph: profile.ph || 7.0,
    alkalinity: profile.alkalinity || 0,
    style_category: profile.style_category || '',
    notes: profile.notes || ''
  }
  dialogOpen.value = true
}

const saveProfile = async () => {
  saving.value = true

  try {
    if (isEditing.value && selectedProfile.value) {
      const { error: updateError } = await useApi(`/water-profiles/${selectedProfile.value.id}`, {
        method: 'PUT',
        body: formData.value
      })

      if (updateError && updateError.value) {
        error.value = updateError.value.message || 'Failed to update water profile'
        return
      }
    } else {
      const { error: createError } = await useApi('/water-profiles', {
        method: 'POST',
        body: formData.value
      })

      if (createError && createError.value) {
        error.value = createError.value.message || 'Failed to create water profile'
        return
      }
    }

    dialogOpen.value = false
    await fetchProfiles()
  } catch (e: any) {
    error.value = e.message || 'Failed to save water profile'
  } finally {
    saving.value = false
  }
}

const deleteProfile = async (profile: WaterProfile) => {
  if (profile.is_default) return

  if (!confirm(`Are you sure you want to delete "${profile.name}"?`)) {
    return
  }

  try {
    const { error: deleteError } = await useApi(`/water-profiles/${profile.id}`, {
      method: 'DELETE'
    })

    if (deleteError && deleteError.value) {
      error.value = deleteError.value.message || 'Failed to delete water profile'
      return
    }

    await fetchProfiles()
  } catch (e: any) {
    error.value = e.message || 'Failed to delete water profile'
  }
}

onMounted(() => {
  fetchProfiles()
})
</script>
