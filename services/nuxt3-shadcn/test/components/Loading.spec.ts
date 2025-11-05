import { mount } from '@vue/test-utils'
import Loading from '@/components/Loading.vue'

const normalise = (value: string) => value.replace(/\s+/g, ' ').trim()

describe('Loading.vue', () => {
  it('renders default loading messaging', () => {
    const wrapper = mount(Loading)
    expect(normalise(wrapper.text())).toContain('Loading... Loading...')
  })

  it('renders provided title', () => {
    const wrapper = mount(Loading, {
      props: {
        title: 'Fetching',
      },
    })

    expect(normalise(wrapper.text())).toContain('Loading... Fetching...')
  })
})
