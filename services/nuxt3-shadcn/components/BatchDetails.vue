<template>
    <div class="border-2 p-4">
        <div>
            <label for="name">Batch Name:</label>
            <input
id="name" v-model="batch.batch_name" type="text" required placeholder="Optional"
                class="border-2 border-gray-300 rounded-lg p-2 w-full">
        </div>
        <div>
            <label for="brewer">Brewer:</label>
            <input
id="brewer" v-model="batch.brewer" type="text" required placeholder="Optional"
                class="border-2 border-gray-300 rounded-lg p-2 w-full">
        </div>
        <div>
            <label for="batch_size">Batch Size:</label>
            <input
id="batch_size" v-model="batch.batch_size" type="number" required placeholder="Optional"
                class="border-2 border-gray-300 rounded-lg p-2 w-full">
        </div>
        <div>
            <label for="brew_date">Brew Date:</label>
            <input
id="brew_date" v-model="batch.brew_date" type="date" required placeholder="Optional"
                class="border-2 border-gray-300 rounded-lg p-2 w-full">
        </div>
    </div>
</template>

<script>
export default {
    props: ['batch']
};
</script>