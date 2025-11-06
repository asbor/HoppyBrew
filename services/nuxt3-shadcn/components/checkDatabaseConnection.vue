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

const config = useRuntimeConfig();
const isConnectedToDatabase = ref(false);
const errorMessage = ref('');
let pollInterval = null;
let retryCount = 0;
const MAX_RETRIES = 3;

// Define a method to check the database connection status
const checkDatabaseConnection = async () => {
    try {
        const apiUrl = config.public.API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (response.ok) {
            isConnectedToDatabase.value = true;
            errorMessage.value = '';
            retryCount = 0;
        } else {
            throw new Error(`Health check failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Connection check error:', error);
        isConnectedToDatabase.value = false;
        
        retryCount++;
        if (retryCount >= MAX_RETRIES) {
            errorMessage.value = 'Connection failed after multiple retries';
        } else {
            errorMessage.value = `Connection error (retry ${retryCount}/${MAX_RETRIES})`;
        }
    }
};

onMounted(() => {
    // Initial check
    checkDatabaseConnection();
    
    // Poll every 30 seconds
    pollInterval = setInterval(checkDatabaseConnection, 30000);
});

onUnmounted(() => {
    // Clean up interval on component unmount
    if (pollInterval) {
        clearInterval(pollInterval);
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