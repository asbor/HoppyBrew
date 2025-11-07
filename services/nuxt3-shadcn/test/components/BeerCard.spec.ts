import { mount } from '@vue/test-utils'
import BeerCard from '@/components/BeerCard.vue'

const normalise = (value: string) => value.replace(/\s+/g, ' ').trim()

describe('BeerCard.vue', () => {
  const mockBeer = {
    id: 1,
    name: 'Test IPA',
    style: 'American IPA',
    abv: 6.2,
    ibu: 45,
    srm: 8,
    og: 1.062,
    fg: 1.012,
    description: 'A hoppy test beer'
  }

  it('renders beer information correctly', () => {
    const wrapper = mount(BeerCard, {
      props: {
        beer: mockBeer
      }
    })

    expect(wrapper.text()).toContain('Test IPA')
    expect(wrapper.text()).toContain('American IPA')
    expect(wrapper.text()).toContain('6.2%')
    expect(wrapper.text()).toContain('45')
  })

  it('displays alcohol content when provided', () => {
    const wrapper = mount(BeerCard, {
      props: {
        beer: mockBeer
      }
    })

    expect(wrapper.text()).toContain('6.2%')
  })

  it('shows IBU value when available', () => {
    const wrapper = mount(BeerCard, {
      props: {
        beer: mockBeer
      }
    })

    expect(wrapper.text()).toContain('45')
  })

  it('handles missing beer data gracefully', () => {
    const wrapper = mount(BeerCard, {
      props: {
        beer: {
          id: 1,
          name: 'Empty Beer'
        }
      }
    })

    expect(wrapper.text()).toContain('Empty Beer')
    // Should not crash with missing fields
  })

  it('emits click event when card is clicked', async () => {
    const wrapper = mount(BeerCard, {
      props: {
        beer: mockBeer
      }
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted()).toHaveProperty('click')
  })

  it('displays beer stats correctly formatted', () => {
    const wrapper = mount(BeerCard, {
      props: {
        beer: mockBeer
      }
    })

    // Check that OG and FG are displayed with proper formatting
    expect(wrapper.text()).toContain('1.062')
    expect(wrapper.text()).toContain('1.012')
  })
})