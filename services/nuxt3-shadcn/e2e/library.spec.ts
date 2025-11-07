import { test, expect } from '@playwright/test'

test.describe('Library Page - Ingredient Search and Display', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/library')
  })

  test('should display library page with ingredient categories', async ({ page }) => {
    // Check page loads
    await expect(page.locator('h1')).toContainText(/library/i)
    
    // Should have ingredient category navigation
    const hopTab = page.locator('button:has-text("Hops"), a:has-text("Hops")')
    const fermentableTab = page.locator('button:has-text("Fermentables"), a:has-text("Fermentables")')
    const yeastTab = page.locator('button:has-text("Yeast"), a:has-text("Yeast")')
    
    await expect(hopTab).toBeVisible()
    await expect(fermentableTab).toBeVisible()
    await expect(yeastTab).toBeVisible()
  })

  test('should filter hops by search', async ({ page }) => {
    // Switch to hops tab if needed
    const hopTab = page.locator('button:has-text("Hops"), a:has-text("Hops")')
    if (await hopTab.isVisible()) {
      await hopTab.click()
    }
    
    // Find search input
    const searchInput = page.locator('input[type="text"], input[placeholder*="search" i]').first()
    await expect(searchInput).toBeVisible()
    
    // Search for specific hop variety
    await searchInput.fill('Cascade')
    
    // Should filter results
    await page.waitForLoadState('networkidle')
    
    // Check results contain search term
    const resultCards = page.locator('[data-testid="ingredient-card"], .hop-card, .ingredient-item')
    if (await resultCards.count() > 0) {
      await expect(resultCards.first()).toContainText(/cascade/i)
    }
  })

  test('should display fermentable details', async ({ page }) => {
    // Switch to fermentables tab
    const fermentableTab = page.locator('button:has-text("Fermentables"), a:has-text("Fermentables")')
    if (await fermentableTab.isVisible()) {
      await fermentableTab.click()
    }
    
    // Wait for content to load
    await page.waitForLoadState('networkidle')
    
    // Should display fermentable list or cards
    const fermentableItems = page.locator('[data-testid="ingredient-card"], .fermentable-card, .ingredient-item')
    
    // If fermentables are loaded, check first item details
    if (await fermentableItems.count() > 0) {
      const firstItem = fermentableItems.first()
      
      // Should have basic fermentable info
      await expect(firstItem).toBeVisible()
      
      // Click to view details if clickable
      if (await firstItem.locator('button, a').count() > 0) {
        await firstItem.locator('button, a').first().click()
        
        // Should show more details
        await expect(page.locator('[data-testid="detail-modal"], .modal, .detail-view')).toBeVisible()
      }
    }
  })

  test('should handle empty search results gracefully', async ({ page }) => {
    // Find search input
    const searchInput = page.locator('input[type="text"], input[placeholder*="search" i]').first()
    await expect(searchInput).toBeVisible()
    
    // Search for non-existent ingredient
    await searchInput.fill('XYZ-NONEXISTENT-INGREDIENT-123')
    
    // Wait for search to complete
    await page.waitForLoadState('networkidle')
    
    // Should show "no results" or empty state
    const noResultsMessage = page.locator(':has-text("No results"), :has-text("not found"), :has-text("no ingredients")')
    const emptyState = page.locator('[data-testid="empty-state"], .empty-state')
    
    // At least one of these should be visible, or results count should be 0
    const hasNoResultsMessage = await noResultsMessage.count() > 0
    const hasEmptyState = await emptyState.count() > 0
    const resultCards = await page.locator('[data-testid="ingredient-card"], .ingredient-item').count()
    
    expect(hasNoResultsMessage || hasEmptyState || resultCards === 0).toBeTruthy()
  })
})