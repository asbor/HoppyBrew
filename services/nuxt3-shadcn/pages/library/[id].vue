<script setup lang="ts">
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Star, BookOpen, ExternalLink, ArrowLeft, Pencil, Trash2 } from 'lucide-vue-next'

interface LibraryEntry {
  id: number
  title: string
  author: string
  category: string
  description: string
  isbn?: string
  publisher?: string
  publication_year?: number
  pages?: number
  rating?: number
  cover_url?: string
  purchase_url?: string
  notes?: string
  tags: string[]
  date_added: string
}

const route = useRoute()
const router = useRouter()

const entryId = Number(route.params.id)
const entry = ref<LibraryEntry | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// Sample data (replace with API call)
const sampleLibraryData = [
  {
    id: 1,
    title: "The Complete Joy of Homebrewing",
    author: "Charlie Papazian",
    category: "brewing-basics",
    description: "The classic guide to brewing beer at home, covering everything from basic techniques to advanced brewing methods.",
    isbn: "9780060531058",
    publisher: "William Morrow Cookbooks",
    publication_year: 2014,
    pages: 432,
    rating: 4.5,
    cover_url: "https://images-na.ssl-images-amazon.com/images/I/51VPZcXDH7L.jpg",
    purchase_url: "https://www.amazon.com/Complete-Joy-Homebrewing-Fourth/dp/0060531053",
    notes: "Essential reading for beginners. Great troubleshooting section.",
    tags: ["beginner", "comprehensive", "classic"],
    date_added: "2024-01-15"
  },
  {
    id: 2,
    title: "Designing Great Beers",
    author: "Ray Daniels",
    category: "recipe-development",
    description: "A comprehensive guide to beer recipe formulation and style guidelines.",
    isbn: "9780937381502",
    publisher: "Brewers Publications",
    publication_year: 1996,
    pages: 310,
    rating: 4.8,
    cover_url: "https://images-na.ssl-images-amazon.com/images/I/41ZqYFYQ8ZL.jpg",
    purchase_url: "https://www.amazon.com/Designing-Great-Beers-Ultimate-Classic/dp/0937381500",
    notes: "Deep dive into recipe formulation. Style-by-style analysis.",
    tags: ["recipe", "advanced", "styles"],
    date_added: "2024-02-10"
  }
]

// Category display name
const getCategoryDisplayName = (category: string) => {
  const categoryNames: Record<string, string> = {
    'brewing-basics': 'Brewing Basics',
    'recipe-development': 'Recipe Development',
    'fermentation': 'Fermentation',
    'water-chemistry': 'Water Chemistry',
    'ingredients': 'Ingredients',
    'equipment': 'Equipment',
    'styles': 'Beer Styles',
    'history': 'Brewing History',
    'business': 'Brewing Business',
    'technical': 'Technical Reference'
  }
  return categoryNames[category] || category
}

// Load entry
const loadEntry = async () => {
  loading.value = true
  error.value = null
  
  try {
    // TODO: Replace with actual API call
    // const response = await api.get(`/api/library/${entryId}`)
    // entry.value = response.data
    
    const foundEntry = sampleLibraryData.find(e => e.id === entryId)
    if (foundEntry) {
      entry.value = foundEntry
    } else {
      error.value = 'Library entry not found'
    }
  } catch (err) {
    error.value = 'Failed to load library entry'
    console.error('Error loading library entry:', err)
  } finally {
    loading.value = false
  }
}

// Format rating stars
const formatRating = (rating?: number) => {
  if (!rating) return '—'
  return '★'.repeat(Math.floor(rating)) + (rating % 1 >= 0.5 ? '½' : '') + '☆'.repeat(5 - Math.ceil(rating))
}

// Actions
const handleEdit = () => {
  router.push(`/library/${entryId}/edit`)
}

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this entry?')) {
    // TODO: Implement delete API call
    router.push('/library')
  }
}

const handleBack = () => {
  router.push('/library')
}

