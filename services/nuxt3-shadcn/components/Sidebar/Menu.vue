<template>
  <div>
    <header class="flex items-center gap-ha-sm p-ha-sm transition cursor-pointer">
      <Logo />
      <h2 class="font-bold text-ha-base">HoppyBrew</h2>
      <p class="text-ha-xs text-muted-foreground">v1.0.0</p>
    </header>
    <main class="px-ha-sm grow">
      <div class="grid gap-ha-xs">
        <DropDownCreate />
        <NuxtLink :href="item.path" v-for='(item, index) in items' :key='index'
          class="flex items-center gap-ha-sm px-ha-sm py-ha-xs transition rounded cursor-pointer hover:bg-accent hover:text-accent-foreground">
          <Icon size="24" :name="item.icon" />
          <span class="text-ha-base">{{ item.title }}</span>
          <!-- Add @click event to call handleLinkClick function -->
        </NuxtLink>
      </div>
    </main>
    <footer>
      <div>
        <div class="p-ha-sm">
          <button @click="toggleDark()" class="flex items-center gap-ha-sm text-ha-base">
            <Icon size="24" :name="isDark.value ? 'bx:bx-moon' : 'bx:bx-sun'" />
            <span>Toggle Color Mode</span>
          </button>
          <CheckDatabaseConnection />
        </div>
        <UserAccountUserItem />
      </div>
    </footer>
  </div>
</template>

<script setup>
props: {
  closeOverlay: Function
};

import { defineEmits } from 'vue';

defineEmits(['linkClicked']);

import Button from '../ui/button/Button.vue';

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
  // Styles
  { title: "Styles", path: "/styles", icon: "ri:file-list-3-line" },
  // Tools
  { title: "Tools", path: "/tools", icon: "ri:tools-line" },
  // Settings
  { title: "Settings", path: "/settings", icon: "ri:settings-3-line" },
  // Log
  { title: "Log", path: "/log", icon: "ri:file-list-3-line" },
])

import { useDark, useToggle } from "@vueuse/core";

const isDark = useDark();
const toggleDark = useToggle(isDark);


</script>
