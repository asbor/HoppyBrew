<template>
  <div v-if="equipment && equipment.length > 0" class="bg-white rounded-lg border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Equipment Profile</h3>
    
    <div class="space-y-4">
      <div v-for="(profile, index) in equipment" :key="index" class="p-4 bg-gray-50 rounded-lg">
        <h4 class="font-medium text-gray-900 mb-2">{{ profile.name || 'Equipment Profile' }}</h4>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div v-if="profile.batch_size">
            <span class="text-gray-600">Batch Size:</span>
            <span class="ml-2 font-medium">{{ profile.batch_size }} L</span>
          </div>
          <div v-if="profile.boil_size">
            <span class="text-gray-600">Boil Size:</span>
            <span class="ml-2 font-medium">{{ profile.boil_size }} L</span>
          </div>
          <div v-if="profile.efficiency">
            <span class="text-gray-600">Efficiency:</span>
            <span class="ml-2 font-medium">{{ profile.efficiency }}%</span>
          </div>
          <div v-if="profile.loss_to_trub">
            <span class="text-gray-600">Trub Loss:</span>
            <span class="ml-2 font-medium">{{ profile.loss_to_trub }} L</span>
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