describe("The manage page", () => {
  it("has a form", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)")
      .scrollIntoView()
      .should("have.attr", "method", "POST")
      .should("have.attr", "action", "/wtm/manage/");

    cy.get("form:not(.form)")
      .scrollIntoView()
      .find("input[type='checkbox']")
      .then((results) => {
        expect(results).to.have.length(4);
        expect(results[0]).to.be.disabled;
        expect(results[1]).to.be.checked;
        expect(results[2]).to.be.checked;
        expect(results[3]).to.not.be.checked;
      });
  });

  it("should not have a visible cookie bar", () => {
    cy.visit("/wtm/manage/");

    cy.get("#wtm_cookie_bar").should("have.class", "hidden").should("not.be.visible");
  });

  it("can save default cookies", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)").scrollIntoView()
    cy.get("form:not(.form) input[type='submit']").click();

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only necesarry cookies", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)").scrollIntoView()
    cy.get("form:not(.form) input#id_preferences").click();
    cy.get("form:not(.form) input#id_statistics").click();
    cy.get("form:not(.form) input[type='submit']").click();

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:false|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only preference cookies", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)").scrollIntoView()
    cy.get("form:not(.form) input#id_statistics").click();
    cy.get("form:not(.form) input[type='submit']").click();

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:false|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only statistical cookies", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)").scrollIntoView()
    cy.get("form:not(.form) input#id_preferences").click();
    cy.get("form:not(.form) input[type='submit']").click();

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:true|marketing:false"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can set only marketing cookies", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)").scrollIntoView()
    cy.get("form:not(.form) input#id_preferences").click();
    cy.get("form:not(.form) input#id_statistics").click();
    cy.get("form:not(.form) input#id_marketing").click();
    cy.get("form:not(.form) input[type='submit']").click();

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:false|marketing:true"
    );
    cy.getCookie("wtm_id").should("exist");
  });

  it("can enable all cookies", () => {
    cy.visit("/wtm/manage/");

    cy.get("form:not(.form)").scrollIntoView()
    cy.get("form:not(.form) input#id_marketing").click();
    cy.get("form:not(.form) input[type='submit']").click();

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:true|statistics:true|marketing:true"
    );
    cy.getCookie("wtm_id").should("exist");
  });
});
