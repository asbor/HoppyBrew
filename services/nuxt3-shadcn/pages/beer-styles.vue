<script setup lang="ts">
import { ref } from 'vue'
import { PlusCircle, BookOpen } from 'lucide-vue-next'
import StyleBrowser from '~/components/StyleBrowser.vue'
import StyleEditor from '~/components/StyleEditor.vue'
import { Button } from '@/components/ui/button'
import type { BeerStyle } from '~/composables/useBeerStyles'

// View state
const currentView = ref<'browser' | 'editor'>('browser')
const editingStyleId = ref<number | undefined>(undefined)

// Handlers
const handleCreateNew = () => {
  editingStyleId.value = undefined
  currentView.value = 'editor'
}

const handleStyleSaved = (style: BeerStyle) => {
  console.log('Style saved:', style)
  currentView.value = 'browser'
  editingStyleId.value = undefined
}

const handleCancelled = () => {
  currentView.value = 'browser'
  editingStyleId.value = undefined
}
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Navigation Bar -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <Button
          :variant="currentView === 'browser' ? 'default' : 'outline'"
          @click="currentView = 'browser'"
        >
          <BookOpen class="mr-2 h-4 w-4" />
          Browse Styles
        </Button>
        <Button
          :variant="currentView === 'editor' ? 'default' : 'outline'"
          @click="handleCreateNew"
        >
          <PlusCircle class="mr-2 h-4 w-4" />
          Create Custom Style
        </Button>
      </div>
    </div>

    <!-- Content Area -->
    <div v-if="currentView === 'browser'">
      <StyleBrowser />
    </div>
    
    <div v-else-if="currentView === 'editor'">
      <StyleEditor
        :style-id="editingStyleId"
        @saved="handleStyleSaved"
        @cancelled="handleCancelled"
      />
    </div>
  </div>
</template>
