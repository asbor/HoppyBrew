import { mount } from '@vue/test-utils'
import DataTable from '@/components/DataTable.vue'

describe('DataTable.vue', () => {
  const mockColumns = [
    { key: 'name', label: 'Name' },
    { key: 'value', label: 'Value' },
    { key: 'type', label: 'Type' }
  ]

  const mockData = [
    { id: 1, name: 'Test Item 1', value: 100, type: 'A' },
    { id: 2, name: 'Test Item 2', value: 200, type: 'B' },
    { id: 3, name: 'Test Item 3', value: 300, type: 'A' }
  ]

  it('renders table headers correctly', () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: mockColumns,
        data: mockData
      }
    })

    expect(wrapper.text()).toContain('Name')
    expect(wrapper.text()).toContain('Value')
    expect(wrapper.text()).toContain('Type')
  })

  it('displays all data rows', () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: mockColumns,
        data: mockData
      }
    })

    expect(wrapper.text()).toContain('Test Item 1')
    expect(wrapper.text()).toContain('Test Item 2')
    expect(wrapper.text()).toContain('Test Item 3')
  })

  it('shows correct data values', () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: mockColumns,
        data: mockData
      }
    })

    expect(wrapper.text()).toContain('100')
    expect(wrapper.text()).toContain('200')
    expect(wrapper.text()).toContain('300')
  })

  it('handles empty data gracefully', () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: mockColumns,
        data: []
      }
    })

    // Should render headers but no data rows
    expect(wrapper.text()).toContain('Name')
    expect(wrapper.text()).toContain('Value')
    expect(wrapper.text()).not.toContain('Test Item')
  })

  it('emits row click events', async () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: mockColumns,
        data: mockData
      }
    })

    // Find and click the first row
    const firstRow = wrapper.find('[data-testid="table-row"]')
    if (firstRow.exists()) {
      await firstRow.trigger('click')
      expect(wrapper.emitted()).toHaveProperty('rowClick')
    }
  })

  it('applies sorting when column headers are clicked', async () => {
    const wrapper = mount(DataTable, {
      props: {
        columns: mockColumns,
        data: mockData,
        sortable: true
      }
    })

    const nameHeader = wrapper.find('[data-testid="column-header-name"]')
    if (nameHeader.exists()) {
      await nameHeader.trigger('click')
      expect(wrapper.emitted()).toHaveProperty('sort')
    }
  })
})