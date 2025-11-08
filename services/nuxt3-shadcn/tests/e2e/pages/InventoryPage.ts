import { type Page } from '@playwright/test'
import { BasePage } from './BasePage'

/**
 * Page Object Model for Inventory pages
 */
export class InventoryPage extends BasePage {
  constructor(page: Page) {
    super(page)
  }

  /**
   * Navigate to inventory overview page
   */
  async navigateToOverview() {
    await this.goto('/inventory')
  }

  /**
   * Navigate to hops inventory
   */
  async navigateToHops() {
    await this.goto('/inventory/hops')
  }

  /**
   * Navigate to fermentables inventory
   */
  async navigateToFermentables() {
    await this.goto('/inventory/fermentables')
  }

  /**
   * Navigate to yeasts inventory
   */
  async navigateToYeasts() {
    await this.goto('/inventory/yeasts')
  }

  /**
   * Navigate to miscs inventory
   */
  async navigateToMiscs() {
    await this.goto('/inventory/miscs')
  }

  /**
   * Add new inventory item
   */
  async addInventoryItem(data: {
    name: string
    quantity?: string
    unit?: string
    cost?: string
  }) {
    await this.clickButton(/Add|New/i)

    await this.fillInput(/Name/i, data.name)
    
    if (data.quantity) {
      await this.fillInput(/Quantity|Amount/i, data.quantity)
    }
    if (data.unit) {
      await this.fillInput(/Unit/i, data.unit)
    }
    if (data.cost) {
      await this.fillInput(/Cost|Price/i, data.cost)
    }

    await this.clickButton(/Save|Add/i)
  }

  /**
   * Update inventory quantity
   */
  async updateQuantity(itemName: string, newQuantity: string) {
    // Find the item row and click edit
    await this.getByText(itemName).click()
    await this.clickButton(/Edit/i)
    
    // Update quantity
    await this.fillInput(/Quantity|Amount/i, newQuantity)
    await this.clickButton(/Save|Update/i)
  }

  /**
   * Search inventory
   */
  async searchInventory(searchTerm: string) {
    const searchInput = this.getByPlaceholder(/Search/i)
    await searchInput.fill(searchTerm)
  }

  /**
   * Filter by low stock
   */
  async filterByLowStock() {
    await this.clickButton(/Low Stock|Filter/i)
  }

  /**
   * Verify item in inventory
   */
  async verifyItemInInventory(itemName: string) {
    await this.waitForText(itemName)
  }

  /**
   * Delete inventory item
   */
  async deleteItem(itemName: string) {
    await this.getByText(itemName).click()
    await this.clickButton(/Delete|Remove/i)
    // Confirm deletion if dialog appears
    const confirmButton = this.page.getByRole('button', { name: /Confirm|Yes|Delete/i })
    if (await confirmButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await confirmButton.click()
    }
  }

  /**
   * Verify low stock alert
   */
  async verifyLowStockAlert(itemName: string) {
    // Look for alert badge or indicator near the item
    await this.waitForText(itemName)
    await this.waitForText(/Low Stock|Alert/i)
  }

  /**
   * Export inventory
   */
  async exportInventory() {
    await this.clickButton(/Export/i)
  }

  /**
   * Import inventory
   */
  async importInventory(filePath: string) {
    await this.clickButton(/Import/i)
    const fileInput = this.page.locator('input[type="file"]')
    await fileInput.setInputFiles(filePath)
  }
}
