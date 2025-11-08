<template>
  <div>
    <header class="flex items-center gap-2 p-4 transition cursor-pointer">
      <Logo />
      <h2 class="font-bold text-base">HoppyBrew</h2>
      <p class="text-xs text-muted-foreground">v1.0.0</p>
    </header>
    <main class="px-4 grow">
      <div class="grid gap-1">
        <DropDownCreate v-if="false" />
        <NuxtLink :to="item.path" v-for='(item, index) in items' :key='index'
          class="flex items-center gap-2 px-4 py-2 transition rounded cursor-pointer hover:bg-accent hover:text-accent-foreground">
          <Icon size="24" :name="item.icon" />
          <span class="text-base">{{ item.title }}</span>
        </NuxtLink>
      </div>
    </main>
    <footer>
      <div>
        <div class="p-4">
          <button @click="toggleDark()" class="flex items-center gap-2 text-base">
            <Icon size="24" :name="isDark ? 'bx:bx-moon' : 'bx:bx-sun'" />
            <span>Toggle Color Mode</span>
          </button>
          <CheckDatabaseConnection />
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDark, useToggle } from '@vueuse/core'

interface Props {
  closeOverlay?: Function
}

defineProps<Props>()

interface Emits {
  linkClicked: []
}

defineEmits<Emits>()

const items = ref([
  // Dashboard
  { title: "Dashboard", path: "/", icon: "ri:dashboard-line" },
  // Beer brewing recipe
  { title: "Recipes", path: "/recipes", icon: "lucide:book-open-text" },
  // Beer brewing batches
  { title: "Batches", path: "/batches", icon: "lucide:beer" },
  // Inventory
  { title: "Inventory", path: "/inventory", icon: "lucide:clipboard-list" },
  // References
  { title: "References", path: "/references", icon: "lucide:store" },
  // Library
  { title: "Library", path: "/library", icon: "lucide:library-big" },
  // Profiles
  { title: "Profiles", path: "/profiles", icon: "ri:contacts-line" },
  // Beer Styles
  { title: "Beer Styles", path: "/beer-styles", icon: "ri:file-list-3-line" },
  // Tools
  { title: "Tools", path: "/tools", icon: "ri:tools-line" },
  // Settings
  { title: "Settings", path: "/settings", icon: "ri:settings-3-line" },
  // Log
  { title: "Log", path: "/log", icon: "ri:file-list-3-line" },
])

const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>