// Load data on mount
onMounted(() => {
  loadEntry()
})
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
      <p class="mt-4 text-muted-foreground">Loading library entry...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <Card>
        <CardHeader>
          <CardTitle class="text-destructive">Error</CardTitle>
          <CardDescription>{{ error }}</CardDescription>
        </CardHeader>
        <CardFooter class="justify-center">
          <Button @click="handleBack" variant="outline">
            <ArrowLeft class="mr-2 h-4 w-4" />
            Back to Library
          </Button>
        </CardFooter>
      </Card>
    </div>

    <!-- Entry Detail -->
    <div v-else-if="entry" class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-start">
        <Button @click="handleBack" variant="ghost" size="sm">
          <ArrowLeft class="mr-2 h-4 w-4" />
          Back to Library
        </Button>
        <div class="flex gap-2">
          <Button @click="handleEdit" variant="outline" size="sm">
            <Pencil class="mr-2 h-4 w-4" />
            Edit
          </Button>
          <Button @click="handleDelete" variant="outline" size="sm">
            <Trash2 class="mr-2 h-4 w-4" />
            Delete
          </Button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Left Column - Cover and Quick Info -->
        <div class="space-y-4">
          <Card>
            <CardContent class="p-6 space-y-4">
              <div v-if="entry.cover_url" class="aspect-[2/3] bg-muted rounded-lg overflow-hidden">
                <img :src="entry.cover_url" :alt="entry.title" class="w-full h-full object-cover" />
              </div>
              <div v-else class="aspect-[2/3] bg-muted rounded-lg flex items-center justify-center">
                <BookOpen class="h-12 w-12 text-muted-foreground" />
              </div>
              
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Rating</span>
                  <div class="flex items-center gap-2">
                    <Star class="h-4 w-4 text-yellow-500" />
                    <span class="font-medium">{{ entry.rating || '—' }}</span>
                  </div>
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Pages</span>
                  <span class="font-medium">{{ entry.pages || '—' }}</span>
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-sm text-muted-foreground">Year</span>
                  <span class="font-medium">{{ entry.publication_year }}</span>
                </div>
              </div>

              <Button 
                v-if="entry.purchase_url" 
                @click="window.open(entry.purchase_url, '_blank')"
                class="w-full"
                variant="outline"
              >
                <ExternalLink class="mr-2 h-4 w-4" />
                Purchase Link
              </Button>
            </CardContent>
          </Card>
        </div>

        <!-- Right Column - Details -->
        <div class="md:col-span-2 space-y-6">
          <!-- Title and Category -->
          <div>
            <div class="flex items-start justify-between mb-2">
              <h1 class="text-3xl font-bold">{{ entry.title }}</h1>
              <Badge variant="secondary">{{ getCategoryDisplayName(entry.category) }}</Badge>
            </div>
            <p class="text-xl text-muted-foreground">by {{ entry.author }}</p>
          </div>

          <!-- Description -->
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-muted-foreground">{{ entry.description }}</p>
            </CardContent>
          </Card>

          <!-- Publishing Info -->
          <Card>
            <CardHeader>
              <CardTitle>Publishing Information</CardTitle>
            </CardHeader>
            <CardContent class="space-y-2">
              <div v-if="entry.publisher" class="flex items-center justify-between">
                <span class="text-sm text-muted-foreground">Publisher</span>
                <span class="font-medium">{{ entry.publisher }}</span>
              </div>
              <div v-if="entry.isbn" class="flex items-center justify-between">
                <span class="text-sm text-muted-foreground">ISBN</span>
                <span class="font-mono text-sm">{{ entry.isbn }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-muted-foreground">Date Added</span>
                <span class="font-medium">{{ new Date(entry.date_added).toLocaleDateString() }}</span>
              </div>
            </CardContent>
          </Card>

          <!-- Tags -->
          <Card>
            <CardHeader>
              <CardTitle>Tags</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="flex flex-wrap gap-2">
                <Badge 
                  v-for="tag in entry.tags" 
                  :key="tag" 
                  variant="outline"
                >
                  {{ tag }}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <!-- Notes -->
          <Card v-if="entry.notes">
            <CardHeader>
              <CardTitle>Notes</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-muted-foreground">{{ entry.notes }}</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>
