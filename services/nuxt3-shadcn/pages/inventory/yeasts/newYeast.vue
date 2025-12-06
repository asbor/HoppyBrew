<template>
    <div>
        <!-- Header -->
        <header>
            <div>
                <h1 class="text-2xl font-semibold">Create a new yeast item</h1>
            </div>
        </header>

        <!-- Main section -->
        <main>
            <div v-if="isLoading">
                <Loading :title="isLoadingTitle" />
            </div>
            <div v-if="!isLoading">
                <form @submit.prevent="saveYeast">
                    <div>
                        <label for="name">Name:</label>
                        <input
id="name" v-model="yeast.name" type="text" required placeholder="Optional"
                            class="border-2 border-gray-300 rounded-lg p-2 w-full">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label for="type">Type:</label>
                            <input
id="type" v-model="yeast.type" type="text" required placeholder="Optional"
                                class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="form">Form:</label>
                            <input
id="form" v-model="yeast.form" type="text" required placeholder="Optional"
                                class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="laboratory">Laboratory:</label>
                            <input
id="laboratory" v-model="yeast.laboratory" type="text" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="product_id">Product ID:</label>
                            <input
id="product_id" v-model="yeast.product_id" type="text" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="min_temperature">Min Temperature:</label>
                            <input
id="min_temperature" v-model="yeast.min_temperature" type="number" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="max_temperature">Max Temperature:</label>
                            <input
id="max_temperature" v-model="yeast.max_temperature" type="number" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="flocculation">Flocculation:</label>
                            <input
id="flocculation" v-model="yeast.flocculation" type="text" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="attenuation">Attenuation:</label>
                            <input
id="attenuation" v-model="yeast.attenuation" type="number" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="max_reuse">Max Reuse:</label>
                            <input
id="max_reuse" v-model="yeast.max_reuse" type="number" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="amount">Amount:</label>
                            <input
id="amount" v-model="yeast.amount" type="number" required placeholder="Optional"
                                class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="amount_is_weight">Amount is Weight:</label>
                            <input
id="amount_is_weight" v-model="yeast.amount_is_weight" type="checkbox"
                                class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="times_cultured">Times Cultured:</label>
                            <input
id="times_cultured" v-model="yeast.times_cultured" type="number" required
                                placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                        <div>
                            <label for="add_to_secondary">Add to Secondary:</label>
                            <input
id="add_to_secondary" v-model="yeast.add_to_secondary" type="checkbox"
                                class="border-2 border-gray-300 rounded-lg p-2 w-full">
                        </div>
                    </div>
                    <div>
                        <label for="notes">Notes:</label>
                        <textarea
id="notes" v-model="yeast.notes"
                            class="w-full border-2 border-gray-300 rounded-lg p-2"></textarea>
                    </div>
                    <div>
                        <label for="best_for">Best For:</label>
                        <input
id="best_for" v-model="yeast.best_for" type="text" required placeholder="Optional"
                            class="border-2 border-gray-300 rounded-lg p-2 w-full">
                    </div>
                    <div>
                        <label for="display_amount">Display Amount:</label>
                        <input
id="display_amount" v-model="yeast.display_amount" type="text" required
                            placeholder="Optional" class="border-2 border-gray-300 rounded-lg p-2 w-full">
                    </div>
                    <div>
                        <label for="inventory">Inventory:</label>
                        <input
id="inventory" v-model="yeast.inventory" type="number" required placeholder="Optional"
                            class="border-2 border-gray-300 rounded-lg p-2 w-full">
                    </div>
                </form>
            </div>
        </main>

        <!-- Footer -->
        <footer class="flex justify-end gap-4 mt-8">
            <Button @click="saveYeast">Save</Button>
            <Button @click="cancel">Cancel</Button>
        </footer>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
    data() {
        return {
            yeast: {
                name: '',
                type: '',
                form: '',
                laboratory: '',
                product_id: '',
                min_temperature: 0,
                max_temperature: 0,
                flocculation: '',
                attenuation: 0,
                notes: '',
                best_for: '',
                max_reuse: 0,
                amount: 0,
                amount_is_weight: false,
                inventory: 0,
                display_amount: '',
                times_cultured: 0,
                add_to_secondary: false,
            },
            isLoading: false,
            isLoadingTitle: 'Loading...',
        };
    },
    methods: {
        saveYeast() {
            this.isLoading = true;
            this.isLoadingTitle = 'Saving...';
            axios.post('http://localhost:8000/inventory/yeasts', this.yeast)
                .then(res => {
                    this.$router.back();
                })
                .catch(error => {
                    console.error(error);
                });
            this.isLoading = false;
        },
        cancel() {
            this.$router.back();
        },
    },
};
</script>
