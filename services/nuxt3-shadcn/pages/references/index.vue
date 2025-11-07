<script setup lang="ts">
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import XMLImportReferenceDialog from '@/components/XML/ImportReferenceDialog.vue'
import XMLExportReferenceDialog from '@/components/XML/ExportReferenceDialog.vue'

interface Reference {
  id: number
  name: string
  url: string
  description: string
  category: string
  favicon_url: string
}

const DEFAULT_FAVICON_URL = 'https://static-00.iconduck.com/assets.00/unknown-icon-2048x2048-6wlnie9m.png'

const api = useApi()
const router = useRouter()

const references = ref<Reference[]>([])
const searchQuery = ref('')
const filterCategory = ref<string>('all')
const viewMode = ref<'table' | 'cards'>('table')
const loading = ref(false)
const error = ref<string | null>(null)

// Get unique categories
const categories = computed(() => {
  const cats = new Set(references.value.map(ref => ref.category).filter(Boolean))
  return Array.from(cats).sort()
})

// Filtered references
const filteredReferences = computed(() => {
  let result = references.value

  // Filter by category
  if (filterCategory.value !== 'all') {
    result = result.filter(ref => ref.category === filterCategory.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(ref =>
      ref.name.toLowerCase().includes(query) ||
      ref.description?.toLowerCase().includes(query) ||
      ref.url.toLowerCase().includes(query)
    )
  }

  return result
})

async function fetchReferences() {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get<Reference[]>('/references')
    if (response.error.value) {
      error.value = response.error.value
    } else {
      references.value = response.data.value || []
    }
  } catch (err) {
    error.value = 'Failed to fetch references'
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function deleteReference(id: number) {
  if (!confirm('Are you sure you want to delete this reference?')) {
    return
  }

  try {
    const response = await api.delete(`/references/${id}`)
    if (!response.error.value) {
      references.value = references.value.filter(ref => ref.id !== id)
    } else {
      alert(`Failed to delete reference: ${response.error.value}`)
    }
  } catch (err) {
    console.error(err)
    alert('Failed to delete reference')
  }
}

function handleFaviconError(event: Event) {
  const target = event.target as HTMLImageElement
  target.src = DEFAULT_FAVICON_URL
}

function openUrl(url: string) {
  window.open(url, '_blank')
}

onMounted(fetchReferences)
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold">References</h1>
        <p class="text-muted-foreground">Useful brewing resources and links</p>
      </div>
      <div class="flex gap-2 flex-wrap">
        <div class="flex gap-1 border rounded-md">
          <Button 
            variant="ghost" 
            size="sm" 
            :class="{ 'bg-muted': viewMode === 'table' }"
            @click="viewMode = 'table'"
          >
            <Icon name="mdi:table" class="h-4 w-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            :class="{ 'bg-muted': viewMode === 'cards' }"
            @click="viewMode = 'cards'"
          >
            <Icon name="mdi:view-grid" class="h-4 w-4" />
          </Button>
        </div>
        <Button asChild variant="outline" size="sm">
          <XMLImportReferenceDialog />
        </Button>
        <Button asChild variant="outline" size="sm">
          <XMLExportReferenceDialog />
        </Button>
        <Button asChild>
          <NuxtLink href="/references/newReferences">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            New Reference
          </NuxtLink>
        </Button>
      </div>
    </header>

    <!-- Search & Filters -->
    <div class="flex flex-col md:flex-row gap-4">
      <div class="flex-1">
        <Input
          v-model="searchQuery"
          placeholder="Search references by name, description, or URL..."
          class="max-w-md"
        >
          <template #prefix>
            <Icon name="mdi:magnify" class="h-4 w-4 text-muted-foreground" />
          </template>
        </Input>
      </div>
      <div v-if="categories.length > 0" class="flex gap-2 flex-wrap">
        <Button 
          variant="outline" 
          size="sm" 
          :class="{ 'bg-primary text-primary-foreground': filterCategory === 'all' }"
          @click="filterCategory = 'all'"
        >
          All
        </Button>
        <Button 
          v-for="category in categories" 
          :key="category"
          variant="outline" 
          size="sm"
          :class="{ 'bg-primary text-primary-foreground': filterCategory === category }"
          @click="filterCategory = category"
        >
          {{ category }}
        </Button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-muted-foreground">Loading references...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-destructive">{{ error }}</p>
    </div>

    <!-- Empty State -->
    <Card v-else-if="references.length === 0" class="text-center py-12">
      <CardHeader>
        <Icon name="mdi:link-variant" class="mx-auto h-12 w-12 text-muted-foreground" />
        <CardTitle>No references yet</CardTitle>
        <CardDescription>
          Start building your reference library
        </CardDescription>
      </CardHeader>
      <CardFooter class="justify-center">
        <Button asChild>
          <NuxtLink href="/references/newReferences">
            <Icon name="mdi:plus" class="mr-2 h-4 w-4" />
            Add First Reference
          </NuxtLink>
        </Button>
      </CardFooter>
    </Card>

    <!-- Table View -->
    <Card v-else-if="viewMode === 'table'">
      <CardHeader>
        <div class="flex items-center justify-between">
          <div>
            <CardTitle>Reference List</CardTitle>
            <CardDescription>
              {{ filteredReferences.length }} {{ filteredReferences.length === 1 ? 'reference' : 'references' }} found
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead class="w-16">Logo</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>URL</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Category</TableHead>
              <TableHead class="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="reference in filteredReferences" :key="reference.id">
              <TableCell>
                <img 
                  :src="reference.favicon_url || DEFAULT_FAVICON_URL"
                  alt="Favicon" 
                  @error="handleFaviconError"
                  class="w-8 h-8 object-contain"
                >
              </TableCell>
              <TableCell class="font-medium">{{ reference.name }}</TableCell>
              <TableCell>
                <a 
                  :href="reference.url" 
                  target="_blank" 
                  class="text-primary hover:underline inline-flex items-center gap-1"
                >
                  {{ reference.url }}
                  <Icon name="mdi:open-in-new" class="h-3 w-3" />
                </a>
              </TableCell>
              <TableCell>{{ reference.description || 'N/A' }}</TableCell>
              <TableCell>
                <Badge v-if="reference.category" variant="outline">{{ reference.category }}</Badge>
              </TableCell>
              <TableCell class="text-right space-x-2">
                <Button asChild variant="ghost" size="sm">
                  <NuxtLink :href="`/references/${reference.id}`">
                    <Icon name="mdi:pencil" class="h-4 w-4" />
                  </NuxtLink>
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  @click="deleteReference(reference.id)"
                  class="text-destructive hover:text-destructive"
                >
                  <Icon name="mdi:delete" class="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>

    <!-- Card View -->
    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <Card v-for="reference in filteredReferences" :key="reference.id" class="flex flex-col">
        <CardHeader class="pb-3">
          <div class="flex items-start gap-3">
            <img 
              :src="reference.favicon_url || DEFAULT_FAVICON_URL"
              alt="Favicon" 
              @error="handleFaviconError"
              class="w-12 h-12 object-contain shrink-0"
            >
            <div class="flex-1 min-w-0">
              <CardTitle class="text-base line-clamp-2">{{ reference.name }}</CardTitle>
              <Badge v-if="reference.category" variant="outline" class="mt-1 text-xs">
                {{ reference.category }}
              </Badge>
            </div>
          </div>
        </CardHeader>
        
        <CardContent class="flex-1 pb-3">
          <CardDescription class="line-clamp-3 text-sm">
            {{ reference.description || 'No description available' }}
          </CardDescription>
        </CardContent>
        
        <CardFooter class="flex gap-2 pt-3 border-t">
          <Button 
            @click="openUrl(reference.url)" 
            variant="default" 
            size="sm"
            class="flex-1"
          >
            <Icon name="mdi:open-in-new" class="mr-1 h-4 w-4" />
            Visit
          </Button>
          <Button 
            @click="router.push(`/references/${reference.id}`)" 
            variant="outline" 
            size="sm"
          >
            <Icon name="mdi:pencil" class="h-4 w-4" />
          </Button>
          <Button 
            @click="deleteReference(reference.id)" 
            variant="outline" 
            size="sm"
            class="text-destructive hover:text-destructive"
          >
            <Icon name="mdi:delete" class="h-4 w-4" />
          </Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
