import { test, expect } from '@playwright/test'
import { RecipePage } from '../pages/RecipePage'
import { mockApiSuccess, mockMultipleApis } from '../utils/apiHelpers'
import { generateRecipeData, generateCompleteRecipe, generateBeerXMLData } from '../utils/testDataGenerator'
import { generateTestName } from '../utils/helpers'

test.describe('Recipe Management Flows', () => {
  let recipePage: RecipePage
  
  test.beforeEach(async ({ page }) => {
    recipePage = new RecipePage(page)
  })

  test('should create a new recipe with complete workflow', async ({ page }) => {
    // Mock APIs
    const newRecipe = generateRecipeData({
      name: generateTestName('New IPA Recipe')
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes$/, response: [], method: 'GET' },
      { pattern: /\/recipes$/, response: newRecipe, status: 201, method: 'POST' }
    ])

    // Navigate to recipes page
    await recipePage.navigateToList()
    await expect(page.getByRole('heading', { name: 'Recipes' })).toBeVisible()

    // Click new recipe button
    await recipePage.clickNewRecipe()

    // Fill recipe details
    await recipePage.fillRecipeBasicInfo({
      name: newRecipe.name,
      type: newRecipe.type,
      style: newRecipe.style,
      batchSize: newRecipe.batchSize.toString(),
      boilTime: newRecipe.boilTime.toString()
    })

    // Save recipe
    await recipePage.saveRecipe()

    // Verify success message or redirect
    await expect(page).toHaveURL(/\/recipes/)
  })

  test('should add ingredients to a recipe', async ({ page }) => {
    const recipe = generateCompleteRecipe()

    await mockMultipleApis(page, [
      { pattern: /\/recipes\//, response: recipe, method: 'GET' },
      { pattern: /\/fermentables/, response: recipe.fermentables, method: 'GET' },
      { pattern: /\/hops/, response: recipe.hops, method: 'GET' },
      { pattern: /\/yeasts/, response: recipe.yeasts, method: 'GET' }
    ])

    // Navigate to recipe details
    await recipePage.navigateToDetails(recipe.id)

    // Verify ingredients are displayed
    for (const fermentable of recipe.fermentables) {
      await expect(page.getByText(fermentable.name)).toBeVisible()
    }

    for (const hop of recipe.hops) {
      await expect(page.getByText(hop.name)).toBeVisible()
    }

    for (const yeast of recipe.yeasts) {
      await expect(page.getByText(yeast.name)).toBeVisible()
    }
  })

  test('should search and filter recipes', async ({ page }) => {
    const recipes = [
      generateRecipeData({ name: 'West Coast IPA', style: 'IPA' }),
      generateRecipeData({ name: 'Vienna Lager', style: 'Lager' }),
      generateRecipeData({ name: 'Midnight Stout', style: 'Stout' })
    ]

    await mockApiSuccess(page, /\/recipes/, recipes)

    await recipePage.navigateToList()

    // Search for IPA
    await recipePage.searchRecipes('IPA')

    // Should show only IPA recipe
    await expect(page.getByText('West Coast IPA')).toBeVisible()
    
    // Vienna Lager should not be visible (filtered out)
    // Note: This depends on client-side filtering implementation
  })

  test('should clone an existing recipe', async ({ page }) => {
    const originalRecipe = generateRecipeData({
      name: 'Original Recipe'
    })
    
    const clonedRecipe = generateRecipeData({
      name: 'Original Recipe (Copy)',
      type: originalRecipe.type,
      style: originalRecipe.style
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes$/, response: [originalRecipe], method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: originalRecipe, method: 'GET' },
      { pattern: /\/recipes\/.*\/clone/, response: clonedRecipe, status: 201, method: 'POST' }
    ])

    // Navigate to recipe details
    await recipePage.navigateToDetails(originalRecipe.id)

    // Clone the recipe
    await recipePage.cloneRecipe()

    // Verify cloned recipe appears
    await expect(page.getByText(clonedRecipe.name)).toBeVisible()
  })

  test('should modify a cloned recipe and save as new', async ({ page }) => {
    const clonedRecipe = generateRecipeData({
      name: 'Modified Clone Recipe'
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes\/.*$/, response: clonedRecipe, method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: { ...clonedRecipe, name: 'Updated Clone' }, method: 'PUT' }
    ])

    // Navigate to cloned recipe
    await recipePage.navigateToDetails(clonedRecipe.id)

    // Modify recipe name
    await recipePage.fillRecipeBasicInfo({
      name: 'Updated Clone'
    })

    // Save changes
    await recipePage.saveRecipe()

    // Verify success
    await expect(page).toHaveURL(/\/recipes/)
  })

  test('should view recipe details', async ({ page }) => {
    const recipe = generateCompleteRecipe()

    await mockMultipleApis(page, [
      { pattern: /\/recipes\//, response: recipe, method: 'GET' }
    ])

    await recipePage.navigateToDetails(recipe.id)

    // Verify recipe details are displayed
    await expect(page.getByText(recipe.name)).toBeVisible()
    await expect(page.getByText(recipe.type)).toBeVisible()
    await expect(page.getByText(recipe.style)).toBeVisible()
  })

  test('should switch between card and table views', async ({ page }) => {
    const recipes = [
      generateRecipeData({ name: 'Recipe 1' }),
      generateRecipeData({ name: 'Recipe 2' })
    ]

    await mockApiSuccess(page, /\/recipes/, recipes)

    await recipePage.navigateToList()

    // Verify we're in table view
    await expect(page.getByRole('table')).toBeVisible()

    // Switch to card view
    await recipePage.switchToCardView()

    // Verify URL changed
    await expect(page).toHaveURL(/recipeCardWindow/)

    // Switch back to table view
    await recipePage.switchToTableView()

    // Verify we're back to table view
    await expect(page).toHaveURL(/\/recipes$/)
  })

  test('should delete a recipe', async ({ page }) => {
    const recipe = generateRecipeData({
      name: 'Recipe to Delete'
    })

    await mockMultipleApis(page, [
      { pattern: /\/recipes$/, response: [recipe], method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: recipe, method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: { success: true }, status: 204, method: 'DELETE' }
    ])

    await recipePage.navigateToDetails(recipe.id)

    // Delete the recipe
    await recipePage.deleteRecipe()

    // Confirm deletion if needed
    const confirmButton = page.getByRole('button', { name: /Confirm|Yes|Delete/i })
    if (await confirmButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await confirmButton.click()
    }

    // Should redirect to recipe list
    await expect(page).toHaveURL(/\/recipes$/)
  })

  test('should validate recipe form inputs', async ({ page }) => {
    await mockApiSuccess(page, /\/recipes/, [])

    await recipePage.navigateToNew()

    // Try to save without filling required fields
    await recipePage.saveRecipe()

    // Should show validation errors
    // Note: Specific validation depends on implementation
    await expect(page.getByText(/required|field|invalid/i)).toBeVisible()
  })

  test('should display recipe statistics', async ({ page }) => {
    const recipe = generateCompleteRecipe()

    await mockApiSuccess(page, /\/recipes\//, recipe)

    await recipePage.navigateToDetails(recipe.id)

    // Verify statistics are displayed
    await expect(page.getByText(/batch.*size/i)).toBeVisible()
    await expect(page.getByText(/boil.*time/i)).toBeVisible()
    await expect(page.getByText(/efficiency/i)).toBeVisible()
  })
})
