<script setup lang="ts">
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Star, BookOpen, Search, Plus, Filter, Grid3X3, List, ExternalLink } from 'lucide-vue-next'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

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

const api = useApi()
const router = useRouter()

// State
const libraryEntries = ref<LibraryEntry[]>([])
const searchQuery = ref('')
const filterCategory = ref<string>('all')
const sortBy = ref<string>('title')
const viewMode = ref<'table' | 'cards'>('cards')
const loading = ref(false)
const error = ref<string | null>(null)

// Sample library data (replace with API calls)
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
  },
  {
    id: 3,
    title: "Yeast: The Practical Guide to Beer Fermentation",
    author: "Chris White & Jamil Zainasheff",
    category: "fermentation",
    description: "Everything you need to know about yeast and fermentation for better beer.",
    isbn: "9780937381960",
    publisher: "Brewers Publications",
    publication_year: 2010,
    pages: 312,
    rating: 4.7,
    cover_url: "https://images-na.ssl-images-amazon.com/images/I/51PvQQvY9QL.jpg",
    purchase_url: "https://www.amazon.com/Yeast-Practical-Guide-Beer-Fermentation/dp/0937381969",
    notes: "Comprehensive yeast guide. Essential for understanding fermentation.",
    tags: ["yeast", "fermentation", "technical"],
    date_added: "2024-03-05"
  },
  {
    id: 4,
    title: "Water: A Comprehensive Guide for Brewers",
    author: "John Palmer & Colin Kaminski",
    category: "water-chemistry",
    description: "Understanding water chemistry and its impact on beer quality.",
    isbn: "9780937381908",
    publisher: "Brewers Publications",
    publication_year: 2013,
    pages: 295,
    rating: 4.6,
    cover_url: "https://images-na.ssl-images-amazon.com/images/I/51ZxR9KDa8L.jpg",
    purchase_url: "https://www.amazon.com/Water-Comprehensive-Guide-Brewers/dp/0937381900",
    notes: "Deep dive into water chemistry. Can be technical but very informative.",
    tags: ["water", "chemistry", "technical"],
    date_added: "2024-01-28"
  },
  {
    id: 5,
    title: "The Brewing Elements Series: Hops",
    author: "Stan Hieronymus",
    category: "ingredients",
    description: "A comprehensive look at hop varieties, selection, and usage in brewing.",
    isbn: "9780937381885",
    publisher: "Brewers Publications",
    publication_year: 2012,
    pages: 206,
    rating: 4.4,
    cover_url: "https://images-na.ssl-images-amazon.com/images/I/51EQqGzCt4L.jpg",
    purchase_url: "https://www.amazon.com/Brewing-Elements-Hops-Stan-Hieronymus/dp/0937381888",
    notes: "Great reference for hop varieties and characteristics.",
    tags: ["hops", "ingredients", "reference"],
    date_added: "2024-02-22"
  }
]

// Categories
const categories = computed(() => {
  const cats = new Set(libraryEntries.value.map(entry => entry.category).filter(Boolean))
  return Array.from(cats).sort()
})

// Filtered and sorted entries
const filteredEntries = computed(() => {
  let result = [...libraryEntries.value]

  // Filter by category
  if (filterCategory.value !== 'all') {
    result = result.filter(entry => entry.category === filterCategory.value)
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(entry => 
      entry.title.toLowerCase().includes(query) ||
      entry.author.toLowerCase().includes(query) ||
      entry.description.toLowerCase().includes(query) ||
      entry.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  // Sort entries
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'title':
        return a.title.localeCompare(b.title)
      case 'author':
        return a.author.localeCompare(b.author)
      case 'rating':
        return (b.rating || 0) - (a.rating || 0)
      case 'date_added':
        return new Date(b.date_added).getTime() - new Date(a.date_added).getTime()
      default:
        return 0
    }
  })

  return result
})

// Load library entries
const loadLibraryEntries = async () => {
  loading.value = true
  error.value = null
  
  try {
    // For now, use sample data
    // TODO: Replace with actual API call
    // const response = await api.get('/api/library')
    // libraryEntries.value = response.data
    
    libraryEntries.value = sampleLibraryData
  } catch (err) {
    error.value = 'Failed to load library entries'
    console.error('Error loading library entries:', err)
  } finally {
    loading.value = false
  }
}

// Format rating stars
const formatRating = (rating?: number) => {
  if (!rating) return '—'
  return '★'.repeat(Math.floor(rating)) + (rating % 1 >= 0.5 ? '½' : '') + '☆'.repeat(5 - Math.ceil(rating))
}

// Navigate to entry detail
const viewEntry = (id: number) => {
  // TODO: Implement library detail page
  console.log('View library entry:', id)
  // router.push(`/library/${id}`)
}

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

