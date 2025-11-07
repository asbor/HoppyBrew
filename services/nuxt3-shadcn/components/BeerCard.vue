<script setup lang="ts">
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from '@/components/ui/card';

const props = defineProps(["card"]);
const emit = defineEmits(['startBrew', 'edit', 'delete']);

const DESCRIPTION_MAX_LENGTH = 120;

// Truncate description to max length
const truncatedDescription = computed(() => {
  const description = props.card.notes || props.card.taste_notes || '';
  return description.length > DESCRIPTION_MAX_LENGTH 
    ? description.substring(0, DESCRIPTION_MAX_LENGTH) + '...' 
    : description;
});

function handleStartBrew() {
  emit('startBrew', props.card);
}

function handleEdit() {
  emit('edit', props.card);
}

function handleDelete() {
  emit('delete', props.card);
}
</script>

<template>
    <Card class="flex flex-col h-full">
        <CardHeader class="px-4 pt-4 pb-1">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 flex-1 min-w-0">
                    <Icon size="40" name="mdi:beer" color="yellow" class="shrink-0" />
                    <div class="min-w-0 flex-1">
                        <CardTitle class="truncate">{{ card.name }}</CardTitle>
                    </div>
                </div>
                <Badge variant="outline" class="ml-2 shrink-0">{{ card.type }}</Badge>
            </div>
            <div class="text-sm text-muted-foreground">
                <p>{{ card.brewer }}</p>
            </div>
        </CardHeader>

        <CardContent class="px-4 py-2 flex-1">
            <CardDescription class="line-clamp-4">
                {{ truncatedDescription }}
            </CardDescription>
        </CardContent>
        
        <CardFooter class="flex flex-col gap-3 py-3 px-4">
            <!-- Stats Row -->
            <div class="flex w-full items-center justify-between text-sm">
                <div class="flex items-center gap-1">
                    <label class="font-bold">ABV:</label>
                    <p>{{ card.abv?.toFixed(1) || 'N/A' }}%</p>
                </div>
                <div class="flex items-center gap-1">
                    <label class="font-bold">OG:</label>
                    <p>{{ card.og?.toFixed(3) || 'N/A' }}</p>
                </div>
                <div class="flex items-center gap-1">
                    <label class="font-bold">FG:</label>
                    <p>{{ card.fg?.toFixed(3) || 'N/A' }}</p>
                </div>
                <div class="flex items-center gap-1">
                    <label class="font-bold">IBU:</label>
                    <p>{{ card.ibu?.toFixed(0) || 'N/A' }}</p>
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