<template>
  <div v-if="equipment && equipment.length > 0" class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-card-foreground mb-4">Equipment Profile</h3>
    
    <div class="space-y-4">
      <div v-for="(profile, index) in equipment" :key="index" class="p-4 bg-muted/50 rounded-lg">
        <h4 class="font-medium text-card-foreground mb-2">{{ profile.name || 'Equipment Profile' }}</h4>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div v-if="profile.batch_size">
            <span class="text-muted-foreground">Batch Size:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ profile.batch_size }} L</span>
          </div>
          <div v-if="profile.boil_size">
            <span class="text-muted-foreground">Boil Size:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ profile.boil_size }} L</span>
          </div>
          <div v-if="profile.efficiency">
            <span class="text-muted-foreground">Efficiency:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ profile.efficiency }}%</span>
          </div>
          <div v-if="profile.loss_to_trub">
            <span class="text-muted-foreground">Trub Loss:</span>
            <span class="ml-2 font-medium text-card-foreground">{{ profile.loss_to_trub }} L</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface EquipmentProfile {
  name?: string
  batch_size?: number
  boil_size?: number
  efficiency?: number
  loss_to_trub?: number
}

interface Props {
  equipment: EquipmentProfile[]
}

defineProps<Props>()
</script>