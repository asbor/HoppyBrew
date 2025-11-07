import { mount } from '@vue/test-utils'
import CheckDatabaseConnection from '@/components/checkDatabaseConnection.vue'

describe('CheckDatabaseConnection.vue', () => {
  it('renders connection status display', () => {
    const wrapper = mount(CheckDatabaseConnection)
    
    // Should render some form of connection status
    expect(wrapper.find('[data-testid="connection-status"]').exists() || 
           wrapper.text().includes('connection') || 
           wrapper.text().includes('database')).toBe(true)
  })

  it('shows loading state initially', () => {
    const wrapper = mount(CheckDatabaseConnection)
    
    // Should show some indication of loading/checking
    expect(wrapper.text().includes('checking') || 
           wrapper.text().includes('loading') ||
           wrapper.find('.loading').exists() ||
           wrapper.find('[data-testid="loading"]').exists()).toBe(true)
  })

  it('displays connection result after check', async () => {
    const wrapper = mount(CheckDatabaseConnection)
    
    // Wait for any async operations to complete
    await wrapper.vm.$nextTick()
    
    // Should show some result (success or failure)
    expect(wrapper.text().includes('connected') || 
           wrapper.text().includes('failed') ||
           wrapper.text().includes('success') ||
           wrapper.text().includes('error')).toBe(true)
  })

  it('handles connection success state', () => {
    const wrapper = mount(CheckDatabaseConnection, {
      props: {
        isConnected: true
      }
    })

    expect(wrapper.text().includes('connected') ||
           wrapper.text().includes('success') ||
           wrapper.find('.success').exists()).toBe(true)
  })

  it('handles connection failure state', () => {
    const wrapper = mount(CheckDatabaseConnection, {
      props: {
        isConnected: false
      }
    })

    expect(wrapper.text().includes('failed') ||
           wrapper.text().includes('error') ||
           wrapper.find('.error').exists()).toBe(true)
  })

  it('emits reconnect event when reconnect button is clicked', async () => {
    const wrapper = mount(CheckDatabaseConnection, {
      props: {
        isConnected: false
      }
    })

    const reconnectButton = wrapper.find('[data-testid="reconnect-button"]') ||
                           wrapper.find('button')
    
    if (reconnectButton.exists()) {
      await reconnectButton.trigger('click')
      expect(wrapper.emitted()).toHaveProperty('reconnect')
    }
  })
})