<template>
  <div v-if="water && water.length > 0" class="bg-card rounded-lg border border-border p-6 shadow-sm">
    <h3 class="text-lg font-semibold text-card-foreground mb-4">Water Profile</h3>
    
    <div class="space-y-4">
      <div v-for="(profile, index) in water" :key="index" class="p-4 bg-cyan-100/20 dark:bg-cyan-900/20 rounded-lg">
        <h4 class="font-medium text-cyan-900 dark:text-cyan-200 mb-3">{{ profile.name || 'Water Profile' }}</h4>
        
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div v-if="profile.calcium">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">Calcium (Ca²⁺):</span>
            <div class="text-card-foreground">{{ profile.calcium }} ppm</div>
          </div>
          <div v-if="profile.magnesium">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">Magnesium (Mg²⁺):</span>
            <div class="text-card-foreground">{{ profile.magnesium }} ppm</div>
          </div>
          <div v-if="profile.sodium">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">Sodium (Na⁺):</span>
            <div class="text-card-foreground">{{ profile.sodium }} ppm</div>
          </div>
          <div v-if="profile.chloride">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">Chloride (Cl⁻):</span>
            <div class="text-card-foreground">{{ profile.chloride }} ppm</div>
          </div>
          <div v-if="profile.sulfate">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">Sulfate (SO₄²⁻):</span>
            <div class="text-card-foreground">{{ profile.sulfate }} ppm</div>
          </div>
          <div v-if="profile.bicarbonate">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">Bicarbonate (HCO₃⁻):</span>
            <div class="text-card-foreground">{{ profile.bicarbonate }} ppm</div>
          </div>
          <div v-if="profile.ph">
            <span class="text-cyan-700 dark:text-cyan-300 font-medium">pH:</span>
            <div class="text-card-foreground">{{ profile.ph.toFixed(2) }}</div>
          </div>
        </div>

        <!-- Calculated ratios -->
        <div v-if="profile.calcium && profile.sulfate && profile.chloride" class="mt-4 pt-3 border-t border-cyan-200 dark:border-cyan-800">
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-cyan-700 dark:text-cyan-300 font-medium">Sulfate/Chloride Ratio:</span>
              <div class="text-card-foreground">{{ calculateSulfateChlorideRatio(profile.sulfate, profile.chloride) }}</div>
            </div>
            <div>
              <span class="text-cyan-700 dark:text-cyan-300 font-medium">Total Hardness:</span>
              <div class="text-card-foreground">{{ calculateHardness(profile.calcium, profile.magnesium) }} ppm</div>
            </div>
          </div>
        </div>

        <div v-if="profile.notes" class="mt-3 pt-3 border-t border-cyan-200 dark:border-cyan-800">
          <span class="text-cyan-700 dark:text-cyan-300 font-medium">Notes:</span>
          <p class="mt-1 text-muted-foreground text-sm leading-relaxed">{{ profile.notes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface WaterProfile {
  name?: string
  calcium?: number
  magnesium?: number
  sodium?: number
  chloride?: number
  sulfate?: number
  bicarbonate?: number
  ph?: number
  notes?: string
}

interface Props {
  water: WaterProfile[]
}

defineProps<Props>()

// Calculate sulfate to chloride ratio
const calculateSulfateChlorideRatio = (sulfate?: number, chloride?: number) => {
  if (!sulfate || !chloride || chloride === 0) return 'N/A'
  const ratio = sulfate / chloride
  return ratio.toFixed(1) + ':1'
}

// Calculate total hardness (Ca + Mg)
const calculateHardness = (calcium?: number, magnesium?: number) => {
  const ca = calcium || 0
  const mg = magnesium || 0
  // Convert Mg to Ca equivalent: Mg * 2.5
  const totalHardness = ca + (mg * 2.5)
  return totalHardness.toFixed(0)
}
</script>