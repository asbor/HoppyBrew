import { type Page } from '@playwright/test'
import { BasePage } from './BasePage'

/**
 * Page Object Model for Profile pages (Water, Mash, Equipment, Fermentation)
 */
export class ProfilePage extends BasePage {
  constructor(page: Page) {
    super(page)
  }

  /**
   * Navigate to profiles overview
   */
  async navigateToOverview() {
    await this.goto('/profiles')
  }

  /**
   * Navigate to water profiles
   */
  async navigateToWater() {
    await this.goto('/profiles/water')
  }

  /**
   * Navigate to mash profiles
   */
  async navigateToMash() {
    await this.goto('/profiles/mash')
  }

  /**
   * Navigate to equipment profiles
   */
  async navigateToEquipment() {
    await this.goto('/profiles/equipment')
  }

  /**
   * Navigate to fermentation profiles
   */
  async navigateToFermentation() {
    await this.goto('/profiles/fermentation')
  }

  /**
   * Create new water profile
   */
  async createWaterProfile(data: {
    name: string
    calcium?: string
    magnesium?: string
    sodium?: string
    chloride?: string
    sulfate?: string
    bicarbonate?: string
  }) {
    await this.clickButton(/New Profile|Add Profile/i)

    await this.fillInput(/Name/i, data.name)
    
    if (data.calcium) {
      await this.fillInput(/Calcium/i, data.calcium)
    }
    if (data.magnesium) {
      await this.fillInput(/Magnesium/i, data.magnesium)
    }
    if (data.sodium) {
      await this.fillInput(/Sodium/i, data.sodium)
    }
    if (data.chloride) {
      await this.fillInput(/Chloride/i, data.chloride)
    }
    if (data.sulfate) {
      await this.fillInput(/Sulfate/i, data.sulfate)
    }
    if (data.bicarbonate) {
      await this.fillInput(/Bicarbonate/i, data.bicarbonate)
    }

    await this.clickButton(/Save|Create/i)
  }

  /**
   * Create new mash profile
   */
  async createMashProfile(data: {
    name: string
    description?: string
  }) {
    await this.clickButton(/New Profile|Add Profile/i)

    await this.fillInput(/Name/i, data.name)
    
    if (data.description) {
      await this.fillInput(/Description/i, data.description)
    }

    await this.clickButton(/Save|Create/i)
  }

  /**
   * Add mash step to profile
   */
  async addMashStep(data: {
    name: string
    temperature: string
    time: string
    type?: string
  }) {
    await this.clickButton(/Add Step/i)

    await this.fillInput(/Step Name/i, data.name)
    await this.fillInput(/Temperature/i, data.temperature)
    await this.fillInput(/Time/i, data.time)
    
    if (data.type) {
      await this.fillInput(/Type/i, data.type)
    }

    await this.clickButton(/Save Step/i)
  }

  /**
   * Create new equipment profile
   */
  async createEquipmentProfile(data: {
    name: string
    batchSize?: string
    boilTime?: string
    efficiency?: string
    trubLoss?: string
  }) {
    await this.clickButton(/New Profile|Add Profile/i)

    await this.fillInput(/Name/i, data.name)
    
    if (data.batchSize) {
      await this.fillInput(/Batch Size/i, data.batchSize)
    }
    if (data.boilTime) {
      await this.fillInput(/Boil Time/i, data.boilTime)
    }
    if (data.efficiency) {
      await this.fillInput(/Efficiency/i, data.efficiency)
    }
    if (data.trubLoss) {
      await this.fillInput(/Trub.*Loss/i, data.trubLoss)
    }

    await this.clickButton(/Save|Create/i)
  }

  /**
   * Duplicate a profile
   */
  async duplicateProfile(profileName: string) {
    await this.getByText(profileName).click()
    await this.clickButton(/Duplicate|Clone|Copy/i)
  }

  /**
   * Delete a profile
   */
  async deleteProfile(profileName: string) {
    await this.getByText(profileName).click()
    await this.clickButton(/Delete|Remove/i)
    
    // Confirm deletion if dialog appears
    const confirmButton = this.page.getByRole('button', { name: /Confirm|Yes|Delete/i })
    if (await confirmButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await confirmButton.click()
    }
  }

  /**
   * Apply profile to recipe
   */
  async applyProfileToRecipe(profileName: string) {
    await this.getByText(profileName).click()
    await this.clickButton(/Apply|Use Profile/i)
  }

  /**
   * Verify profile in list
   */
  async verifyProfileInList(profileName: string) {
    await this.waitForText(profileName)
  }

  /**
   * Edit profile
   */
  async editProfile(profileName: string) {
    await this.getByText(profileName).click()
    await this.clickButton(/Edit/i)
  }

  /**
   * Search profiles
   */
  async searchProfiles(searchTerm: string) {
    const searchInput = this.getByPlaceholder(/Search/i)
    await searchInput.fill(searchTerm)
  }
}
