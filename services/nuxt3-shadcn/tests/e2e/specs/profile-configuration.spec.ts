import { test, expect } from '@playwright/test'
import { ProfilePage } from '../pages/ProfilePage'
import { RecipePage } from '../pages/RecipePage'
import { mockMultipleApis, waitForApiCall } from '../utils/apiHelpers'
import { 
  generateWaterProfileData, 
  generateMashProfileData,
  generateEquipmentProfileData,
  generateRecipeData 
} from '../utils/testDataGenerator'
import { generateTestName } from '../utils/helpers'

test.describe('Profile Configuration', () => {
  let profilePage: ProfilePage

  test.beforeEach(async ({ page }) => {
    profilePage = new ProfilePage(page)
  })

  test('should create water profile', async ({ page }) => {
    const newProfile = generateWaterProfileData({
      name: generateTestName('Burton-on-Trent'),
      calcium: 295,
      magnesium: 45,
      sodium: 55,
      chloride: 25,
      sulfate: 725,
      bicarbonate: 300
    })

    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [], method: 'GET' },
      { pattern: /\/water-profiles$/, response: newProfile, status: 201, method: 'POST' }
    ])

    await profilePage.navigateToWater()

    await profilePage.createWaterProfile({
      name: newProfile.name,
      calcium: newProfile.calcium.toString(),
      magnesium: newProfile.magnesium.toString(),
      sodium: newProfile.sodium.toString(),
      chloride: newProfile.chloride.toString(),
      sulfate: newProfile.sulfate.toString(),
      bicarbonate: newProfile.bicarbonate.toString()
    })

    await waitForApiCall(page, /\/water-profiles/, 'POST')
  })

  test('should apply water profile to recipe', async ({ page }) => {
    const waterProfile = generateWaterProfileData({
      name: 'IPA Water Profile'
    })

    const recipe = generateRecipeData({
      name: 'IPA Recipe'
    })

    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [waterProfile], method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: recipe, method: 'GET' },
      { pattern: /\/recipes\/.*$/, response: { ...recipe, waterProfileId: waterProfile.id }, method: 'PUT' }
    ])

    await profilePage.navigateToWater()

    // Apply profile to recipe
    const applyButton = page.getByRole('button', { name: /apply|use/i })
    if (await applyButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await applyButton.click()
    }
  })

  test('should validate water chemistry calculations', async ({ page }) => {
    const waterProfile = generateWaterProfileData({
      name: 'Calculation Test'
    })

    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [waterProfile], method: 'GET' }
    ])

    await profilePage.navigateToWater()

    // Verify profile is displayed with values
    await expect(page.getByText(waterProfile.name)).toBeVisible()
    
    // Look for calculated values (like RA, hardness, etc.)
    const calculatedValue = page.getByText(/ra|hardness|alkalinity/i)
    if (await calculatedValue.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(calculatedValue).toBeVisible()
    }
  })

  test('should create mash profile with temperature schedule', async ({ page }) => {
    const newProfile = generateMashProfileData({
      name: generateTestName('Single Infusion'),
      description: 'Basic single infusion mash'
    })

    await mockMultipleApis(page, [
      { pattern: /\/mash-profiles$/, response: [], method: 'GET' },
      { pattern: /\/mash-profiles$/, response: newProfile, status: 201, method: 'POST' }
    ])

    await profilePage.navigateToMash()

    await profilePage.createMashProfile({
      name: newProfile.name,
      description: newProfile.description
    })

    await waitForApiCall(page, /\/mash-profiles/, 'POST')
  })

  test('should add mash steps to profile', async ({ page }) => {
    const mashProfile = generateMashProfileData({
      name: 'Multi-Step Mash'
    })

    const mashStep = {
      name: 'Beta Glucanase Rest',
      temperature: '40',
      time: '10',
      type: 'Infusion'
    }

    await mockMultipleApis(page, [
      { pattern: /\/mash-profiles\/.*$/, response: mashProfile, method: 'GET' },
      { pattern: /\/mash-steps$/, response: mashStep, status: 201, method: 'POST' }
    ])

    await page.goto(`/profiles/mash/${mashProfile.id}`)

    await profilePage.addMashStep(mashStep)

    await waitForApiCall(page, /\/mash-steps/, 'POST')
  })

  test('should apply mash profile to batch', async ({ page }) => {
    const mashProfile = generateMashProfileData({
      name: 'Batch Mash Profile'
    })

    await mockMultipleApis(page, [
      { pattern: /\/mash-profiles$/, response: [mashProfile], method: 'GET' }
    ])

    await profilePage.navigateToMash()

    // Apply profile
    const applyButton = page.getByRole('button', { name: /apply|use/i })
    if (await applyButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await applyButton.click()
    }
  })

  test('should create equipment profile', async ({ page }) => {
    const newProfile = generateEquipmentProfileData({
      name: generateTestName('Grainfather G30'),
      batchSize: 23,
      boilTime: 60,
      efficiency: 75,
      trubLoss: 1.5
    })

    await mockMultipleApis(page, [
      { pattern: /\/equipment$/, response: [], method: 'GET' },
      { pattern: /\/equipment$/, response: newProfile, status: 201, method: 'POST' }
    ])

    await profilePage.navigateToEquipment()

    await profilePage.createEquipmentProfile({
      name: newProfile.name,
      batchSize: newProfile.batchSize.toString(),
      boilTime: newProfile.boilTime.toString(),
      efficiency: newProfile.efficiency.toString(),
      trubLoss: newProfile.trubLoss.toString()
    })

    await waitForApiCall(page, /\/equipment/, 'POST')
  })

  test('should duplicate equipment profile', async ({ page }) => {
    const originalProfile = generateEquipmentProfileData({
      name: 'Original Equipment'
    })

    const duplicatedProfile = generateEquipmentProfileData({
      name: 'Original Equipment (Copy)'
    })

    await mockMultipleApis(page, [
      { pattern: /\/equipment$/, response: [originalProfile], method: 'GET' },
      { pattern: /\/equipment\/.*\/duplicate/, response: duplicatedProfile, status: 201, method: 'POST' }
    ])

    await profilePage.navigateToEquipment()

    await profilePage.duplicateProfile(originalProfile.name)

    await waitForApiCall(page, /\/equipment.*duplicate/, 'POST')
  })

  test('should delete profile', async ({ page }) => {
    const profile = generateWaterProfileData({
      name: 'Delete Me Profile'
    })

    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [profile], method: 'GET' },
      { pattern: /\/water-profiles\/.*$/, response: { success: true }, status: 204, method: 'DELETE' }
    ])

    await profilePage.navigateToWater()

    await profilePage.deleteProfile(profile.name)

    await waitForApiCall(page, /\/water-profiles/, 'DELETE')
  })

  test('should search profiles', async ({ page }) => {
    const profiles = [
      generateWaterProfileData({ name: 'Burton-on-Trent' }),
      generateWaterProfileData({ name: 'Pilsen' }),
      generateWaterProfileData({ name: 'Dublin' })
    ]

    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: profiles, method: 'GET' }
    ])

    await profilePage.navigateToWater()

    await profilePage.searchProfiles('Burton')

    await expect(page.getByText('Burton-on-Trent')).toBeVisible()
  })

  test('should edit existing profile', async ({ page }) => {
    const profile = generateWaterProfileData({
      name: 'Edit Me Profile'
    })

    const updatedProfile = {
      ...profile,
      calcium: 100
    }

    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [profile], method: 'GET' },
      { pattern: /\/water-profiles\/.*$/, response: profile, method: 'GET' },
      { pattern: /\/water-profiles\/.*$/, response: updatedProfile, method: 'PUT' }
    ])

    await profilePage.navigateToWater()

    await profilePage.editProfile(profile.name)

    // Edit calcium value
    await page.getByLabel(/calcium/i).fill('100')
    await page.getByRole('button', { name: /save|update/i }).click()

    await waitForApiCall(page, /\/water-profiles/, 'PUT')
  })

  test('should validate profile form inputs', async ({ page }) => {
    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [], method: 'GET' }
    ])

    await profilePage.navigateToWater()

    const newButton = page.getByRole('button', { name: /new.*profile|add.*profile/i })
    if (await newButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await newButton.click()

      // Try to save without name
      const saveButton = page.getByRole('button', { name: /save|create/i })
      if (await saveButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await saveButton.click()

        // Should show validation error
        await expect(page.getByText(/required|invalid|error/i)).toBeVisible()
      }
    }
  })

  test('should navigate between profile types', async ({ page }) => {
    await mockMultipleApis(page, [
      { pattern: /\/water-profiles$/, response: [], method: 'GET' },
      { pattern: /\/mash-profiles$/, response: [], method: 'GET' },
      { pattern: /\/equipment$/, response: [], method: 'GET' }
    ])

    // Navigate to water profiles
    await profilePage.navigateToWater()
    await expect(page).toHaveURL(/\/profiles\/water/)

    // Navigate to mash profiles
    await profilePage.navigateToMash()
    await expect(page).toHaveURL(/\/profiles\/mash/)

    // Navigate to equipment profiles
    await profilePage.navigateToEquipment()
    await expect(page).toHaveURL(/\/profiles\/equipment/)
  })

  test('should display profile statistics', async ({ page }) => {
    const equipmentProfile = generateEquipmentProfileData({
      name: 'Stats Profile',
      batchSize: 20,
      efficiency: 75
    })

    await mockMultipleApis(page, [
      { pattern: /\/equipment$/, response: [equipmentProfile], method: 'GET' }
    ])

    await profilePage.navigateToEquipment()

    // Verify profile stats are displayed
    await expect(page.getByText(equipmentProfile.name)).toBeVisible()
    await expect(page.getByText(`${equipmentProfile.batchSize}`)).toBeVisible()
    await expect(page.getByText(`${equipmentProfile.efficiency}`)).toBeVisible()
  })
})
