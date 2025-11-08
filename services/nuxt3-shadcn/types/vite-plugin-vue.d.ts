declare module '@vitejs/plugin-vue' {
  import type { Plugin } from 'vite'

  export interface VuePluginOptions {
    [key: string]: unknown
  }

  export default function vuePlugin(options?: VuePluginOptions): Plugin
}
