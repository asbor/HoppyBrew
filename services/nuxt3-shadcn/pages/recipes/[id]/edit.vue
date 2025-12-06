<template>
    <div class="container mx-auto py-6 space-y-6">
        <!-- Loading State -->
        <div v-if="isLoading && !recipe" class="flex justify-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
                <p class="mt-4 text-muted-foreground">Loading recipe...</p>
            </div>
        </div>

        <!-- Edit Form -->
        <div v-else-if="recipe" class="space-y-6">
            <!-- Header -->
            <div class="flex items-start justify-between">
                <div class="space-y-1">
                    <div class="flex items-center gap-2">
                        <Button variant="ghost" size="icon" @click="router.back()">
                            <ChevronLeft class="h-5 w-5" />
                        </Button>
                        <h1 class="text-3xl font-bold text-foreground">Edit Recipe</h1>
                    </div>
                    <p class="text-lg text-muted-foreground ml-12">{{ recipe.name }}</p>
                </div>

                <div class="flex space-x-2">
                    <Button variant="outline" @click="router.back()">
                        Cancel
                    </Button>
                    <Button :disabled="saving" @click="saveRecipe">
                        <Icon v-if="saving" name="mdi:loading" class="mr-2 h-4 w-4 animate-spin" />
                        Save Changes
                    </Button>
                </div>
            </div>

            <!-- Edit Form Content -->
            <Card>
                <CardHeader>
                    <CardTitle>Recipe Editor</CardTitle>
                    <CardDescription>This is a placeholder for the recipe editor. Full editing functionality will be
                        implemented soon.</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="space-y-4">
                        <!-- Basic Info -->
                        <div class="grid grid-cols-2 gap-4">
                            <div class="space-y-2">
                                <Label for="name">Recipe Name</Label>
                                <Input id="name" v-model="recipe.name" />
                            </div>
                            <div class="space-y-2">
                                <Label for="type">Type</Label>
                                <Input id="type" v-model="recipe.type" />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div class="space-y-2">
                                <Label for="brewer">Brewer</Label>
                                <Input id="brewer" v-model="recipe.brewer" />
                            </div>
                            <div class="space-y-2">
                                <Label for="batch_size">Batch Size (L)</Label>
                                <Input id="batch_size" v-model.number="recipe.batch_size" type="number" step="0.1" />
                            </div>
                        </div>

                        <div class="space-y-2">
                            <Label for="notes">Notes</Label>
                            <Textarea id="notes" v-model="recipe.notes" rows="4" />
                        </div>

                        <!-- Placeholder for additional sections -->
                        <Alert>
                            <AlertCircle class="h-4 w-4" />
                            <AlertTitle>Under Development</AlertTitle>
                            <AlertDescription>
                                Full recipe editing with ingredient management, fermentation profiles, and equipment
                                settings is coming soon.
                                For now, you can edit basic recipe information above.
                            </AlertDescription>
                        </Alert>
                    </div>
                </CardContent>
            </Card>
        </div>

        <!-- Error State -->
        <Alert v-else variant="destructive">
            <AlertCircle class="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>Failed to load recipe</AlertDescription>
        </Alert>
    </div>
</template>

<script setup lang="ts">
import { ChevronLeft, AlertCircle } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import type { Recipe } from '@/composables/useRecipes'

const route = useRoute()
const router = useRouter()
const { fetchOne, update, loading: recipeLoading } = useRecipes()

const recipeId = route.params.id as string
const recipe = ref<Recipe | null>(null)
const saving = ref(false)
const isLoading = computed(() => recipeLoading.value)

// Load recipe on mount
onMounted(async () => {
    const result = await fetchOne(recipeId)
    if (result.data.value) {
        // Create a copy for editing
        recipe.value = { ...result.data.value }
    } else if (result.error.value) {
        console.error('Failed to load recipe:', result.error.value)
    }
})

// Set page title
useHead({
    title: computed(() => recipe.value ? `Edit ${recipe.value.name}` : 'Edit Recipe')
})

// Save changes
const saveRecipe = async () => {
    if (!recipe.value) return

    saving.value = true
    try {
        const result = await update(recipeId, recipe.value)

        if (result.error.value) {
            alert(`Failed to save recipe: ${result.error.value}`)
        } else {
            // Navigate back to recipe detail
            router.push(`/recipes/${recipeId}`)
        }
    } catch (error) {
        console.error('Error saving recipe:', error)
        alert('Failed to save recipe')
    } finally {
        saving.value = false
    }
}
</script>
