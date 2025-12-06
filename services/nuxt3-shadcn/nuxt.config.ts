export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss', 'shadcn-nuxt', 'nuxt-icon', 'nuxt-highcharts'],
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  },
  runtimeConfig: {
    public: {
      // Allow runtime override via NUXT_PUBLIC_API_URL to avoid baking the backend URL at build time
      API_URL: process.env.NUXT_PUBLIC_API_URL || "http://localhost:8000",
    },
  },
  generate: {
    fallback: true
  },
  vite: {
    define: {
      global: 'globalThis',
    },
    optimizeDeps: {
      include: ['xml2js', 'buffer']
    },
    server: {
      fs: {
        allow: ['..']
      }
    }
  },
  nitro: {
    experimental: {
      wasm: true
    }
  },
  ssr: false
})
