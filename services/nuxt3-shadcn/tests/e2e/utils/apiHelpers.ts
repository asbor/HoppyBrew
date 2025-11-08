import type { Page, Route } from '@playwright/test'

/**
 * Mock successful response
 */
export async function mockApiSuccess<T>(
  page: Page,
  urlPattern: string | RegExp,
  responseData: T,
  statusCode = 200
) {
  await page.route(urlPattern, async (route: Route) => {
    await route.fulfill({
      status: statusCode,
      contentType: 'application/json',
      body: JSON.stringify(responseData)
    })
  })
}

/**
 * Mock error response
 */
export async function mockApiError(
  page: Page,
  urlPattern: string | RegExp,
  statusCode = 500,
  errorMessage = 'Internal Server Error'
) {
  await page.route(urlPattern, async (route: Route) => {
    await route.fulfill({
      status: statusCode,
      contentType: 'application/json',
      body: JSON.stringify({
        error: errorMessage,
        message: errorMessage,
        statusCode
      })
    })
  })
}

/**
 * Mock network delay
 */
export async function mockApiWithDelay(
  page: Page,
  urlPattern: string | RegExp,
  delayMs: number,
  responseData: unknown
) {
  await page.route(urlPattern, async (route: Route) => {
    await new Promise(resolve => setTimeout(resolve, delayMs))
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(responseData)
    })
  })
}

/**
 * Intercept and log API calls
 */
export async function interceptApiCalls(page: Page, urlPattern: string | RegExp) {
  const calls: Array<{ url: string; method: string; postData: string | null }> = []
  
  await page.route(urlPattern, async (route: Route) => {
    const request = route.request()
    calls.push({
      url: request.url(),
      method: request.method(),
      postData: request.postData()
    })
    await route.continue()
  })
  
  return calls
}

/**
 * Wait for specific API call
 */
export async function waitForApiCall(
  page: Page,
  urlPattern: string | RegExp,
  method: string = 'GET'
) {
  return await page.waitForRequest(
    request => {
      const url = request.url()
      const requestMethod = request.method()
      const matchesUrl = typeof urlPattern === 'string' 
        ? url.includes(urlPattern) 
        : urlPattern.test(url)
      return matchesUrl && requestMethod === method
    }
  )
}

/**
 * Wait for API response
 */
export async function waitForApiResponse(
  page: Page,
  urlPattern: string | RegExp,
  statusCode?: number
) {
  return await page.waitForResponse(
    response => {
      const url = response.url()
      const status = response.status()
      const matchesUrl = typeof urlPattern === 'string' 
        ? url.includes(urlPattern) 
        : urlPattern.test(url)
      return matchesUrl && (statusCode === undefined || status === statusCode)
    }
  )
}

/**
 * Mock multiple API endpoints
 */
export async function mockMultipleApis(
  page: Page,
  mocks: Array<{
    pattern: string | RegExp
    response: unknown
    status?: number
    method?: string
  }>
) {
  for (const mock of mocks) {
    await page.route(mock.pattern, async (route: Route) => {
      if (mock.method && route.request().method() !== mock.method) {
        await route.continue()
        return
      }
      
      await route.fulfill({
        status: mock.status ?? 200,
        contentType: 'application/json',
        body: JSON.stringify(mock.response)
      })
    })
  }
}

/**
 * Clear all API mocks
 */
export async function clearApiMocks(page: Page) {
  await page.unrouteAll({ behavior: 'ignoreErrors' })
}
