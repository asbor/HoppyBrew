<template>
    <div class="p-2">
        <div class="flex items-center gap-2">
            <div class="indicator"
                :class="{ 'connected': isConnectedToDatabase, 'disconnected': !isConnectedToDatabase }">
            </div>
            <span>{{ isConnectedToDatabase ? 'Connected' : 'Disconnected' }}</span>
            <span v-if="errorMessage" class="text-red-500 text-sm ml-2">{{ errorMessage }}</span>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const MAX_RETRIES = 3;
const POLL_INTERVAL_MS = 30000; // 30 seconds
const DEFAULT_API_URL = 'http://localhost:8000';

const config = useRuntimeConfig();
const isConnectedToDatabase = ref(false);
const errorMessage = ref('');
const pollInterval = ref(null);
const retryCount = ref(0);

// Define a method to check the database connection status
const checkDatabaseConnection = async () => {
    try {
        const apiUrl = config.public.API_URL || DEFAULT_API_URL;
        const response = await fetch(`${apiUrl}/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (response.ok) {
            isConnectedToDatabase.value = true;
            errorMessage.value = '';
            retryCount.value = 0;
        } else {
            throw new Error(`Health check failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Connection check error:', error);
        isConnectedToDatabase.value = false;
        
        retryCount.value++;
        if (retryCount.value >= MAX_RETRIES) {
            errorMessage.value = 'Connection failed after multiple retries';
        } else {
            errorMessage.value = `Connection error (retry ${retryCount.value}/${MAX_RETRIES})`;
        }
    }
};

onMounted(() => {
    // Initial check
    checkDatabaseConnection();
    
    // Poll every 30 seconds
    pollInterval.value = setInterval(checkDatabaseConnection, POLL_INTERVAL_MS);
});

onUnmounted(() => {
    // Clean up interval on component unmount
    if (pollInterval.value) {
        clearInterval(pollInterval.value);
    }
});

</script>


<style scoped>
/* Define styling for the indicator */
.indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

/* Define styling for connected state */
.connected {
    background-color: green;
}

/* Define styling for disconnected state */
.disconnected {
    background-color: red;
}
</style>