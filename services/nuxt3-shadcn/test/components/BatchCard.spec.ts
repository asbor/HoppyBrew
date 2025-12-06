import { mount } from '@vue/test-utils'
import BatchCard from '@/components/BatchCard.vue'

describe('BatchCard.vue', () => {
  const mockBatch = {
    id: 1,
    name: 'Test Batch IPA',
    recipe_name: 'American IPA Recipe',
    status: 'fermenting',
    brew_date: '2024-11-01',
    target_og: 1.062,
    measured_og: 1.060,
    target_fg: 1.012,
    measured_fg: null,
    target_abv: 6.2,
    current_stage: 'primary',
    temperature: 20,
    days_in_stage: 5
  }

  it('renders batch information correctly', () => {
    const wrapper = mount(BatchCard, {
      props: {
        batch: mockBatch
      }
    })

    expect(wrapper.text()).toContain('Test Batch IPA')
    expect(wrapper.text()).toContain('American IPA Recipe')
    expect(wrapper.text()).toContain('fermenting')
  })

  it('shows brewing progress indicators', () => {
    const wrapper = mount(BatchCard, {
      props: {
        batch: mockBatch
      }
    })

    expect(wrapper.text()).toContain('5')  // days in stage
    expect(wrapper.text()).toContain('primary')
  })

  it('displays gravity readings when available', () => {
    const wrapper = mount(BatchCard, {
      props: {
        batch: mockBatch
      }
    })

    expect(wrapper.text()).toContain('1.060')  // measured OG
    expect(wrapper.text()).toContain('1.062')  // target OG
  })

  it('handles different batch statuses', () => {
    const completedBatch = { ...mockBatch, status: 'complete' }
    const wrapper = mount(BatchCard, {
      props: {
        batch: completedBatch
      }
    })

    expect(wrapper.text()).toContain('completed')
  })

  it('shows temperature when available', () => {
    const wrapper = mount(BatchCard, {
      props: {
        batch: mockBatch
      }
    })

    expect(wrapper.text()).toContain('20')  // temperature
  })

  it('emits batch selection event', async () => {
    const wrapper = mount(BatchCard, {
      props: {
        batch: mockBatch
      }
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted()).toHaveProperty('select')
  })
})
