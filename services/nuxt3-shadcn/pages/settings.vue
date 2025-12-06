<template>
  <div>
    <header class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-2xl font-semibold">Settings</h1>
        <p class="text-gray-600 mt-2">Manage your external brewing devices and system settings</p>
      </div>
    </header>

    <div class="space-y-6">
      <!-- Devices Section -->
      <Card>
        <CardHeader>
          <div class="flex justify-between items-center">
            <div>
              <CardTitle>External Devices</CardTitle>
              <CardDescription>Configure iSpindel, Tilt, and other monitoring devices</CardDescription>
            </div>
            <Button @click="showAddDevice = true">
              Add Device
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div v-if="loading" class="text-center py-8">
            <p>Loading devices...</p>
          </div>
          <div v-else-if="error" class="text-center py-8 text-red-600">
            <p>Error: {{ error }}</p>
          </div>
          <div v-else-if="devices.length === 0" class="text-center py-8 text-gray-500">
            <p>No devices configured. Add your first device to get started.</p>
          </div>
          <div v-else class="space-y-4">
            <Card v-for="device in devices" :key="device.id" class="border">
              <CardContent class="pt-6">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="flex items-center gap-2">
                      <h3 class="text-lg font-semibold">{{ device.name }}</h3>
                      <Badge :variant="device.is_active ? 'default' : 'secondary'">
                        {{ device.is_active ? 'Active' : 'Inactive' }}
                      </Badge>
                      <Badge variant="outline">{{ device.device_type }}</Badge>
                    </div>
                    <p v-if="device.description" class="text-sm text-gray-600 mt-1">
                      {{ device.description }}
                    </p>
                    <div class="mt-3 space-y-1 text-sm text-gray-500">
                      <p v-if="device.api_endpoint">
                        <span class="font-medium">Endpoint:</span> {{ device.api_endpoint }}
                      </p>
                      <p v-if="device.calibration_data">
                        <span class="font-medium">Calibration:</span> Configured
                      </p>
                      <p v-if="device.configuration?.update_interval">
                        <span class="font-medium">Update Interval:</span> 
                        {{ device.configuration.update_interval }}s
                      </p>
                    </div>
                  </div>
                  <div class="flex gap-2">
                    <Button variant="outline" size="sm" @click="editDevice(device)">
                      Edit
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      @click="toggleStatus(device)"
                    >
                      {{ device.is_active ? 'Deactivate' : 'Activate' }}
                    </Button>
                    <Button variant="destructive" size="sm" @click="confirmDelete(device)">
                      Delete
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Add/Edit Device Dialog -->
    <AlertDialog :open="showAddDevice || showEditDevice" @update:open="closeDialog">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>
            {{ editingDevice ? 'Edit Device' : 'Add New Device' }}
          </AlertDialogTitle>
          <AlertDialogDescription>
            Configure your external brewing device settings
          </AlertDialogDescription>
        </AlertDialogHeader>
        
        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="name">Device Name *</Label>
            <Input 
              id="name" 
              v-model="deviceForm.name" 
              placeholder="My iSpindel"
            />
          </div>

          <div class="space-y-2">
            <Label for="device_type">Device Type *</Label>
            <Input 
              id="device_type" 
              v-model="deviceForm.device_type" 
              placeholder="ispindel"
            />
            <p class="text-xs text-gray-500">e.g., ispindel, tilt</p>
          </div>

          <div class="space-y-2">
            <Label for="description">Description</Label>
            <Input 
              id="description" 
              v-model="deviceForm.description" 
              placeholder="Device description"
            />
          </div>

          <div class="space-y-2">
            <Label for="api_endpoint">API Endpoint</Label>
            <Input 
              id="api_endpoint" 
              v-model="deviceForm.api_endpoint" 
              placeholder="/api/devices/ispindel/data"
            />
          </div>

          <div class="space-y-2">
            <Label for="api_token">API Token</Label>
            <Input 
              id="api_token" 
              v-model="deviceForm.api_token" 
              type="password"
              placeholder="Optional authentication token"
            />
          </div>

          <div class="flex items-center space-x-2">
            <input 
              id="is_active" 
              v-model="deviceForm.is_active" 
              type="checkbox"
              class="rounded"
            />
            <Label for="is_active">Active</Label>
          </div>
        </div>

        <AlertDialogFooter>
          <AlertDialogCancel @click="closeDialog">Cancel</AlertDialogCancel>
          <AlertDialogAction @click="saveDevice">
            {{ editingDevice ? 'Update' : 'Create' }}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>

    <!-- Delete Confirmation Dialog -->
    <AlertDialog :open="showDeleteConfirm" @update:open="showDeleteConfirm = false">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Device</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete "{{ deviceToDelete?.name }}"? This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction @click="deleteDeviceConfirmed">
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import type { Device } from '@/composables/useDevices'

const { getAllDevices, createDevice, updateDevice, deleteDevice, toggleDeviceStatus } = useDevices()

const devices = ref<Device[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showAddDevice = ref(false)
const showEditDevice = ref(false)
const showDeleteConfirm = ref(false)
const editingDevice = ref<Device | null>(null)
const deviceToDelete = ref<Device | null>(null)

const deviceForm = ref({
  name: '',
  device_type: '',
  description: '',
  api_endpoint: '',
  api_token: '',
  is_active: true
})

const loadDevices = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await getAllDevices()
    if (response.error.value) {
      error.value = response.error.value
    } else {
      devices.value = response.data.value || []
    }
  } catch (e) {
    error.value = 'Failed to load devices'
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  deviceForm.value = {
    name: '',
    device_type: '',
    description: '',
    api_endpoint: '',
    api_token: '',
    is_active: true
  }
  editingDevice.value = null
}

const closeDialog = () => {
  showAddDevice.value = false
  showEditDevice.value = false
  resetForm()
}

const editDevice = (device: Device) => {
  editingDevice.value = device
  deviceForm.value = {
    name: device.name,
    device_type: device.device_type,
    description: device.description || '',
    api_endpoint: device.api_endpoint || '',
    api_token: device.api_token || '',
    is_active: device.is_active
  }
  showEditDevice.value = true
}

const saveDevice = async () => {
  try {
    if (editingDevice.value) {
      const response = await updateDevice(editingDevice.value.id, deviceForm.value)
      if (response.error.value) {
        alert('Error updating device: ' + response.error.value)
        return
      }
    } else {
      const response = await createDevice(deviceForm.value)
      if (response.error.value) {
        alert('Error creating device: ' + response.error.value)
        return
      }
    }
    closeDialog()
    await loadDevices()
  } catch (e) {
    alert('Failed to save device')
  }
}

const toggleStatus = async (device: Device) => {
  try {
    const response = await toggleDeviceStatus(device.id, !device.is_active)
    if (response.error.value) {
      alert('Error toggling device status: ' + response.error.value)
      return
    }
    await loadDevices()
  } catch (e) {
    alert('Failed to toggle device status')
  }
}

const confirmDelete = (device: Device) => {
  deviceToDelete.value = device
  showDeleteConfirm.value = true
}

const deleteDeviceConfirmed = async () => {
  if (!deviceToDelete.value) return
  
  try {
    const response = await deleteDevice(deviceToDelete.value.id)
    if (response.error.value) {
      alert('Error deleting device: ' + response.error.value)
      return
    }
    showDeleteConfirm.value = false
    deviceToDelete.value = null
    await loadDevices()
  } catch (e) {
    alert('Failed to delete device')
  }
}

onMounted(() => {
  loadDevices()
})
</script>