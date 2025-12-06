<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
} from '@/components/ui/card'
import BeerGlassIcon from '@/components/recipe/BeerGlassIcon.vue'

const props = defineProps<{
  card?: any
  beer?: any
}>()
const emit = defineEmits(['startBrew', 'edit', 'delete']);

const DESCRIPTION_MAX_LENGTH = 120;

// Truncate description to max length
const cardData = computed(() => props.card || props.beer || {})

const truncatedDescription = computed(() => {
  const description = cardData.value.notes || cardData.value.taste_notes || cardData.value.description || '';
  return description.length > DESCRIPTION_MAX_LENGTH 
    ? description.substring(0, DESCRIPTION_MAX_LENGTH) + '...' 
    : description;
});

function handleStartBrew() {
  emit('startBrew', cardData.value);
}

function handleEdit() {
  emit('edit', cardData.value);
}

function handleDelete() {
  emit('delete', cardData.value);
}

const fallbackSrm = computed(() => cardData.value.est_color || cardData.value.color || cardData.value.srm || null)
</script>

<template>
    <Card class="flex flex-col h-full" @click="$emit('click')">
        <CardHeader class="px-4 pt-4 pb-1">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 flex-1 min-w-0">
                    <div class="shrink-0 w-12 h-12 rounded-md bg-muted flex items-center justify-center overflow-hidden border border-border">
                        <img
                          v-if="cardData.image_url"
                          :src="cardData.image_url"
                          alt="Recipe image"
                          class="w-full h-full object-cover"
                          loading="lazy"
                        />
                        <BeerGlassIcon v-else :srm="fallbackSrm" :size="44" :label="cardData.est_color ? `${cardData.est_color.toFixed(0)} SRM` : ''" />
                    </div>
                    <div class="min-w-0 flex-1">
                        <CardTitle class="truncate">{{ cardData.name }}</CardTitle>
                    </div>
                </div>
                <Badge variant="outline" class="ml-2 shrink-0">{{ cardData.type }}</Badge>
            </div>
            <div class="text-sm text-muted-foreground">
                <p>{{ cardData.brewer }}</p>
            </div>
        </CardHeader>

        <CardContent class="px-4 py-2 flex-1">
            <CardDescription class="line-clamp-4 text-muted-foreground">
                {{ truncatedDescription }}
            </CardDescription>
        </CardContent>
        
        <CardFooter class="flex flex-col gap-3 py-3 px-4">
            <!-- Stats Row -->
            <div class="flex w-full items-center justify-between text-sm text-card-foreground">
                <div class="flex items-center gap-1">
                    <label class="font-bold">ABV:</label>
                    <p>{{ cardData.abv?.toFixed(1) || 'N/A' }}%</p>
                </div>
                <div class="flex items-center gap-1">
                    <label class="font-bold">OG:</label>
                    <p>{{ cardData.og?.toFixed(3) || 'N/A' }}</p>
                </div>
                <div class="flex items-center gap-1">
                    <label class="font-bold">FG:</label>
                    <p>{{ cardData.fg?.toFixed(3) || 'N/A' }}</p>
                </div>
                <div class="flex items-center gap-1">
                    <label class="font-bold">IBU:</label>
                    <p>{{ cardData.ibu?.toFixed(0) || 'N/A' }}</p>
                </div>
            </div>
            
            <!-- Action Buttons Row -->
            <div class="flex w-full gap-2">
                <Button 
                    @click="handleStartBrew" 
                    variant="default" 
                    size="sm" 
                    class="flex-1"
                >
                    <Icon name="mdi:flask" class="mr-1 h-4 w-4" />
                    Start Brew
                </Button>
                <Button 
                    @click="handleEdit" 
                    variant="outline" 
                    size="sm"
                >
                    <Icon name="mdi:pencil" class="h-4 w-4" />
                </Button>
                <Button 
                    @click="handleDelete" 
                    variant="outline" 
                    size="sm"
                    class="text-destructive hover:text-destructive"
                >
                    <Icon name="mdi:delete" class="h-4 w-4" />
                </Button>
            </div>
        </CardFooter>
    </Card>
</template>
