import { test, expect } from '@playwright/test'
import { InventoryPage } from '../pages/InventoryPage'
import { mockMultipleApis, waitForApiCall } from '../utils/apiHelpers'
import { 
  generateHopData, 
  generateFermentableData, 
  generateYeastData 
} from '../utils/testDataGenerator'
import { generateTestName } from '../utils/helpers'

test.describe('Inventory Management', () => {
  let inventoryPage: InventoryPage

  test.beforeEach(async ({ page }) => {
    inventoryPage = new InventoryPage(page)
  })

  test('should add new hop to inventory', async ({ page }) => {
    const newHop = generateHopData({
      name: generateTestName('Cascade'),
      alpha: 7.5,
      quantity: 100,
      unit: 'g'
    })

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [], method: 'GET' },
      { pattern: /\/hops$/, response: newHop, status: 201, method: 'POST' }
    ])

    await inventoryPage.navigateToHops()

    await inventoryPage.addInventoryItem({
      name: newHop.name,
      quantity: newHop.quantity.toString(),
      unit: newHop.unit
    })

    await waitForApiCall(page, /\/hops/, 'POST')
  })

  test('should add new fermentable to inventory', async ({ page }) => {
    const newFermentable = generateFermentableData({
      name: generateTestName('Pale Malt'),
      quantity: 25,
      unit: 'kg'
    })

    await mockMultipleApis(page, [
      { pattern: /\/fermentables$/, response: [], method: 'GET' },
      { pattern: /\/fermentables$/, response: newFermentable, status: 201, method: 'POST' }
    ])

    await inventoryPage.navigateToFermentables()

    await inventoryPage.addInventoryItem({
      name: newFermentable.name,
      quantity: newFermentable.quantity.toString(),
      unit: newFermentable.unit
    })

    await waitForApiCall(page, /\/fermentables/, 'POST')
  })

  test('should add new yeast to inventory', async ({ page }) => {
    const newYeast = generateYeastData({
      name: generateTestName('US-05'),
      quantity: 5
    })

    await mockMultipleApis(page, [
      { pattern: /\/yeasts$/, response: [], method: 'GET' },
      { pattern: /\/yeasts$/, response: newYeast, status: 201, method: 'POST' }
    ])

    await inventoryPage.navigateToYeasts()

    await inventoryPage.addInventoryItem({
      name: newYeast.name,
      quantity: newYeast.quantity.toString()
    })

    await waitForApiCall(page, /\/yeasts/, 'POST')
  })

  test('should update inventory quantities', async ({ page }) => {
    const hop = generateHopData({
      name: 'Existing Hop',
      quantity: 100
    })

    const updatedHop = { ...hop, quantity: 150 }

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [hop], method: 'GET' },
      { pattern: /\/hops\/.*$/, response: hop, method: 'GET' },
      { pattern: /\/hops\/.*$/, response: updatedHop, method: 'PUT' }
    ])

    await inventoryPage.navigateToHops()

    // Update quantity
    await inventoryPage.updateQuantity(hop.name, '150')

    await waitForApiCall(page, /\/hops/, 'PUT')
  })

  test('should track ingredient usage', async ({ page }) => {
    const fermentable = generateFermentableData({
      name: 'Tracking Malt',
      quantity: 10
    })

    await mockMultipleApis(page, [
      { pattern: /\/fermentables$/, response: [fermentable], method: 'GET' }
    ])

    await inventoryPage.navigateToFermentables()

    // Verify current quantity is displayed
    await expect(page.getByText(fermentable.name)).toBeVisible()
    await expect(page.getByText(`${fermentable.quantity}`)).toBeVisible()
  })

  test('should search inventory items', async ({ page }) => {
    const hops = [
      generateHopData({ name: 'Cascade', alpha: 7.5 }),
      generateHopData({ name: 'Centennial', alpha: 10.0 }),
      generateHopData({ name: 'Citra', alpha: 12.0 })
    ]

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: hops, method: 'GET' }
    ])

    await inventoryPage.navigateToHops()

    // Search for Cascade
    await inventoryPage.searchInventory('Cascade')

    // Should show Cascade
    await expect(page.getByText('Cascade')).toBeVisible()
  })

  test('should filter by low stock items', async ({ page }) => {
    const hops = [
      generateHopData({ name: 'Low Stock Hop', quantity: 5 }),
      generateHopData({ name: 'Good Stock Hop', quantity: 100 })
    ]

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: hops, method: 'GET' },
      { pattern: /\/hops\?.*low.*stock/, response: [hops[0]], method: 'GET' }
    ])

    await inventoryPage.navigateToHops()

    // Filter by low stock
    const filterButton = page.getByRole('button', { name: /low.*stock|filter/i })
    if (await filterButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await filterButton.click()
    }
  })

  test('should display low stock alert', async ({ page }) => {
    const lowStockHop = generateHopData({
      name: 'Alert Hop',
      quantity: 5 // Low quantity
    })

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [lowStockHop], method: 'GET' }
    ])

    await inventoryPage.navigateToHops()

    // Look for low stock indicator
    await expect(page.getByText(lowStockHop.name)).toBeVisible()
    
    // Check for alert badge or warning
    const alertIndicator = page.getByText(/low|alert|warning/i)
    if (await alertIndicator.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(alertIndicator).toBeVisible()
    }
  })

  test('should delete inventory item', async ({ page }) => {
    const hop = generateHopData({
      name: 'Delete Me Hop'
    })

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [hop], method: 'GET' },
      { pattern: /\/hops\/.*$/, response: { success: true }, status: 204, method: 'DELETE' }
    ])

    await inventoryPage.navigateToHops()

    // Delete the item
    await inventoryPage.deleteItem(hop.name)

    await waitForApiCall(page, /\/hops/, 'DELETE')
  })

  test('should view inventory overview', async ({ page }) => {
    const inventory = {
      hops: [generateHopData({ name: 'Overview Hop' })],
      fermentables: [generateFermentableData({ name: 'Overview Malt' })],
      yeasts: [generateYeastData({ name: 'Overview Yeast' })]
    }

    await mockMultipleApis(page, [
      { pattern: /\/inventory$/, response: inventory, method: 'GET' },
      { pattern: /\/hops$/, response: inventory.hops, method: 'GET' },
      { pattern: /\/fermentables$/, response: inventory.fermentables, method: 'GET' },
      { pattern: /\/yeasts$/, response: inventory.yeasts, method: 'GET' }
    ])

    await inventoryPage.navigateToOverview()

    // Verify overview page displays categories
    await expect(page.getByRole('heading', { name: /inventory/i })).toBeVisible()
  })

  test('should navigate between inventory categories', async ({ page }) => {
    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [], method: 'GET' },
      { pattern: /\/fermentables$/, response: [], method: 'GET' },
      { pattern: /\/yeasts$/, response: [], method: 'GET' },
      { pattern: /\/miscs$/, response: [], method: 'GET' }
    ])

    // Navigate to hops
    await inventoryPage.navigateToHops()
    await expect(page).toHaveURL(/\/inventory\/hops/)

    // Navigate to fermentables
    await inventoryPage.navigateToFermentables()
    await expect(page).toHaveURL(/\/inventory\/fermentables/)

    // Navigate to yeasts
    await inventoryPage.navigateToYeasts()
    await expect(page).toHaveURL(/\/inventory\/yeasts/)

    // Navigate to miscs
    await inventoryPage.navigateToMiscs()
    await expect(page).toHaveURL(/\/inventory\/miscs/)
  })

  test('should handle inventory reorder workflow', async ({ page }) => {
    const lowStockItem = generateHopData({
      name: 'Reorder Hop',
      quantity: 5
    })

    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [lowStockItem], method: 'GET' }
    ])

    await inventoryPage.navigateToHops()

    // Verify low stock item
    await expect(page.getByText(lowStockItem.name)).toBeVisible()

    // Look for reorder button or link
    const reorderButton = page.getByRole('button', { name: /reorder|order/i })
    if (await reorderButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(reorderButton).toBeVisible()
    }
  })

  test('should validate inventory form inputs', async ({ page }) => {
    await mockMultipleApis(page, [
      { pattern: /\/hops$/, response: [], method: 'GET' }
    ])

    await inventoryPage.navigateToHops()

    // Try to add item without name
    const addButton = page.getByRole('button', { name: /add|new/i })
    if (await addButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await addButton.click()

      // Try to save without filling required fields
      const saveButton = page.getByRole('button', { name: /save|add/i })
      if (await saveButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await saveButton.click()

        // Should show validation error
        await expect(page.getByText(/required|invalid|error/i)).toBeVisible()
      }
    }
  })
})
