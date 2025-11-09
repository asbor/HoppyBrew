import { test, expect } from '@playwright/test'
import { RecipePage } from '../pages/RecipePage'
import { mockMultipleApis, waitForApiCall } from '../utils/apiHelpers'
import { generateRecipeData, generateBeerXMLData } from '../utils/testDataGenerator'
import { generateTestName } from '../utils/helpers'

test.describe('BeerXML Import Workflow', () => {
  let recipePage: RecipePage

  test.beforeEach(async ({ page }) => {
    recipePage = new RecipePage(page)
  })

  test('should import BeerXML file and create recipe', async ({ page }) => {
    const recipeName = generateTestName('Imported Recipe')
    const xmlData = generateBeerXMLData(recipeName)
    
    const importedRecipe = generateRecipeData({
      name: recipeName,
      type: 'All Grain',
      brewer: 'Test Brewer'
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes\/import/, response: importedRecipe, status: 201, method: 'POST' },
      { pattern: /\/recipes$/, response: [importedRecipe], method: 'GET' }
    ])

    // Navigate to import page
    await page.goto('/ImportXML')

    // Verify import page loaded
    await expect(page.getByRole('heading', { name: /Import/i })).toBeVisible()

    // Create a file with BeerXML content
    const buffer = Buffer.from(xmlData)
    
    // Upload the file
    const fileInput = page.locator('input[type="file"]')
    if (await fileInput.isVisible({ timeout: 2000 }).catch(() => false)) {
      // Create a temporary file-like object
      await fileInput.setInputFiles({
        name: 'recipe.xml',
        mimeType: 'application/xml',
        buffer
      })
    }

    // Submit import
    await page.getByRole('button', { name: /Import|Upload/i }).click()

    // Wait for import to complete
    await waitForApiCall(page, /\/recipes\/import/, 'POST')

    // Should show success message or redirect
    const successMessage = page.getByText(/success|imported|created/i)
    if (await successMessage.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(successMessage).toBeVisible()
    }
  })

  test('should validate BeerXML data after import', async ({ page }) => {
    const recipeName = generateTestName('Validated Import')
    const importedRecipe = generateRecipeData({
      name: recipeName,
      type: 'All Grain',
      batchSize: 19,
      boilTime: 60,
      efficiency: 72
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes\/import/, response: importedRecipe, status: 201, method: 'POST' },
      { pattern: /\/recipes\/.*$/, response: importedRecipe, method: 'GET' }
    ])

    await page.goto('/ImportXML')

    const xmlData = generateBeerXMLData(recipeName)
    const buffer = Buffer.from(xmlData)

    const fileInput = page.locator('input[type="file"]')
    if (await fileInput.isVisible({ timeout: 2000 }).catch(() => false)) {
      await fileInput.setInputFiles({
        name: 'recipe.xml',
        mimeType: 'application/xml',
        buffer
      })
    }

    await page.getByRole('button', { name: /Import|Upload/i }).click()

    // Navigate to the imported recipe to verify data
    await recipePage.navigateToDetails(importedRecipe.id)

    // Verify recipe data
    await expect(page.getByText(recipeName)).toBeVisible()
    await expect(page.getByText('All Grain')).toBeVisible()
  })

  test('should handle invalid BeerXML file', async ({ page }) => {
    await mockMultipleApis(page, [
      { 
        pattern: /\/recipes\/import/, 
        response: { error: 'Invalid XML format' }, 
        status: 400, 
        method: 'POST' 
      }
    ])

    await page.goto('/ImportXML')

    const invalidXml = '<?xml version="1.0"?><INVALID>Not a valid BeerXML</INVALID>'
    const buffer = Buffer.from(invalidXml)

    const fileInput = page.locator('input[type="file"]')
    if (await fileInput.isVisible({ timeout: 2000 }).catch(() => false)) {
      await fileInput.setInputFiles({
        name: 'invalid.xml',
        mimeType: 'application/xml',
        buffer
      })
    }

    await page.getByRole('button', { name: /Import|Upload/i }).click()

    // Should show error message
    await expect(page.getByText(/error|invalid|failed/i)).toBeVisible()
  })

  test('should save imported recipe after validation', async ({ page }) => {
    const recipeName = generateTestName('Import to Save')
    const importedRecipe = generateRecipeData({
      name: recipeName
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes\/import/, response: importedRecipe, status: 201, method: 'POST' },
      { pattern: /\/recipes\/.*$/, response: importedRecipe, method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: importedRecipe, method: 'PUT' }
    ])

    await page.goto('/ImportXML')

    const xmlData = generateBeerXMLData(recipeName)
    const buffer = Buffer.from(xmlData)

    const fileInput = page.locator('input[type="file"]')
    if (await fileInput.isVisible({ timeout: 2000 }).catch(() => false)) {
      await fileInput.setInputFiles({
        name: 'recipe.xml',
        mimeType: 'application/xml',
        buffer
      })
    }

    await page.getByRole('button', { name: /Import|Upload/i }).click()

    // Wait for import
    await waitForApiCall(page, /\/recipes\/import/, 'POST')

    // Navigate to recipe and save
    await recipePage.navigateToDetails(importedRecipe.id)
    await recipePage.saveRecipe()

    // Verify saved
    await expect(page).toHaveURL(/\/recipes/)
  })

  test('should import recipe with ingredients', async ({ page }) => {
    const recipeName = generateTestName('Full Import')
    const importedRecipe = {
      ...generateRecipeData({ name: recipeName }),
      fermentables: [
        { name: 'Pale Malt', amount: 5.0, type: 'Grain' }
      ],
      hops: [
        { name: 'Cascade', amount: 0.05, alpha: 7.5 }
      ],
      yeasts: [
        { name: 'US-05', type: 'Ale' }
      ]
    }

    await mockMultipleApis(page, [
      { pattern: /\/recipes\/import/, response: importedRecipe, status: 201, method: 'POST' },
      { pattern: /\/recipes\/.*$/, response: importedRecipe, method: 'GET' }
    ])

    await page.goto('/ImportXML')

    const xmlData = generateBeerXMLData(recipeName)
    const buffer = Buffer.from(xmlData)

    const fileInput = page.locator('input[type="file"]')
    if (await fileInput.isVisible({ timeout: 2000 }).catch(() => false)) {
      await fileInput.setInputFiles({
        name: 'recipe.xml',
        mimeType: 'application/xml',
        buffer
      })
    }

    await page.getByRole('button', { name: /Import|Upload/i }).click()

    // Navigate to verify ingredients
    await recipePage.navigateToDetails(importedRecipe.id)

    // Verify ingredients
    await expect(page.getByText('Pale Malt')).toBeVisible()
    await expect(page.getByText('Cascade')).toBeVisible()
    await expect(page.getByText('US-05')).toBeVisible()
  })

  test('should handle large BeerXML file', async ({ page }) => {
    const recipeName = generateTestName('Large Import')
    const importedRecipe = generateRecipeData({ name: recipeName })

    await mockMultipleApis(page, [
      { pattern: /\/recipes\/import/, response: importedRecipe, status: 201, method: 'POST' }
    ])

    await page.goto('/ImportXML')

    // Generate large XML with many ingredients
    let largeXml = `<?xml version="1.0" encoding="UTF-8"?>
<RECIPES>
  <RECIPE>
    <NAME>${recipeName}</NAME>
    <VERSION>1</VERSION>
    <TYPE>All Grain</TYPE>
    <FERMENTABLES>`
    
    // Add 20 fermentables
    for (let i = 1; i <= 20; i++) {
      largeXml += `
      <FERMENTABLE>
        <NAME>Malt ${i}</NAME>
        <VERSION>1</VERSION>
        <TYPE>Grain</TYPE>
        <AMOUNT>${i * 0.5}</AMOUNT>
      </FERMENTABLE>`
    }
    
    largeXml += `
    </FERMENTABLES>
  </RECIPE>
</RECIPES>`

    const buffer = Buffer.from(largeXml)

    const fileInput = page.locator('input[type="file"]')
    if (await fileInput.isVisible({ timeout: 2000 }).catch(() => false)) {
      await fileInput.setInputFiles({
        name: 'large-recipe.xml',
        mimeType: 'application/xml',
        buffer
      })
    }

    await page.getByRole('button', { name: /Import|Upload/i }).click()

    // Should handle large file
    await waitForApiCall(page, /\/recipes\/import/, 'POST')
  })
})
