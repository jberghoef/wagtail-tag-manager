describe("The website", () => {
  it("contains base configuration", () => {
    cy.visit("/");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:unset|statistics:unset|marketing:false"
    );

    cy.get("body")
      .should("have.attr", "data-wtm-config", "/wtm/config/")
      .should("have.attr", "data-wtm-lazy", "/wtm/lazy/");

    cy.get("link[href='/static/wagtail_tag_manager/wtm.bundle.css']");
    cy.get("script[src='/static/wagtail_tag_manager/wtm.bundle.js']");
  });

  it("has a configured cookie bar", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar")
      .should("be.visible")
      .should("have.class", "cleanslate")
      .contains("This website uses cookies");

    cy.get("#wtm_cookie_bar")
      .find("form")
      .should("have.class", "form")
      .should("have.attr", "method", "POST")
      .should("have.attr", "action", "/wtm/manage/");

    cy.get("#wtm_cookie_bar")
      .find("form")
      .find("input[type='checkbox']")
      .then((results) => {
        expect(results).to.have.length(4);
        expect(results[0]).to.be.disabled;
        expect(results[1]).to.be.checked;
        expect(results[2]).to.be.checked;
        expect(results[3]).to.not.be.checked;
      });

    cy.get("#wtm_cookie_bar")
      .find(".manage-link")
      .find("a")
      .should("have.attr", "href", "/wtm/manage/")
      .contains("Manage settings");

    cy.get("#wtm_cookie_bar").find("input[type='submit']").should("have.value", "Save");
  });
});

describe("The API", () => {
  it("returns a valid config", () => {
    cy.server();
    cy.route("GET", "/wtm/config/*").as("config");
    cy.visit("/");

    cy.wait("@config").should((xhr) => {
      expect(xhr.status, "successful GET").to.equal(200);
    });
  });

  it("returns a valid lazy state", () => {
    cy.server();
    cy.route("POST", "/wtm/lazy/").as("lazy");
    cy.visit("/");

    cy.wait("@lazy").should((xhr) => {
      expect(xhr.status, "successful POST").to.equal(200);
    });
  });
});