// Load data on mount
onMounted(() => {
  loadLibraryEntries()
})
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
          <BookOpen class="h-8 w-8 text-primary" />
          Brewing Library
        </h1>
        <p class="text-muted-foreground">
          Your collection of brewing books, guides, and resources
        </p>
      </div>
      <div class="flex gap-2">
        <Button 
          @click="viewMode = viewMode === 'cards' ? 'table' : 'cards'"
          aria-label="Toggle library view"
          variant="outline"
          size="sm"
        >
          <Grid3X3 v-if="viewMode === 'table'" class="h-4 w-4" />
          <List v-else class="h-4 w-4" />
        </Button>
        <Button @click="router.push('/library/add')" class="flex items-center gap-2">
          <Plus class="h-4 w-4" />
          Add Entry
        </Button>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="flex flex-col sm:flex-row gap-4 items-center">
      <div class="relative flex-1 max-w-sm">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
        <Input
          v-model="searchQuery"
          placeholder="Search by title, author, description, or tags..."
          class="pl-10"
        />
      </div>
      
      <div class="flex items-center gap-2">
        <Filter class="h-4 w-4 text-muted-foreground" />
        <Select v-model="filterCategory">
          <SelectTrigger class="w-48">
            <SelectValue placeholder="All Categories" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem v-for="category in categories" :key="category" :value="category">
              {{ getCategoryDisplayName(category) }}
            </SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="sortBy">
          <SelectTrigger class="w-32">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="title">Title</SelectItem>
            <SelectItem value="author">Author</SelectItem>
            <SelectItem value="rating">Rating</SelectItem>
            <SelectItem value="date_added">Date Added</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Results Summary -->
    <div class="text-sm text-muted-foreground">
      Showing {{ filteredEntries.length }} of {{ libraryEntries.length }} entries
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
      <p class="mt-4 text-muted-foreground">Loading library entries...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-destructive">{{ error }}</p>
      <Button @click="loadLibraryEntries()" class="mt-4">Try Again</Button>
    </div>

    <!-- Cards View -->
    <div v-else-if="viewMode === 'cards'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card 
        v-for="entry in filteredEntries" 
        :key="entry.id" 
        class="cursor-pointer hover:shadow-lg transition-shadow"
        @click="viewEntry(entry.id)"
      >
        <CardHeader class="pb-3">
          <div class="flex justify-between items-start gap-2">
            <div class="flex-1">
              <CardTitle class="text-lg">{{ entry.title }}</CardTitle>
              <CardDescription>by {{ entry.author }}</CardDescription>
            </div>
            <Badge variant="secondary">{{ getCategoryDisplayName(entry.category) }}</Badge>
          </div>
        </CardHeader>
        
        <CardContent class="space-y-3">
          <p class="text-sm text-muted-foreground line-clamp-3">{{ entry.description }}</p>
          
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Star class="h-4 w-4 text-yellow-500" />
              <span class="text-sm">{{ entry.rating || '—' }}</span>
            </div>
            <div class="text-xs text-muted-foreground">
              {{ entry.publication_year }}
            </div>
          </div>

          <div class="flex flex-wrap gap-1">
            <Badge 
              v-for="tag in entry.tags.slice(0, 3)" 
              :key="tag" 
              variant="outline" 
              class="text-xs"
            >
              {{ tag }}
            </Badge>
            <Badge v-if="entry.tags.length > 3" variant="outline" class="text-xs">
              +{{ entry.tags.length - 3 }}
            </Badge>
          </div>
        </CardContent>

        <CardFooter class="pt-3">
          <div class="flex gap-2 w-full">
            <Button variant="outline" size="sm" class="flex-1">
              View Details
            </Button>
            <Button 
              v-if="entry.purchase_url" 
              variant="outline" 
              size="sm"
              @click.stop="() => { if (typeof window !== 'undefined') window.open(entry.purchase_url, '_blank') }"
            >
              <ExternalLink class="h-3 w-3" />
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>

    <!-- Table View -->
    <div v-else class="rounded-md border">
      <Table>
        <TableCaption>Your brewing library collection</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Title</TableHead>
            <TableHead>Author</TableHead>
            <TableHead>Category</TableHead>
            <TableHead>Rating</TableHead>
            <TableHead>Year</TableHead>
            <TableHead>Tags</TableHead>
            <TableHead class="w-[100px]">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow 
            v-for="entry in filteredEntries" 
            :key="entry.id"
            class="cursor-pointer hover:bg-muted/50"
            @click="viewEntry(entry.id)"
          >
            <TableCell class="font-medium">{{ entry.title }}</TableCell>
            <TableCell>{{ entry.author }}</TableCell>
            <TableCell>
              <Badge variant="secondary">{{ getCategoryDisplayName(entry.category) }}</Badge>
            </TableCell>
            <TableCell>
              <div class="flex items-center gap-1">
                <Star class="h-3 w-3 text-yellow-500" />
                {{ entry.rating || '—' }}
              </div>
            </TableCell>
            <TableCell>{{ entry.publication_year }}</TableCell>
            <TableCell>
              <div class="flex flex-wrap gap-1">
                <Badge 
                  v-for="tag in entry.tags.slice(0, 2)" 
                  :key="tag" 
                  variant="outline" 
                  class="text-xs"
                >
                  {{ tag }}
                </Badge>
                <Badge v-if="entry.tags.length > 2" variant="outline" class="text-xs">
                  +{{ entry.tags.length - 2 }}
                </Badge>
              </div>
            </TableCell>
            <TableCell>
              <Button variant="outline" size="sm" @click.stop="viewEntry(entry.id)">
                View
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && filteredEntries.length === 0" class="text-center py-12">
      <BookOpen class="h-12 w-12 text-muted-foreground mx-auto mb-4" />
      <h3 class="text-lg font-medium">No library entries found</h3>
      <p class="text-muted-foreground mt-2">
        {{ searchQuery || filterCategory !== 'all' ? 'Try adjusting your filters' : 'Start building your brewing library' }}
      </p>
      <Button @click="router.push('/library/add')" class="mt-4">
        <Plus class="h-4 w-4 mr-2" />
        Add First Entry
      </Button>
    </div>
  </div>
</template>
