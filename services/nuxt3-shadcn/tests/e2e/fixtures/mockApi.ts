import type { Page, Route } from '@playwright/test'
import { equipmentFixtures, recipeFixtures } from './testData'

const jsonHeaders = { 'content-type': 'application/json' }

const fulfill = (route: Route, body: unknown, status = 200) =>
  route.fulfill({
    status,
    headers: jsonHeaders,
    body: JSON.stringify(body)
  })

const extractResourceId = (url: string, resource: string) => {
  const segments = new URL(url).pathname.split('/').filter(Boolean)
  const resourceIndex = segments.indexOf(resource)

  if (resourceIndex === -1) return null
  if (segments.length <= resourceIndex + 1) return null

  return segments[resourceIndex + 1]
}

export const mockRecipesApi = async (page: Page) => {
  await page.route('**/recipes*', async route => {
    const method = route.request().method()
    if (method === 'GET') {
      const recipeId = extractResourceId(route.request().url(), 'recipes')
      if (recipeId) {
        const recipe = recipeFixtures.find(item => item.id === recipeId) ?? recipeFixtures[0]
        return fulfill(route, recipe)
      }

      return fulfill(route, recipeFixtures)
    }

    return fulfill(route, { ok: true })
  })
}

export const mockEquipmentApi = async (page: Page) => {
  await page.route('**/equipment*', async route => {
    if (route.request().method() === 'GET') {
      return fulfill(route, equipmentFixtures)
    }

    return fulfill(route, { ok: true })
  })
}
