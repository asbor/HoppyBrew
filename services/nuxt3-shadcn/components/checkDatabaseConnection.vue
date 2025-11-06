<template>
    <div class="p-2">
        <div class="flex items-center gap-2">
            <div class="indicator"
                :class="{ 'connected': isConnectedToDatabase, 'disconnected': !isConnectedToDatabase }">
            </div>
            <span>{{ isConnectedToDatabase ? 'Connected' : 'Disconnected' }}</span>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isConnectedToDatabase = ref(false);
let intervalId = null;

// Define a method to check the database connection status
const checkDatabaseConnection = () => {
    // Make an API request to check the database connection status using /health endpoint
    fetch('http://localhost:8000/health', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
        .then(response => {
            if (response.ok) {
                isConnectedToDatabase.value = true;
            } else {
                isConnectedToDatabase.value = false;
            }
        })
        .catch(error => {
            console.error('Database connection check failed:', error);
            isConnectedToDatabase.value = false;
        });
}

// Set up polling when component is mounted
onMounted(() => {
    // Check immediately on mount
    checkDatabaseConnection();
    
    // Poll every 30 seconds
    intervalId = setInterval(checkDatabaseConnection, 30000);
});

// Clean up interval when component is unmounted
onUnmounted(() => {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
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