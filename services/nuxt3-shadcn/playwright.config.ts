import { defineConfig, devices, type ReporterDescription } from '@playwright/test'
import { fileURLToPath } from 'node:url'
import { dirname } from 'node:path'

const baseDir = dirname(fileURLToPath(import.meta.url))
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? 'http://127.0.0.1:3000'
const isCI = !!process.env.CI
const testTimeout = isCI ? 90_000 : 60_000
const expectTimeout = isCI ? 10_000 : 5_000
const reporters: ReporterDescription[] = [
  ['list'],
  ['html', { open: 'never' }]
]

if (isCI) {
  reporters.unshift(['github'])
}

export default defineConfig({
  testDir: './tests/e2e/specs',
  fullyParallel: true,
  forbidOnly: isCI,
  retries: isCI ? 2 : 0,
  workers: isCI ? 3 : undefined,
  timeout: testTimeout,
  expect: {
    timeout: expectTimeout
  },
  reporter: reporters,
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: isCI ? 15_000 : undefined,
    navigationTimeout: isCI ? 30_000 : undefined
  },
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: 'yarn dev --hostname 0.0.0.0 --port 3000',
        url: 'http://127.0.0.1:3000',
        reuseExistingServer: !isCI,
        timeout: 180000,
        cwd: baseDir
      },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    }
  ]
})
