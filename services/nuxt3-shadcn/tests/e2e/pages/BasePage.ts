import { type Page, type Locator } from '@playwright/test'

/**
 * Base Page class providing common functionality for all page objects
 */
export class BasePage {
  protected page: Page

  constructor(page: Page) {
    this.page = page
  }

  /**
   * Navigate to a specific path
   */
  async goto(path: string) {
    await this.page.goto(path)
  }

  /**
   * Wait for page to be fully loaded
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle')
  }

  /**
   * Get element by role
   */
  getByRole(role: Parameters<Page['getByRole']>[0], options?: Parameters<Page['getByRole']>[1]): Locator {
    return this.page.getByRole(role, options)
  }

  /**
   * Get element by text
   */
  getByText(text: string | RegExp, options?: { exact?: boolean }): Locator {
    return this.page.getByText(text, options)
  }

  /**
   * Get element by placeholder
   */
  getByPlaceholder(text: string | RegExp): Locator {
    return this.page.getByPlaceholder(text)
  }

  /**
   * Get element by label
   */
  getByLabel(text: string | RegExp): Locator {
    return this.page.getByLabel(text)
  }

  /**
   * Click a button by name
   */
  async clickButton(name: string | RegExp) {
    await this.getByRole('button', { name }).click()
  }

  /**
   * Fill input field by label
   */
  async fillInput(label: string | RegExp, value: string) {
    await this.getByLabel(label).fill(value)
  }

  /**
   * Wait for element to be visible
   */
  async waitForVisible(locator: Locator) {
    await locator.waitFor({ state: 'visible' })
  }

  /**
   * Wait for text to appear
   */
  async waitForText(text: string | RegExp) {
    await this.getByText(text).waitFor({ state: 'visible' })
  }
}
