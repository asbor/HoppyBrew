// Polyfills for Node.js modules in browser
import { Buffer } from 'buffer'

// Make global available
if (typeof global === 'undefined') {
    ; (globalThis as any).global = globalThis
}

// Make Buffer available globally
if (typeof window !== 'undefined') {
    ; (window as any).Buffer = Buffer
        ; (window as any).global = window
        ; (window as any).process = { env: {} }
}

export default defineNuxtPlugin(() => {
    // Plugin setup - polyfills are loaded
})