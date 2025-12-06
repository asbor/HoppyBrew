<script setup lang="ts">
definePageMeta({
  middleware: () => navigateTo('/dashboard')
})
</script>

<template>
  <div class="p-6 text-center text-muted-foreground">
    Redirecting to dashboard...
  </div>
</template>
