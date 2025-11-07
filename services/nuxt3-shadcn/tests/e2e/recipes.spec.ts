import { test, expect } from '@playwright/test'
import { mockRecipesApi } from './fixtures/mockApi'
import { recipeFixtures } from './fixtures/testData'

test.describe('Recipes page', () => {
  test.beforeEach(async ({ page }) => {
    await mockRecipesApi(page)
    await page.goto('/recipes')
  })

  test('renders recipe overview with mocked data', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Recipes' })).toBeVisible()
    await expect(page.getByText('Your personal brewing recipe library')).toBeVisible()
    await expect(page.getByRole('button', { name: 'New Recipe' })).toBeVisible()

    for (const recipe of recipeFixtures.slice(0, 2)) {
      await expect(page.getByRole('cell', { name: recipe.name })).toBeVisible()
      await expect(page.getByRole('cell', { name: recipe.type })).toBeVisible()
    }
  })

  test('filters recipes by search input', async ({ page }) => {
    const searchField = page.getByPlaceholder('Search recipes by name, type, or brewer...')
    await searchField.fill('vienna')

    await expect(page.getByRole('cell', { name: /Vienna Lager/i })).toBeVisible()
    await expect(page.getByRole('cell', { name: /West Coast IPA/i })).toHaveCount(0)
  })

  test('navigates to the recipe card view', async ({ page }) => {
    await page.getByRole('link', { name: 'Card View' }).click()
    await expect(page).toHaveURL(/\/recipes\/recipeCardWindow$/)
    await expect(page.getByRole('link', { name: 'Table View' })).toBeVisible()
  })
})
