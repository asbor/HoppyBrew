import { test, expect } from '@playwright/test'
import { mockEquipmentApi } from '../fixtures/mockApi'
import { equipmentFixtures } from '../fixtures/testData'

test.describe('Equipment profiles page', () => {
  test.beforeEach(async ({ page }) => {
    await mockEquipmentApi(page)
    await page.goto('/profiles/equipment')
  })

  test('renders equipment cards with calculated stats', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Equipment Profiles' })).toBeVisible()
    await expect(page.getByText('Manage your brewing equipment configurations and volume calculations')).toBeVisible()
    await expect(page.getByRole('button', { name: 'New Profile' })).toBeVisible()

    const firstProfile = equipmentFixtures[0]
    await expect(page.getByText(firstProfile.name)).toBeVisible()
    await expect(page.getByText(`${firstProfile.batch_size}L`).first()).toBeVisible()
    await expect(page.getByText(`Trub/Chiller: ${firstProfile.trub_chiller_loss}L`)).toBeVisible()
    await expect(page.getByText(`Boil Time: ${firstProfile.boil_time}min`)).toBeVisible()
  })

  test('opens and closes the new equipment dialog', async ({ page }) => {
    await page.getByRole('button', { name: 'New Profile' }).click()
    await expect(page.getByRole('heading', { name: 'Create Equipment Profile' })).toBeVisible()
    await page.getByRole('button', { name: 'Cancel' }).click()
    await expect(page.getByRole('heading', { name: 'Create Equipment Profile' })).toHaveCount(0)
  })

  test('duplicates an equipment profile with copy suffix', async ({ page }) => {
    const [request] = await Promise.all([
      page.waitForRequest(req => req.url().includes('/equipment') && req.method() === 'POST'),
      page.getByTitle('Duplicate').first().click()
    ])

    const payload = request.postDataJSON()
    await expect(page.getByTitle('Duplicate').first()).toBeVisible()
    expect(payload.name).toContain('(Copy)')
  })
})
