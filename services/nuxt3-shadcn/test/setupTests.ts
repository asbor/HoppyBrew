import { config } from '@vue/test-utils'
import { vi } from 'vitest'

// Mock useRuntimeConfig globally
global.useRuntimeConfig = vi.fn(() => ({
  public: {
    API_URL: 'http://localhost:8000',
  },
}))

config.global.stubs = {
  NuxtLink: {
    name: 'NuxtLink',
    template: '<a><slot /></a>',
    props: ['to'],
  },
}
