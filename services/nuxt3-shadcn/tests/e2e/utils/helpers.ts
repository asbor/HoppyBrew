import { type Page } from '@playwright/test'

/**
 * Wait for a condition to be true with retries
 */
export async function waitForCondition(
  fn: () => Promise<boolean>,
  options: {
    timeout?: number
    interval?: number
    message?: string
  } = {}
): Promise<void> {
  const { timeout = 30000, interval = 500, message = 'Condition not met' } = options
  
  const startTime = Date.now()
  
  while (Date.now() - startTime < timeout) {
    if (await fn()) {
      return
    }
    await new Promise(resolve => setTimeout(resolve, interval))
  }
  
  throw new Error(`${message} (timeout: ${timeout}ms)`)
}

/**
 * Retry an action multiple times
 */
export async function retry<T>(
  fn: () => Promise<T>,
  options: {
    maxAttempts?: number
    delay?: number
    onError?: (error: Error, attempt: number) => void
  } = {}
): Promise<T> {
  const { maxAttempts = 3, delay = 1000, onError } = options
  
  let lastError: Error | undefined
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      if (onError) {
        onError(lastError, attempt)
      }
      
      if (attempt < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }
  
  throw lastError || new Error('Retry failed')
}

/**
 * Wait for network to be idle
 */
export async function waitForNetworkIdle(page: Page, timeout = 30000): Promise<void> {
  await page.waitForLoadState('networkidle', { timeout })
}

/**
 * Wait for element to disappear
 */
export async function waitForElementToDisappear(
  page: Page,
  selector: string,
  timeout = 10000
): Promise<void> {
  await page.waitForSelector(selector, { state: 'hidden', timeout })
}

/**
 * Scroll element into view
 */
export async function scrollIntoView(page: Page, selector: string): Promise<void> {
  await page.locator(selector).scrollIntoViewIfNeeded()
}

/**
 * Take screenshot with timestamp
 */
export async function takeTimestampedScreenshot(
  page: Page,
  name: string,
  options?: {
    fullPage?: boolean
    path?: string
  }
): Promise<Buffer> {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const filename = `${name}-${timestamp}.png`
  
  return await page.screenshot({
    fullPage: options?.fullPage ?? false,
    path: options?.path ? `${options.path}/${filename}` : undefined
  })
}

/**
 * Clear local storage
 */
export async function clearLocalStorage(page: Page): Promise<void> {
  await page.evaluate(() => {
    localStorage.clear()
  })
}

/**
 * Clear session storage
 */
export async function clearSessionStorage(page: Page): Promise<void> {
  await page.evaluate(() => {
    sessionStorage.clear()
  })
}

/**
 * Clear all storage
 */
export async function clearAllStorage(page: Page): Promise<void> {
  await clearLocalStorage(page)
  await clearSessionStorage(page)
}

/**
 * Get local storage item
 */
export async function getLocalStorageItem(page: Page, key: string): Promise<string | null> {
  return await page.evaluate((storageKey) => {
    return localStorage.getItem(storageKey)
  }, key)
}

/**
 * Set local storage item
 */
export async function setLocalStorageItem(page: Page, key: string, value: string): Promise<void> {
  await page.evaluate(({ storageKey, storageValue }) => {
    localStorage.setItem(storageKey, storageValue)
  }, { storageKey: key, storageValue: value })
}

/**
 * Check if element is visible
 */
export async function isVisible(page: Page, selector: string): Promise<boolean> {
  try {
    const element = page.locator(selector)
    return await element.isVisible({ timeout: 1000 })
  } catch {
    return false
  }
}

/**
 * Wait for URL to match pattern
 */
export async function waitForURL(
  page: Page,
  pattern: string | RegExp,
  timeout = 10000
): Promise<void> {
  await page.waitForURL(pattern, { timeout })
}

/**
 * Get current timestamp for test data
 */
export function getTimestamp(): string {
  return new Date().toISOString()
}

/**
 * Generate random string
 */
export function randomString(length = 10): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * Generate unique test name
 */
export function generateTestName(prefix: string): string {
  return `${prefix}-${randomString(8)}`
}
