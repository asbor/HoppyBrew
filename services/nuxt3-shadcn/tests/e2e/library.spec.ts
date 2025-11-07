import { test, expect } from '@playwright/test'

test.describe('Library page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/library')
  })

  test('shows featured brewing books in card view', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Brewing Library' })).toBeVisible()
    await expect(page.getByText('Your collection of brewing books, guides, and resources')).toBeVisible()

    await expect(page.getByText('The Complete Joy of Homebrewing')).toBeVisible()
    await expect(page.getByText('Designing Great Beers')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Add Entry' })).toBeVisible()
  })

  test('filters entries via search', async ({ page }) => {
    const searchBox = page.getByPlaceholder('Search by title, author, description, or tags...')
    await searchBox.fill('water chemistry')

    await expect(page.getByText('Water: A Comprehensive Guide for Brewers')).toBeVisible()
    await expect(page.getByText('Designing Great Beers', { exact: true })).toHaveCount(0)
  })
})
