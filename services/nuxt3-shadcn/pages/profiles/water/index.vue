<template>
  <div class="grid w-full gap-4 p-4">
    <!-- Error notification -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Error: </strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <header class="flex items-start justify-between">
      <div class="grow">
        <h1 class="text-2xl font-bold">Water Profiles</h1>
        <p class="text-neutral-500">Manage your brewing water profiles</p>
      </div>
      <div class="flex gap-2">
        <button
          @click="showCreateDialog = true"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + New Profile
        </button>
      </div>
    </header>

    <!-- Filters -->
    <div class="flex gap-4 items-center bg-white p-4 rounded shadow">
      <div class="flex gap-2">
        <button
          @click="filterType = 'all'"
          :class="['px-4 py-2 rounded', filterType === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200']"
        >
          All
        </button>
        <button
          @click="filterType = 'source'"
          :class="['px-4 py-2 rounded', filterType === 'source' ? 'bg-blue-600 text-white' : 'bg-gray-200']"
        >
          Source
        </button>
        <button
          @click="filterType = 'target'"
          :class="['px-4 py-2 rounded', filterType === 'target' ? 'bg-blue-600 text-white' : 'bg-gray-200']"
        >
          Target
        </button>
      </div>
      <div class="flex gap-2">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="showDefaultOnly" />
          <span>Default profiles only</span>
        </label>
      </div>
    </div>

    <!-- Profiles List -->
    <main>
      <div v-if="loading" class="text-center py-8">
        <p>Loading water profiles...</p>
      </div>

      <div v-else-if="filteredProfiles.length === 0" class="text-center py-8 bg-white rounded shadow">
        <p class="text-neutral-500">No water profiles found. Create one to get started!</p>
      </div>

      <div v-else class="grid gap-4 lg:grid-cols-3 md:grid-cols-2">
        <div
          v-for="profile in filteredProfiles"
          :key="profile.id"
          class="bg-white rounded shadow p-4 hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-start mb-2">
            <div>
              <h3 class="font-semibold text-lg">{{ profile.name }}</h3>
              <div class="flex gap-2 mt-1">
                <span
                  :class="[
                    'text-xs px-2 py-1 rounded',
                    profile.profile_type === 'source' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                  ]"
                >
                  {{ profile.profile_type }}
                </span>
                <span v-if="profile.is_default" class="text-xs px-2 py-1 rounded bg-yellow-100 text-yellow-800">
                  Default
                </span>
              </div>
            </div>
            <div class="flex gap-2">
              <button
                @click="viewProfile(profile)"
                class="text-blue-600 hover:text-blue-800"
                title="View details"
              >
                <Icon name="lucide:eye" size="20" />
              </button>
              <button
                @click="duplicateProfile(profile.id)"
                class="text-gray-600 hover:text-gray-800"
                title="Duplicate"
              >
                <Icon name="lucide:copy" size="20" />
              </button>
              <button
                v-if="!profile.is_default"
                @click="editProfile(profile)"
                class="text-green-600 hover:text-green-800"
                title="Edit"
              >
                <Icon name="lucide:edit" size="20" />
              </button>
              <button
                v-if="!profile.is_default"
                @click="confirmDelete(profile)"
                class="text-red-600 hover:text-red-800"
                title="Delete"
              >
                <Icon name="lucide:trash" size="20" />
              </button>
            </div>
          </div>

          <p v-if="profile.description" class="text-sm text-neutral-600 mb-3">
            {{ profile.description }}
          </p>

          <p v-if="profile.style_category" class="text-xs text-neutral-500 mb-3">
            Style: {{ profile.style_category }}
          </p>

          <div class="grid grid-cols-2 gap-2 text-sm">
            <div class="flex justify-between">
              <span class="text-neutral-600">Ca²⁺:</span>
              <span class="font-mono">{{ profile.calcium }} ppm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">Mg²⁺:</span>
              <span class="font-mono">{{ profile.magnesium }} ppm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">Na⁺:</span>
              <span class="font-mono">{{ profile.sodium }} ppm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">Cl⁻:</span>
              <span class="font-mono">{{ profile.chloride }} ppm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">SO₄²⁻:</span>
              <span class="font-mono">{{ profile.sulfate }} ppm</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-600">HCO₃⁻:</span>
              <span class="font-mono">{{ profile.bicarbonate }} ppm</span>
            </div>
          </div>

          <div v-if="profile.sulfate && profile.chloride && profile.chloride > 0" class="mt-2 pt-2 border-t">
            <div class="flex justify-between text-sm">
              <span class="text-neutral-600">SO₄:Cl ratio:</span>
              <span class="font-mono">{{ (profile.sulfate / profile.chloride).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Create/Edit Dialog -->
    <div v-if="showCreateDialog || selectedProfile" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-bold mb-4">
          {{ selectedProfile ? 'Edit Water Profile' : 'Create Water Profile' }}
        </h2>

        <form @submit.prevent="saveProfile">
          <div class="grid gap-4">
            <div>
              <label class="block text-sm font-medium mb-1">Name *</label>
              <input
                v-model="formData.name"
                type="text"
                required
                class="w-full border rounded px-3 py-2"
                placeholder="e.g., My Custom Profile"
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Description</label>
              <textarea
                v-model="formData.description"
                class="w-full border rounded px-3 py-2"
                rows="2"
                placeholder="Describe this water profile..."
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Profile Type *</label>
                <select
                  v-model="formData.profile_type"
                  required
                  class="w-full border rounded px-3 py-2"
                >
                  <option value="source">Source Water</option>
                  <option value="target">Target Profile</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium mb-1">Style Category</label>
                <input
                  v-model="formData.style_category"
                  type="text"
                  class="w-full border rounded px-3 py-2"
                  placeholder="e.g., IPA, Stout"
                />
              </div>
            </div>

            <div class="border-t pt-4">
              <h3 class="font-semibold mb-3">Ion Concentrations (ppm)</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-1">Calcium (Ca²⁺)</label>
                  <input
                    v-model.number="formData.calcium"
                    type="number"
                    step="0.01"
                    min="0"
                    class="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">Magnesium (Mg²⁺)</label>
                  <input
                    v-model.number="formData.magnesium"
                    type="number"
                    step="0.01"
                    min="0"
                    class="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">Sodium (Na⁺)</label>
                  <input
                    v-model.number="formData.sodium"
                    type="number"
                    step="0.01"
                    min="0"
                    class="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">Chloride (Cl⁻)</label>
                  <input
                    v-model.number="formData.chloride"
                    type="number"
                    step="0.01"
                    min="0"
                    class="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">Sulfate (SO₄²⁻)</label>
                  <input
                    v-model.number="formData.sulfate"
                    type="number"
                    step="0.01"
                    min="0"
                    class="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1">Bicarbonate (HCO₃⁻)</label>
                  <input
                    v-model.number="formData.bicarbonate"
                    type="number"
                    step="0.01"
                    min="0"
                    class="w-full border rounded px-3 py-2"
                  />
                </div>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">pH</label>
              <input
                v-model.number="formData.ph"
                type="number"
                step="0.01"
                min="0"
                max="14"
                class="w-full border rounded px-3 py-2"
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Notes</label>
              <textarea
                v-model="formData.notes"
                class="w-full border rounded px-3 py-2"
                rows="2"
                placeholder="Additional notes..."
              ></textarea>
            </div>
          </div>

          <div class="flex gap-2 justify-end mt-6">
            <button
              type="button"
              @click="closeDialog"
              class="px-4 py-2 border rounded hover:bg-gray-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {{ selectedProfile ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation -->
    <div v-if="profileToDelete" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md">
        <h2 class="text-xl font-bold mb-4">Confirm Delete</h2>
        <p class="mb-4">
          Are you sure you want to delete "{{ profileToDelete.name }}"? This action cannot be undone.
        </p>
        <div class="flex gap-2 justify-end">
          <button
            @click="profileToDelete = null"
            class="px-4 py-2 border rounded hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            @click="deleteProfile"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profiles: [],
      loading: false,
      filterType: 'all',
      showDefaultOnly: false,
      showCreateDialog: false,
      selectedProfile: null,
      profileToDelete: null,
      formData: this.getEmptyFormData(),
      error: null,
    };
  },
  computed: {
    filteredProfiles() {
      let filtered = this.profiles;

      if (this.filterType !== 'all') {
        filtered = filtered.filter(p => p.profile_type === this.filterType);
      }

      if (this.showDefaultOnly) {
        filtered = filtered.filter(p => p.is_default);
      }

      return filtered;
    },
    apiBaseUrl() {
      const config = useRuntimeConfig();
      return config.public.API_URL || 'http://localhost:8000';
    }
  },
  async created() {
    await this.fetchProfiles();
  },
  methods: {
    getEmptyFormData() {
      return {
        name: '',
        description: '',
        profile_type: 'source',
        style_category: '',
        calcium: 0,
        magnesium: 0,
        sodium: 0,
        chloride: 0,
        sulfate: 0,
        bicarbonate: 0,
        ph: null,
        notes: '',
      };
    },
    showError(message) {
      this.error = message;
      setTimeout(() => { this.error = null; }, 5000);
    },
    async fetchProfiles() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch(`${this.apiBaseUrl}/water-profiles`);
        if (!response.ok) throw new Error('Failed to fetch profiles');
        this.profiles = await response.json();
      } catch (error) {
        console.error('Error fetching water profiles:', error);
        this.showError('Failed to load water profiles. Please try again.');
      } finally {
        this.loading = false;
      }
    },
    async saveProfile() {
      this.error = null;
      try {
        const url = this.selectedProfile
          ? `${this.apiBaseUrl}/water-profiles/${this.selectedProfile.id}`
          : `${this.apiBaseUrl}/water-profiles`;

        const method = this.selectedProfile ? 'PUT' : 'POST';

        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.formData),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Failed to save profile');
        }

        await this.fetchProfiles();
        this.closeDialog();
      } catch (error) {
        console.error('Error saving profile:', error);
        this.showError(error.message);
      }
    },
    async duplicateProfile(id) {
      this.error = null;
      try {
        const response = await fetch(
          `${this.apiBaseUrl}/water-profiles/${id}/duplicate`,
          { method: 'POST' }
        );

        if (!response.ok) throw new Error('Failed to duplicate profile');

        await this.fetchProfiles();
      } catch (error) {
        console.error('Error duplicating profile:', error);
        this.showError('Failed to duplicate profile. Please try again.');
      }
    },
    async deleteProfile() {
      this.error = null;
      try {
        const response = await fetch(
          `${this.apiBaseUrl}/water-profiles/${this.profileToDelete.id}`,
          { method: 'DELETE' }
        );

        if (!response.ok) throw new Error('Failed to delete profile');

        await this.fetchProfiles();
        this.profileToDelete = null;
      } catch (error) {
        console.error('Error deleting profile:', error);
        this.showError('Failed to delete profile. Please try again.');
      }
    },
    viewProfile(profile) {
      // For now, just open edit dialog in read-only mode
      this.editProfile(profile);
    },
    editProfile(profile) {
      this.selectedProfile = profile;
      this.formData = {
        name: profile.name,
        description: profile.description || '',
        profile_type: profile.profile_type,
        style_category: profile.style_category || '',
        calcium: profile.calcium,
        magnesium: profile.magnesium,
        sodium: profile.sodium,
        chloride: profile.chloride,
        sulfate: profile.sulfate,
        bicarbonate: profile.bicarbonate,
        ph: profile.ph,
        notes: profile.notes || '',
      };
    },
    confirmDelete(profile) {
      this.profileToDelete = profile;
    },
    closeDialog() {
      this.showCreateDialog = false;
      this.selectedProfile = null;
      this.formData = this.getEmptyFormData();
    },
  },
};
</script>
