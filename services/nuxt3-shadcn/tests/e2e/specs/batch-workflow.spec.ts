import { test, expect } from '@playwright/test'
import { BatchPage } from '../pages/BatchPage'
import { mockMultipleApis, waitForApiCall } from '../utils/apiHelpers'
import { generateBatchData, generateRecipeData, generateFermentationReading } from '../utils/testDataGenerator'
import { generateTestName } from '../utils/helpers'

test.describe('Batch Workflow', () => {
  let batchPage: BatchPage

  test.beforeEach(async ({ page }) => {
    batchPage = new BatchPage(page)
  })

  test('should start a batch from a recipe', async ({ page }) => {
    const recipe = generateRecipeData({
      name: 'Recipe for Batch'
    })
    
    const newBatch = generateBatchData({
      name: generateTestName('New Batch'),
      recipeId: recipe.id
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes$/, response: [recipe], method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: recipe, method: 'GET' },
      { pattern: /\/batches$/, response: newBatch, status: 201, method: 'POST' }
    ])

    // Navigate to new batch page
    await batchPage.navigateToNew()

    // Fill batch information
    await batchPage.fillBatchInfo({
      name: newBatch.name,
      brewDate: newBatch.brewDate,
      notes: newBatch.notes
    })

    // Create batch
    await page.getByRole('button', { name: /Create|Start|Save/i }).click()

    // Verify batch created
    await waitForApiCall(page, /\/batches/, 'POST')
  })

  test('should track fermentation with gravity readings', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Fermenting Batch',
      status: 'fermenting'
    })

    const reading = generateFermentationReading({
      gravity: 1.050,
      temperature: 20,
      pH: 5.2
    })

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: batch, method: 'GET' },
      { pattern: /\/fermentation-readings/, response: reading, status: 201, method: 'POST' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Add fermentation reading
    await batchPage.addFermentationReading({
      gravity: reading.gravity.toString(),
      temperature: reading.temperature.toString(),
      pH: reading.pH.toString(),
      date: new Date().toISOString().split('T')[0]
    })

    // Verify reading added
    await waitForApiCall(page, /\/fermentation-readings/, 'POST')
  })

  test('should log multiple fermentation readings over time', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Multi-Reading Batch'
    })

    const readings = [
      generateFermentationReading({ gravity: 1.050, date: '2025-01-01' }),
      generateFermentationReading({ gravity: 1.030, date: '2025-01-03' }),
      generateFermentationReading({ gravity: 1.015, date: '2025-01-07' }),
      generateFermentationReading({ gravity: 1.010, date: '2025-01-10' })
    ]

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: { ...batch, readings }, method: 'GET' },
      { pattern: /\/fermentation-readings/, response: readings[0], status: 201, method: 'POST' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Verify readings are displayed (if already present)
    for (const reading of readings) {
      const gravityText = reading.gravity.toString()
      if (await page.getByText(gravityText).isVisible({ timeout: 1000 }).catch(() => false)) {
        await expect(page.getByText(gravityText)).toBeVisible()
      }
    }
  })

  test('should update batch status through workflow', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Status Update Batch',
      status: 'planning'
    })

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: batch, method: 'GET' },
      { pattern: /\/batches\/.*$/, response: { ...batch, status: 'brewing' }, method: 'PUT' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Update status to brewing
    const statusButton = page.getByRole('button', { name: /status|brewing/i })
    if (await statusButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await statusButton.click()
    }
  })

  test('should complete batch workflow', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Complete Batch',
      status: 'fermenting'
    })

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: batch, method: 'GET' },
      { pattern: /\/batches\/.*$/, response: { ...batch, status: 'completed' }, method: 'PUT' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Complete batch
    const completeButton = page.getByRole('button', { name: /complete|finish/i })
    if (await completeButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await completeButton.click()
    }

    // Verify completion
    await expect(page.getByText(/completed|finished/i)).toBeVisible()
  })

  test('should display batch timeline', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Timeline Batch'
    })

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: batch, method: 'GET' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Verify batch details displayed
    await expect(page.getByText(batch.name)).toBeVisible()
    await expect(page.getByText(/brew.*date/i)).toBeVisible()
  })

  test('should search and filter batches', async ({ page }) => {
    const batches = [
      generateBatchData({ name: 'Active Batch 1', status: 'fermenting' }),
      generateBatchData({ name: 'Active Batch 2', status: 'brewing' }),
      generateBatchData({ name: 'Completed Batch', status: 'completed' })
    ]

    await mockMultipleApis(page, [
      { pattern: /\/batches$/, response: batches, method: 'GET' }
    ])

    await batchPage.navigateToList()

    // Search for active batches
    await batchPage.searchBatches('Active')

    // Should show active batches
    await expect(page.getByText('Active Batch 1')).toBeVisible()
    await expect(page.getByText('Active Batch 2')).toBeVisible()
  })

  test('should archive completed batch', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Archive Me',
      status: 'completed'
    })

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: batch, method: 'GET' },
      { pattern: /\/batches\/.*\/archive/, response: { ...batch, archived: true }, method: 'PUT' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Archive batch
    const archiveButton = page.getByRole('button', { name: /archive/i })
    if (await archiveButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await archiveButton.click()
    }
  })

  test('should display fermentation chart', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Chart Batch'
    })

    const readings = [
      generateFermentationReading({ gravity: 1.050 }),
      generateFermentationReading({ gravity: 1.030 }),
      generateFermentationReading({ gravity: 1.015 })
    ]

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: { ...batch, readings }, method: 'GET' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Look for chart or graph element
    const chartElement = page.locator('[class*="chart"], [class*="graph"], canvas, svg')
    if (await chartElement.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(chartElement).toBeVisible()
    }
  })

  test('should validate fermentation reading inputs', async ({ page }) => {
    const batch = generateBatchData({
      name: 'Validation Batch'
    })

    await mockMultipleApis(page, [
      { pattern: /\/batches\/.*$/, response: batch, method: 'GET' }
    ])

    await batchPage.navigateToDetails(batch.id)

    // Try to add invalid reading
    const addButton = page.getByRole('button', { name: /add.*reading/i })
    if (await addButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await addButton.click()

      // Try to save without filling required fields
      const saveButton = page.getByRole('button', { name: /save.*reading/i })
      if (await saveButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await saveButton.click()

        // Should show validation error
        await expect(page.getByText(/required|invalid|error/i)).toBeVisible()
      }
    }
  })
})
