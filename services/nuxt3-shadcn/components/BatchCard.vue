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
import type { Batch } from '@/composables/useBatches';

const props = defineProps<{
  batch: Batch
}>();

const emit = defineEmits(['edit', 'delete']);

const { getBatchStatusColor } = useStatusColors();
const { formatDate } = useFormatters();

// Calculate days in current stage
const daysInStage = computed(() => {
  const statusDate = props.batch.fermentation_start_date || props.batch.brew_date || props.batch.created_at;
  if (!statusDate) return 0;
  
  const now = new Date();
  const start = new Date(statusDate);
  const diffTime = Math.abs(now.getTime() - start.getTime());
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
});

// Format brew date
const formattedBrewDate = computed(() => {
  const dateString = props.batch.brew_date || props.batch.created_at;
  return formatDate(dateString);
});

function handleEdit() {
  emit('edit', props.batch);
}

function handleDelete() {
  emit('delete', props.batch);
}
</script>

<template>
    <Card class="flex flex-col h-full">
        <CardHeader class="px-4 pt-4 pb-2">
            <div class="flex items-start justify-between gap-2">
                <div class="flex items-center gap-2 flex-1 min-w-0">
                    <Icon size="40" name="mdi:beer" class="text-primary shrink-0" />
                    <div class="min-w-0 flex-1">
                        <CardTitle class="text-base line-clamp-2">{{ batch.batch_name }}</CardTitle>
                    </div>
                </div>
            </div>
            <div class="flex items-center gap-2 mt-2">
                <Badge :class="getBatchStatusColor(batch.status)" class="text-white text-xs">
                    {{ batch.status ? batch.status.replace(/_/g, ' ') : 'N/A' }}
                </Badge>
                <span class="text-xs text-muted-foreground">
                    {{ batch.batch_size }} L
                </span>
            </div>
        </CardHeader>

        <CardContent class="px-4 py-3 flex-1">
            <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                    <span class="text-muted-foreground">Brew Date:</span>
                    <span class="font-medium">{{ formattedBrewDate }}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-muted-foreground">Days in Stage:</span>
                    <span class="font-medium">{{ daysInStage }} days</span>
                </div>
                <div v-if="batch.og" class="flex justify-between">
                    <span class="text-muted-foreground">OG:</span>
                    <span class="font-medium">{{ batch.og.toFixed(3) }}</span>
                </div>
                <div v-if="batch.fg" class="flex justify-between">
                    <span class="text-muted-foreground">FG:</span>
                    <span class="font-medium">{{ batch.fg.toFixed(3) }}</span>
                </div>
                <div v-if="batch.abv" class="flex justify-between">
                    <span class="text-muted-foreground">ABV:</span>
                    <span class="font-medium">{{ batch.abv.toFixed(1) }}%</span>
                </div>
            </div>
        </CardContent>
        
        <CardFooter class="flex gap-2 py-3 px-4 border-t">
            <Button 
                @click="handleEdit" 
                variant="default" 
                size="sm"
                class="flex-1"
            >
                <Icon name="mdi:eye" class="mr-1 h-4 w-4" />
                View Details
            </Button>
            <Button 
                @click="handleDelete" 
                variant="outline" 
                size="sm"
                class="text-destructive hover:text-destructive"
            >
                <Icon name="mdi:delete" class="h-4 w-4" />
            </Button>
        </CardFooter>
    </Card>
</template>
