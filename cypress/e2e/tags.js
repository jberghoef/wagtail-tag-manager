describe("Necessary tags", () => {
  it("will be loaded", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("be.calledWith", "instant required");
    cy.get("@consoleInfo").should("be.calledWith", "lazy required");
  });

  it("will always be loaded", () => {
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });
    cy.get("@consoleInfo").should("be.calledWith", "instant required");
    cy.get("@consoleInfo").should("be.calledWith", "lazy required");

    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:unset|preferences:unset|statistics:pending|marketing:unset"
    );

    cy.setCookie("wtm", "necessary:false|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });
    cy.get("@consoleInfo").should("be.calledWith", "instant required");
    cy.get("@consoleInfo").should("be.calledWith", "lazy required");
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:unset|preferences:false|statistics:false|marketing:false"
    );

    cy.setCookie("wtm", "necessary:unset|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });
    cy.get("@consoleInfo").should("be.calledWith", "instant required");
    cy.get("@consoleInfo").should("be.calledWith", "lazy required");
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:unset|preferences:false|statistics:false|marketing:false"
    );
  });

  it("will be loaded instantly and lazy", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.document.head, "appendChild").as("headAppendChild");
      },
    });

    cy.get("@headAppendChild").should("be.calledOnce");
  });
});

describe("Preference tags", () => {
  it("will be loaded", () => {
    cy.setCookie("wtm", "necessary:true|preferences:unset|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("be.calledWith", "instant initial");
    cy.get("@consoleInfo").should("be.calledWith", "lazy initial");
  });

  it("will not be loaded", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("not.be.calledWith", "instant initial");
    cy.get("@consoleInfo").should("not.be.calledWith", "lazy initial");
  });

  it("will be loaded lazy", () => {
    cy.setCookie("wtm", "necessary:true|preferences:unset|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.document.head, "appendChild").as("headAppendChild");
      },
    });

    cy.get("@headAppendChild").should("be.calledThrice");
  });

  it("will be loaded instantly and lazy", () => {
    cy.setCookie("wtm", "necessary:true|preferences:true|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.document.head, "appendChild").as("headAppendChild");
      },
    });

    cy.get("@headAppendChild").should("be.calledTwice");
  });
});

describe("Statistical tags", () => {
  it("will be loaded at the second visit", () => {
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("not.be.calledWith", "instant initial");
    cy.get("@consoleInfo").should("not.be.calledWith", "lazy initial");

    cy.reload();

    cy.get("@consoleInfo").should("be.calledWith", "instant initial");
    cy.get("@consoleInfo").should("be.calledWith", "lazy initial");
  });

  it("will not be loaded at the second visit", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("not.be.calledWith", "instant delayed");
    cy.get("@consoleInfo").should("not.be.calledWith", "lazy delayed");

    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("not.be.calledWith", "instant delayed");
    cy.get("@consoleInfo").should("not.be.calledWith", "lazy delayed");
  });

  it("will be loaded lazy", () => {
    cy.setCookie("wtm", "necessary:true|preferences:unset|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.document.head, "appendChild").as("headAppendChild");
      },
    });

    cy.get("@headAppendChild").should("be.calledThrice");
  });

  it("will be loaded instantly and lazy", () => {
    cy.setCookie("wtm", "necessary:true|preferences:true|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.document.head, "appendChild").as("headAppendChild");
      },
    });

    cy.get("@headAppendChild").should("be.calledTwice");
  });
});

describe("Marketing tags", () => {
  it("can't be unset", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:unset");
    cy.visit("/");
    cy.getCookie("wtm").should(
      "have.property",
      "value",
      "necessary:true|preferences:false|statistics:false|marketing:unset"
    );
  });

  it("will not be loaded", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:false");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("not.be.calledWith", "instant regular");
    cy.get("@consoleInfo").should("not.be.calledWith", "lazy regular");
  });

  it("will be loaded", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:true");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.console, "info").as("consoleInfo");
      },
    });

    cy.get("@consoleInfo").should("be.calledWith", "instant regular");
    cy.get("@consoleInfo").should("be.calledWith", "lazy regular");
  });

  it("will be loaded instantly and lazy", () => {
    cy.setCookie("wtm", "necessary:true|preferences:false|statistics:false|marketing:true");
    cy.visit("/", {
      onBeforeLoad(win) {
        cy.stub(win.document.head, "appendChild").as("headAppendChild");
      },
    });

    cy.get("@headAppendChild").should("be.calledTwice");
  });
});
