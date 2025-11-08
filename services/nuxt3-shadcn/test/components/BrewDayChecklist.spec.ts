import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import BrewDayChecklist from '@/components/BrewDayChecklist.vue'

// Mock the composables
vi.mock('~/composables/useBrewSteps', () => ({
  useBrewSteps: () => ({
    loading: { value: false },
    error: { value: null },
    getBrewSteps: vi.fn().mockResolvedValue([]),
    updateBrewStep: vi.fn(),
    createBrewSteps: vi.fn(),
    startBrewDay: vi.fn(),
  }),
}))

describe('BrewDayChecklist', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the component', () => {
    const wrapper = mount(BrewDayChecklist, {
      props: {
        batchId: 1,
      },
    })

    expect(wrapper.find('h3').text()).toContain('Brew Day Checklist')
  })

  it('displays no steps message when steps array is empty', async () => {
    const wrapper = mount(BrewDayChecklist, {
      props: {
        batchId: 1,
      },
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('No Brew Steps Yet')
  })

  it('displays loading state', () => {
    vi.mock('~/composables/useBrewSteps', () => ({
      useBrewSteps: () => ({
        loading: { value: true },
        error: { value: null },
        getBrewSteps: vi.fn(),
        updateBrewStep: vi.fn(),
        createBrewSteps: vi.fn(),
        startBrewDay: vi.fn(),
      }),
    }))

    const wrapper = mount(BrewDayChecklist, {
      props: {
        batchId: 1,
      },
    })

    expect(wrapper.text()).toContain('Loading brew steps')
  })

  it('calculates progress percentage correctly', async () => {
    const mockSteps = [
      {
        id: 1,
        batch_id: 1,
        step_name: 'Mash',
        step_type: 'mash',
        duration: 60,
        temperature: 65,
        notes: 'Test',
        completed: true,
        started_at: new Date().toISOString(),
        completed_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        order_index: 0,
      },
      {
        id: 2,
        batch_id: 1,
        step_name: 'Boil',
        step_type: 'boil',
        duration: 60,
        temperature: null,
        notes: 'Test',
        completed: false,
        started_at: null,
        completed_at: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        order_index: 1,
      },
    ]

    vi.mock('~/composables/useBrewSteps', () => ({
      useBrewSteps: () => ({
        loading: { value: false },
        error: { value: null },
        getBrewSteps: vi.fn().mockResolvedValue(mockSteps),
        updateBrewStep: vi.fn(),
        createBrewSteps: vi.fn(),
        startBrewDay: vi.fn(),
      }),
    }))

    const wrapper = mount(BrewDayChecklist, {
      props: {
        batchId: 1,
      },
    })

    // Set steps data
    wrapper.vm.steps = mockSteps
    await wrapper.vm.$nextTick()

    // 1 out of 2 steps completed = 50%
    expect(wrapper.vm.progressPercentage).toBe(50)
  })

  it('formats timer display correctly', () => {
    const wrapper = mount(BrewDayChecklist, {
      props: {
        batchId: 1,
      },
    })

    // Test different time values
    expect(wrapper.vm.formatTimerDisplay(59)).toBe('0:59')
    expect(wrapper.vm.formatTimerDisplay(60)).toBe('1:00')
    expect(wrapper.vm.formatTimerDisplay(3661)).toBe('1:01:01')
    expect(wrapper.vm.formatTimerDisplay(0)).toBe('0:00')
  })

  it('formats time ago correctly', () => {
    const wrapper = mount(BrewDayChecklist, {
      props: {
        batchId: 1,
      },
    })

    const now = new Date()
    const oneMinuteAgo = new Date(now.getTime() - 60000).toISOString()
    const twoHoursAgo = new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString()

    expect(wrapper.vm.formatTimeAgo(oneMinuteAgo)).toBe('1 min ago')
    expect(wrapper.vm.formatTimeAgo(twoHoursAgo)).toBe('2 hours ago')
  })
})
