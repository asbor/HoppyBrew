import { type Page } from '@playwright/test'
import { BasePage } from './BasePage'

/**
 * Page Object Model for Batch pages
 */
export class BatchPage extends BasePage {
  constructor(page: Page) {
    super(page)
  }

  /**
   * Navigate to batches list page
   */
  async navigateToList() {
    await this.goto('/batches')
  }

  /**
   * Navigate to new batch page
   */
  async navigateToNew() {
    await this.goto('/batches/newBatch')
  }

  /**
   * Navigate to batch details by ID
   */
  async navigateToDetails(batchId: string) {
    await this.goto(`/batches/${batchId}`)
  }

  /**
   * Click New Batch button
   */
  async clickNewBatch() {
    await this.clickButton(/New Batch/i)
  }

  /**
   * Start a batch from a recipe
   */
  async startBatchFromRecipe(recipeName: string) {
    await this.getByText(recipeName).click()
    await this.clickButton(/Start Batch|Create Batch/i)
  }

  /**
   * Fill batch information
   */
  async fillBatchInfo(data: {
    name?: string
    brewDate?: string
    notes?: string
  }) {
    if (data.name) {
      await this.fillInput(/Batch Name/i, data.name)
    }
    if (data.brewDate) {
      await this.fillInput(/Brew Date/i, data.brewDate)
    }
    if (data.notes) {
      await this.fillInput(/Notes/i, data.notes)
    }
  }

  /**
   * Add fermentation reading
   */
  async addFermentationReading(data: {
    gravity?: string
    temperature?: string
    pH?: string
    date?: string
  }) {
    await this.clickButton(/Add Reading/i)
    
    if (data.gravity) {
      await this.fillInput(/Gravity/i, data.gravity)
    }
    if (data.temperature) {
      await this.fillInput(/Temperature/i, data.temperature)
    }
    if (data.pH) {
      await this.fillInput(/pH/i, data.pH)
    }
    if (data.date) {
      await this.fillInput(/Date/i, data.date)
    }

    await this.clickButton(/Save Reading/i)
  }

  /**
   * Update batch status
   */
  async updateBatchStatus(status: string) {
    await this.clickButton(/Status|Update Status/i)
    await this.getByText(status).click()
  }

  /**
   * Search batches
   */
  async searchBatches(searchTerm: string) {
    const searchInput = this.getByPlaceholder(/Search batches/i)
    await searchInput.fill(searchTerm)
  }

  /**
   * Verify batch appears in list
   */
  async verifyBatchInList(batchName: string) {
    await this.waitForText(batchName)
  }

  /**
   * Click on a batch in the list
   */
  async clickBatchInList(batchName: string) {
    await this.getByRole('cell', { name: batchName }).click()
  }

  /**
   * Complete batch
   */
  async completeBatch() {
    await this.clickButton(/Complete|Finish/i)
  }

  /**
   * Archive batch
   */
  async archiveBatch() {
    await this.clickButton(/Archive/i)
  }
}
