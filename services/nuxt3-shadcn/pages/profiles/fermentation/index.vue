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
import { useFermentationProfiles, type FermentationProfile } from '@/composables/useFermentationProfiles'

const { getAllProfiles, deleteProfile } = useFermentationProfiles()

const profiles = ref<FermentationProfile[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchProfiles() {
  loading.value = true
  error.value = null
  try {
    const response = await getAllProfiles()
    if (response.error.value) {
      error.value = response.error.value
    } else {
      profiles.value = response.data.value || []
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to fetch profiles'
  } finally {
    loading.value = false
  }
}

async function handleDelete(id: number) {
  if (!confirm('Are you sure you want to delete this fermentation profile?')) {
    return
  }

  try {
    await deleteProfile(id)
    // Remove from local list
    profiles.value = profiles.value.filter((p) => p.id !== id)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to delete profile'
  }
}

function getTotalDays(profile: FermentationProfile): number {
  if (!profile.steps || profile.steps.length === 0) return 0
  return profile.steps.reduce((sum, step) => sum + (step.duration_days || 0), 0)
}

onMounted(fetchProfiles)
</script>

<template>
  <div>
    <header class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-2xl font-semibold">Fermentation Profiles</h1>
        <p class="text-sm text-muted-foreground mt-1">
          Manage temperature schedules and fermentation stages for different beer styles
        </p>
      </div>
      <div>
        <Button asChild>
          <NuxtLink href="/profiles/fermentation/new">New Profile</NuxtLink>
        </Button>
      </div>
    </header>

    <div v-if="error" class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div v-if="loading" class="flex items-center justify-center py-8">
      <p class="text-muted-foreground">Loading profiles...</p>
    </div>

    <Table v-else>
      <TableCaption>A list of your fermentation profiles.</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Description</TableHead>
          <TableHead>Type</TableHead>
          <TableHead>Steps</TableHead>
          <TableHead>Total Days</TableHead>
          <TableHead class="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-if="profiles.length === 0">
          <TableCell colspan="6" class="text-center text-muted-foreground">
            No fermentation profiles found. Create your first profile to get started.
          </TableCell>
        </TableRow>
        <TableRow v-for="profile in profiles" :key="profile.id">
          <TableCell class="font-medium">
            {{ profile.name }}
            <span v-if="profile.is_template" class="ml-2 text-xs bg-primary/10 text-primary px-2 py-0.5 rounded">
              Template
            </span>
          </TableCell>
          <TableCell class="max-w-xs truncate">{{ profile.description || '-' }}</TableCell>
          <TableCell>
            <span v-if="profile.is_pressurized" class="text-sm">Pressurized</span>
            <span v-else class="text-sm text-muted-foreground">Standard</span>
          </TableCell>
          <TableCell>{{ profile.steps?.length || 0 }}</TableCell>
          <TableCell>{{ getTotalDays(profile) }} days</TableCell>
          <TableCell class="text-right">
            <Button asChild variant="outline" size="sm" class="mr-2">
              <NuxtLink :href="`/profiles/fermentation/${profile.id}`">Edit</NuxtLink>
            </Button>
            <Button @click="profile.id && handleDelete(profile.id)" variant="destructive" size="sm" :disabled="!profile.id">Delete</Button>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
