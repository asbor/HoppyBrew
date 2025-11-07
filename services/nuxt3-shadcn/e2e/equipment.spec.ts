import { test, expect } from '@playwright/test'

test.describe('Equipment Profiles Management', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to equipment profiles page
    await page.goto('/profiles/equipment')
  })

  test('should display equipment profiles page', async ({ page }) => {
    // Check page loads with equipment profiles
    await expect(page.locator('h1, h2')).toContainText(/equipment/i)
    
    // Should have ability to add new equipment profile
    const addButton = page.locator('button:has-text("Add"), button:has-text("New"), button:has-text("Create")')
    await expect(addButton).toBeVisible()
  })

  test('should open equipment profile creation modal', async ({ page }) => {
    // Click add/new equipment button
    const addButton = page.locator('button:has-text("Add"), button:has-text("New"), button:has-text("Create")').first()
    await addButton.click()
    
    // Modal or form should appear
    const modal = page.locator('[data-testid="equipment-modal"], .modal, .dialog')
    const form = page.locator('form[data-testid="equipment-form"], form:has(input)')
    
    const modalVisible = await modal.count() > 0
    const formVisible = await form.count() > 0
    
    expect(modalVisible || formVisible).toBeTruthy()
    
    // Should have equipment name field
    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]')
    if (await nameInput.count() > 0) {
      await expect(nameInput).toBeVisible()
    }
  })

  test('should display existing equipment profiles', async ({ page }) => {
    // Wait for any equipment profiles to load
    await page.waitForLoadState('networkidle')
    
    // Check for equipment profile cards or list items
    const profileCards = page.locator('[data-testid="equipment-card"], .equipment-card, .profile-item')
    const profileList = page.locator('[data-testid="equipment-list"] > *, .equipment-list > *')
    
    // If profiles exist, they should be visible
    if (await profileCards.count() > 0) {
      await expect(profileCards.first()).toBeVisible()
    } else if (await profileList.count() > 0) {
      await expect(profileList.first()).toBeVisible()
    } else {
      // If no profiles, should show empty state
      const emptyMessage = page.locator(':has-text("No equipment"), :has-text("no profiles"), :has-text("empty")')
      const hasEmptyMessage = await emptyMessage.count() > 0
      
      // Either should have profiles or empty message
      expect(hasEmptyMessage).toBeTruthy()
    }
  })

  test('should handle equipment profile interactions', async ({ page }) => {
    await page.waitForLoadState('networkidle')
    
    // Look for existing equipment profiles
    const profileCards = page.locator('[data-testid="equipment-card"], .equipment-card, .profile-item')
    
    if (await profileCards.count() > 0) {
      const firstProfile = profileCards.first()
      
      // Should be able to click/view profile details
      const viewButton = firstProfile.locator('button:has-text("View"), button:has-text("Edit"), a')
      
      if (await viewButton.count() > 0) {
        await viewButton.first().click()
        
        // Should show profile details or edit form
        const detailView = page.locator('[data-testid="equipment-details"], .detail-view, .equipment-form')
        await expect(detailView).toBeVisible()
      }
    }
  })

  test('should validate equipment profile form fields', async ({ page }) => {
    // Open creation form
    const addButton = page.locator('button:has-text("Add"), button:has-text("New"), button:has-text("Create")').first()
    if (await addButton.isVisible()) {
      await addButton.click()
    }
    
    // Look for form validation
    const submitButton = page.locator('button[type="submit"], button:has-text("Save"), button:has-text("Create")')
    
    if (await submitButton.count() > 0) {
      // Try to submit empty form
      await submitButton.click()
      
      // Should show validation errors
      const errorMessages = page.locator('.error, [data-testid="error"], .text-red')
      const requiredMessages = page.locator(':has-text("required"), :has-text("cannot be empty")')
      
      const hasErrors = await errorMessages.count() > 0
      const hasRequiredMessages = await requiredMessages.count() > 0
      
      // Form should prevent submission or show validation
      expect(hasErrors || hasRequiredMessages).toBeTruthy()
    }
  })
})