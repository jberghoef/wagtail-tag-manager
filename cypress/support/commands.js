// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.on("window:before:load", (win) => {
  win.fetch = null;
});

Cypress.Commands.add("setConsent", (content) => {
  return cy.setCookie("wtm", encodeURIComponent(btoa(JSON.stringify(content))));
});

Cypress.Commands.add("getConsent", () => {
  return cy.getCookie("wtm").then((cookie) => {
    if (cookie && cookie.value) {
      return JSON.parse(atob(decodeURIComponent(cookie.value)));
    }
    return {};
  });
});
