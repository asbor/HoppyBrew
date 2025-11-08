import { type Page } from '@playwright/test'
import { BasePage } from './BasePage'

/**
 * Page Object Model for Recipe pages
 */
export class RecipePage extends BasePage {
  constructor(page: Page) {
    super(page)
  }

  /**
   * Navigate to recipes list page
   */
  async navigateToList() {
    await this.goto('/recipes')
  }

  /**
   * Navigate to new recipe page
   */
  async navigateToNew() {
    await this.goto('/recipes/newRecipe')
  }

  /**
   * Navigate to recipe details by ID
   */
  async navigateToDetails(recipeId: string) {
    await this.goto(`/recipes/${recipeId}`)
  }

  /**
   * Click New Recipe button
   */
  async clickNewRecipe() {
    await this.clickButton('New Recipe')
  }

  /**
   * Search for recipes
   */
  async searchRecipes(searchTerm: string) {
    const searchInput = this.getByPlaceholder(/Search recipes/i)
    await searchInput.fill(searchTerm)
  }

  /**
   * Fill recipe basic information
   */
  async fillRecipeBasicInfo(data: {
    name: string
    type?: string
    style?: string
    batchSize?: string
    boilTime?: string
  }) {
    if (data.name) {
      await this.fillInput(/Recipe Name/i, data.name)
    }
    if (data.type) {
      await this.fillInput(/Recipe Type/i, data.type)
    }
    if (data.style) {
      await this.fillInput(/Style/i, data.style)
    }
    if (data.batchSize) {
      await this.fillInput(/Batch Size/i, data.batchSize)
    }
    if (data.boilTime) {
      await this.fillInput(/Boil Time/i, data.boilTime)
    }
  }

  /**
   * Save recipe
   */
  async saveRecipe() {
    await this.clickButton(/Save|Create/i)
  }

  /**
   * Clone a recipe
   */
  async cloneRecipe() {
    await this.clickButton(/Clone|Duplicate/i)
  }

  /**
   * Delete a recipe
   */
  async deleteRecipe() {
    await this.clickButton(/Delete/i)
  }

  /**
   * Verify recipe appears in list
   */
  async verifyRecipeInList(recipeName: string) {
    await this.waitForText(recipeName)
  }

  /**
   * Click on a recipe in the list
   */
  async clickRecipeInList(recipeName: string) {
    await this.getByRole('cell', { name: recipeName }).click()
  }

  /**
   * Switch to card view
   */
  async switchToCardView() {
    await this.getByRole('link', { name: 'Card View' }).click()
  }

  /**
   * Switch to table view
   */
  async switchToTableView() {
    await this.getByRole('link', { name: 'Table View' }).click()
  }
}
