// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import "./commands";

// Alternatively you can use CommonJS syntax:
// require('./commands')

Cypress.Cookies.debug(true, { verbose: false });

before("login to admin", () => {
  cy.clearCookies();
  cy.visit("/cms/");
  cy.get("#id_username").type("superuser");
  cy.get("#id_password").type("testing");
  cy.get("button[type='submit']").click();
});

beforeEach("configure cookies", () => {
  window.localStorage.setItem("djdt.show", "false");
  Cypress.Cookies.preserveOnce("csrftoken", "sessionid");
});
