import { test, expect } from '@playwright/test'

test.describe('HoppyBrew Landing Page', () => {
  test('should load homepage and display navigation', async ({ page }) => {
    await page.goto('/')
    
    // Check page title
    await expect(page).toHaveTitle(/HoppyBrew/i)
    
    // Check main navigation elements
    await expect(page.locator('nav')).toBeVisible()
    
    // Check for key navigation links
    const recipeLink = page.locator('a[href="/recipes"]')
    const libraryLink = page.locator('a[href="/library"]')
    const profilesLink = page.locator('a[href="/profiles"]')
    
    await expect(recipeLink).toBeVisible()
    await expect(libraryLink).toBeVisible()
    await expect(profilesLink).toBeVisible()
  })

  test('should navigate to recipes page', async ({ page }) => {
    await page.goto('/')
    
    // Click recipes link
    await page.click('a[href="/recipes"]')
    
    // Wait for navigation
    await expect(page).toHaveURL(/.*\/recipes/)
    
    // Check page content
    await expect(page.locator('h1')).toContainText(/recipes/i)
  })

  test('should navigate to library page', async ({ page }) => {
    await page.goto('/')
    
    // Click library link
    await page.click('a[href="/library"]')
    
    // Wait for navigation
    await expect(page).toHaveURL(/.*\/library/)
    
    // Check page content - should have ingredient search/display
    await expect(page.locator('h1')).toContainText(/library/i)
    
    // Should have search functionality
    const searchInput = page.locator('input[type="text"], input[placeholder*="search" i]')
    await expect(searchInput).toBeVisible()
  })

  test('should navigate to equipment profiles', async ({ page }) => {
    await page.goto('/')
    
    // Navigate to profiles
    await page.click('a[href="/profiles"]')
    await expect(page).toHaveURL(/.*\/profiles/)
    
    // Navigate to equipment profiles
    const equipmentLink = page.locator('a[href="/profiles/equipment"], a:has-text("Equipment")')
    if (await equipmentLink.isVisible()) {
      await equipmentLink.click()
      await expect(page).toHaveURL(/.*\/equipment/)
    }
    
    // Check equipment profiles page
    await expect(page.locator('h1, h2')).toContainText(/equipment/i)
  })
})