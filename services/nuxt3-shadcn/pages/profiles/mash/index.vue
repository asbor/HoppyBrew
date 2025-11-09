<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

// Define interface for mash profile
interface MashProfile {
  id: string
  name: string
  version: number
  grain_temp: number
  tun_temp: number
  sparge_temp: number
  ph: number
  notes: string
}

const mashProfiles = ref<MashProfile[]>([])
const loading = ref(false)
const error = ref('')

async function fetchMashProfiles() {
  loading.value = true
  error.value = ''
  
  try {
    const response = await fetch('http://localhost:8000/mash', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch mash profiles')
    }
    
    const data = await response.json()
    mashProfiles.value = data
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch mash profiles'
    console.error('Error fetching mash profiles:', err)
  } finally {
    loading.value = false
  }
}

async function deleteMashProfile(id: string, name: string) {
  if (!confirm(`Are you sure you want to delete "${name}"?`)) {
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/mash/${id}`, {
      method: 'DELETE',
    })
    
    if (!response.ok) {
      throw new Error('Failed to delete mash profile')
    }
    
    // Remove from list
    mashProfiles.value = mashProfiles.value.filter((profile) => profile.id !== id)
  } catch (err: any) {
    error.value = err.message || 'Failed to delete mash profile'
    console.error('Error deleting mash profile:', err)
  }
}

onMounted(fetchMashProfiles)
</script>

<template>
  <div class="container mx-auto py-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Mash Profiles</h1>
        <p class="text-muted-foreground">
          Manage your mash schedules and brewing profiles
        </p>
      </div>
      <Button asChild>
        <NuxtLink href="/profiles/mash/newMash">
          Create New Profile
        </NuxtLink>
      </Button>
    </div>

    <!-- Error display -->
    <div v-if="error" class="bg-destructive/10 text-destructive border border-destructive rounded-lg p-4">
      {{ error }}
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-muted-foreground">Loading mash profiles...</p>
    </div>

    <!-- Empty state -->
    <Card v-else-if="mashProfiles.length === 0">
      <CardContent class="py-12 text-center">
        <div class="space-y-4">
          <div class="text-6xl">🍺</div>
          <div>
            <h3 class="text-lg font-semibold">No Mash Profiles Yet</h3>
            <p class="text-muted-foreground mt-2">
              Create your first mash profile to get started
            </p>
          </div>
          <Button asChild>
            <NuxtLink href="/profiles/mash/newMash">
              Create Your First Profile
            </NuxtLink>
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Profiles table -->
    <Card v-else>
      <CardHeader>
        <CardTitle>Your Mash Profiles</CardTitle>
        <CardDescription>
          {{ mashProfiles.length }} profile{{ mashProfiles.length !== 1 ? 's' : '' }} configured
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Grain Temp</TableHead>
              <TableHead>Sparge Temp</TableHead>
              <TableHead>pH</TableHead>
              <TableHead>Notes</TableHead>
              <TableHead class="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="profile in mashProfiles" :key="profile.id">
              <TableCell class="font-medium">
                <NuxtLink 
                  :href="`/profiles/mash/${profile.id}`"
                  class="hover:underline text-primary"
                >
                  {{ profile.name }}
                </NuxtLink>
              </TableCell>
              <TableCell>
                <Badge variant="outline">{{ profile.grain_temp }}°C</Badge>
              </TableCell>
              <TableCell>
                <Badge variant="outline">{{ profile.sparge_temp }}°C</Badge>
              </TableCell>
              <TableCell>
                <Badge variant="outline">{{ profile.ph }}</Badge>
              </TableCell>
              <TableCell class="max-w-xs truncate">
                <span class="text-sm text-muted-foreground">
                  {{ profile.notes || '-' }}
                </span>
              </TableCell>
              <TableCell class="text-right">
                <div class="flex justify-end gap-2">
                  <Button asChild size="sm" variant="outline">
                    <NuxtLink :href="`/profiles/mash/${profile.id}`">
                      Edit
                    </NuxtLink>
                  </Button>
                  <Button 
                    @click="deleteMashProfile(profile.id, profile.name)"
                    size="sm"
                    variant="destructive"
                  >
                    Delete
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </div>
</template>
