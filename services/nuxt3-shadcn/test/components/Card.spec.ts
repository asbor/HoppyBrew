import { mount } from '@vue/test-utils'
import Card from '@/components/Card.vue'

describe('Card.vue', () => {
  it('renders card content correctly', () => {
    const wrapper = mount(Card, {
      slots: {
        default: '<div>Test Card Content</div>'
      }
    })

    expect(wrapper.text()).toContain('Test Card Content')
  })

  it('applies custom classes when provided', () => {
    const wrapper = mount(Card, {
      props: {
        class: 'custom-card-class'
      }
    })

    expect(wrapper.classes()).toContain('custom-card-class')
  })

  it('renders with default card styling', () => {
    const wrapper = mount(Card)

    // Should have some form of card styling
    expect(wrapper.classes().length).toBeGreaterThan(0)
  })

  it('supports click events', async () => {
    const wrapper = mount(Card)

    await wrapper.trigger('click')
    expect(wrapper.emitted()).toHaveProperty('click')
  })

  it('renders header slot when provided', () => {
    const wrapper = mount(Card, {
      slots: {
        header: '<h3>Card Header</h3>',
        default: '<p>Card body content</p>'
      }
    })

    expect(wrapper.text()).toContain('Card Header')
    expect(wrapper.text()).toContain('Card body content')
  })

  it('renders footer slot when provided', () => {
    const wrapper = mount(Card, {
      slots: {
        default: '<p>Main content</p>',
        footer: '<div>Card Footer</div>'
      }
    })

    expect(wrapper.text()).toContain('Main content')
    expect(wrapper.text()).toContain('Card Footer')
  })
})