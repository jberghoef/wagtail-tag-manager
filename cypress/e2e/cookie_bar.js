beforeEach("clear wtm cookies", () => {
  cy.clearCookie("wtm", { timeout: 1000 });
  cy.clearCookie("wtm_id", { timeout: 1000 });
});

describe("The cookie bar", () => {
  it("can save default cookies", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only necesarry cookies", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_preferences").click();
    cy.get("#wtm_cookie_bar input#id_statistics").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:false|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only preference cookies", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_statistics").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:false|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only statistical cookies", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_preferences").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:true|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only marketing cookies", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_preferences").click();
    cy.get("#wtm_cookie_bar input#id_statistics").click();
    cy.get("#wtm_cookie_bar input#id_marketing").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:false|marketing:true"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can enable all cookies", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_marketing").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:true"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("is displayed when preference cookies are 'unset'", () => {
    cy.setCookie("wtm", "necessary:true|preferences:unset|statistics:false|marketing:false");
    cy.visit("/");
    cy.get("#wtm_cookie_bar").should("not.have.class", "hidden").should("be.visible");
  });

  it("is displayed when statistical cookies are 'unset'", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:unset|marketing:false");
    cy.visit("/");
    cy.get("#wtm_cookie_bar").should("not.have.class", "hidden").should("be.visible");
  });

  it("is hidden when all cookies are 'false'", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:false");
    cy.visit("/");
    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");
  });

  it("is hidden when all cookies are 'true'", () => {
    cy.setCookie("wtm", "necessary:true|preferences:true|statistics:true|marketing:true");
    cy.visit("/");
    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");
  });

  it("has a functional 'manage' link", () => {
    cy.visit("/");
    cy.get("#wtm_cookie_bar").find(".manage-link a").click();
    cy.url().should("include", "/wtm/manage/");
  });
});
