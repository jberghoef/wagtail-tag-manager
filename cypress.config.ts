import { defineConfig } from 'cypress'

export default defineConfig({
  defaultCommandTimeout: 8000,
  requestTimeout: 10000,
  chromeWebSecurity: false,
  projectId: 'zprv4r',
  retries: {
    runMode: 2,
    openMode: 0,
  },
  e2e: {
    // We've imported your old cypress plugins here.
    // You may want to clean this up later by importing these.
    setupNodeEvents(on, config) {
      return require('./cypress/plugins/index.js')(on, config)
    },
    baseUrl: 'http://127.0.0.1:8000',
    specPattern: 'cypress/e2e/**/*.{js,jsx,ts,tsx}',
  },
})
