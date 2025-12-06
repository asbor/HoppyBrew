<script>
</script>




<template>
    <div class="container mx-auto p-6 space-y-4">
        <div class="mb-6">
            <h1 class="text-3xl font-bold">Profiles</h1>
            <p class="text-muted-foreground">Manage your brewing profiles and settings</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <NuxtLink
href="/profiles/equipment"
                class="flex items-center hover:bg-accent rounded-lg cursor-pointer p-4 gap-4 border transition-colors">
                <Icon size="40" name="lucide:cooking-pot" />
                <div class="flex flex-col gap-1">
                    <span class="font-medium">Equipment</span>
                    <span class="text-xs text-muted-foreground">Manage equipment repository</span>
                </div>
            </NuxtLink>

            <NuxtLink
href="/profiles/mash"
                class="flex items-center hover:bg-accent rounded-lg cursor-pointer p-4 gap-4 border transition-colors">
                <Icon size="40" name="mi:temperature" />
                <div class="flex flex-col gap-1">
                    <span class="font-medium">Mash</span>
                    <span class="text-xs text-muted-foreground">Manage mash profiles</span>
                </div>
            </NuxtLink>

            <NuxtLink
href="/profiles/fermentation"
                class="flex items-center hover:bg-accent rounded-lg cursor-pointer p-4 gap-4 border transition-colors">
                <Icon size="40" name="material-symbols:fluid-rounded" />
                <div class="flex flex-col gap-1">
                    <span class="font-medium">Fermentation</span>
                    <span class="text-xs text-muted-foreground">Manage fermentation profiles</span>
                </div>
            </NuxtLink>

            <NuxtLink
href="/profiles/water"
                class="flex items-center hover:bg-accent rounded-lg cursor-pointer p-4 gap-4 border transition-colors">
                <Icon size="40" name="ph:drop-fill" />
                <div class="flex flex-col gap-1">
                    <span class="font-medium">Water</span>
                    <span class="text-xs text-muted-foreground">Manage water profiles</span>
                </div>
            </NuxtLink>

            <NuxtLink
href="/profiles/customStyles"
                class="flex items-center hover:bg-accent rounded-lg cursor-pointer p-4 gap-4 border transition-colors">
                <Icon size="40" name="ri:file-list-3-line" />
                <div class="flex flex-col gap-1">
                    <span class="font-medium">Custom Styles</span>
                    <span class="text-xs text-muted-foreground">Manage custom beer styles</span>
                </div>
            </NuxtLink>
        </div>
    </div>
</template>