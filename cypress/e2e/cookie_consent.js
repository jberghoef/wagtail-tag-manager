describe("Cookie consent", () => {
  it("will be registered", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_marketing").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.visit("/cms/reports/cookie-consent/");
    cy.getCookie("wtm_id").then((cookie) => {
      cy.get(".listing tbody tr:first td > b").contains(cookie.value);
    });
  });

  it("will be invalidated", () => {
    cy.on("uncaught:exception", (err, runnable) => {
      return false;
    });

    // Configure condition page
    cy.visit("/cms/settings/wagtail_tag_manager/cookieconsentsettings/1/");
    cy.get("button[data-chooser-action-choose]").click({ force: true, multiple: true });
    cy.get(".modal-content").should("be.visible");
    cy.get("a[data-title='Wagtail Tag Manager']").click({
      force: true,
      multiple: true,
    });
    cy.get(".actions button[type='submit']").click();

    // Register consent
    cy.visit("/");
    cy.get("#wtm_cookie_bar input[type='submit']").click();
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:false",
    );
    cy.getCookie("wtm_id").should("exist");

    // Change homepage
    cy.visit("/cms/pages/2/edit/");
    cy.get(".dropdown-toggle").click({ force: true });
    cy.get("[name='action-publish']").click({ force: true });

    // Visit homepage
    cy.visit("/");
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:unset|statistics:pending|marketing:false",
    );
  });

  it("will not be invalidated", () => {
    cy.on("uncaught:exception", (err, runnable) => {
      return false;
    });

    // Remove condition page
    cy.visit("/cms/settings/wagtail_tag_manager/cookieconsentsettings/1/");
    cy.get("button[aria-label='Actions']").click({ force: true });
    cy.get("button[data-chooser-action-clear]").click({ force: true });
    cy.get(".actions button[type='submit']").click();

    // Register consent
    cy.visit("/");
    cy.get("#wtm_cookie_bar input[type='submit']").click();
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:false",
    );
    cy.getCookie("wtm_id").should("exist");

    // Change homepage
    cy.visit("/cms/pages/2/edit/");
    cy.get(".dropdown-toggle").click({ force: true });
    cy.get("[name='action-publish']").click({ force: true });

    // Visit homepage
    cy.visit("/");
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:false",
    );
  });
});
