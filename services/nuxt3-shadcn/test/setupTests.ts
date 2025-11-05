import { config } from '@vue/test-utils'

config.global.stubs = {
  NuxtLink: {
    name: 'NuxtLink',
    template: '<a><slot /></a>',
    props: ['to'],
  },
}
