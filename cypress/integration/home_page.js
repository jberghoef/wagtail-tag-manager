beforeEach("clear wtm cookies", () => {
  cy.clearCookie("wtm");
  cy.clearCookie("wtm_id");
});

describe("The home page", () => {
  it("can enable page tags", () => {
		cy.on('uncaught:exception', (err, runnable) => {
			return false
		})

		cy.visit("/cms/pages/2/edit/");
		cy.get("a[href='#tab-settings']").click();

		cy.contains("Lazy passive required").click();
		cy.contains("Lazy passive initial").click();
		cy.contains("Lazy passive delayed").click();
		cy.contains("Lazy passive regular").click();

		cy.get(".dropdown-toggle").click();
		cy.get("[name='action-publish']").click();

		cy.setCookie("wtm", "necessary:true|preferences:true|statistics:true|marketing:true");
		cy.visit("/", {
			onBeforeLoad(win) {
				cy.stub(win.console, "info").as("consoleInfo");
			},
		});

		cy.get("@consoleInfo").should("be.calledWith", "lazy passive required");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive initial");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive delayed");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive regular");
  });

	it("will honor consent", () => {
		cy.setCookie("wtm", "necessary:true|preferences:unset|statistics:unset|marketing:false");
		cy.visit("/", {
			onBeforeLoad(win) {
				cy.stub(win.console, "info").as("consoleInfo");
			},
		});

		cy.get("@consoleInfo").should("be.calledWith", "lazy passive required");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive initial");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive delayed");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive regular");

		cy.setCookie("wtm", "necessary:false|preferences:false|statistics:delayed|marketing:false");
		cy.visit("/", {
			onBeforeLoad(win) {
				cy.stub(win.console, "info").as("consoleInfo");
			},
		});

		cy.get("@consoleInfo").should("be.calledWith", "lazy passive required");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive initial");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive delayed");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive regular");

		cy.setCookie("wtm", "necessary:true|preferences:true|statistics:true|marketing:true");
		cy.visit("/", {
			onBeforeLoad(win) {
				cy.stub(win.console, "info").as("consoleInfo");
			},
		});

		cy.get("@consoleInfo").should("be.calledWith", "lazy passive required");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive initial");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive delayed");
		cy.get("@consoleInfo").should("be.calledWith", "lazy passive regular");
	});

	it("can disable page tags", () => {
		cy.on('uncaught:exception', (err, runnable) => {
			return false
		})

		cy.visit("/cms/pages/2/edit/");
		cy.get("a[href='#tab-settings']").click();

		cy.contains("Lazy passive required").click();
		cy.contains("Lazy passive initial").click();
		cy.contains("Lazy passive delayed").click();
		cy.contains("Lazy passive regular").click();

		cy.get(".dropdown-toggle").click();
		cy.get("[name='action-publish']").click();

		cy.setCookie("wtm", "necessary:true|preferences:true|statistics:true|marketing:true");
		cy.visit("/", {
			onBeforeLoad(win) {
				cy.stub(win.console, "info").as("consoleInfo");
			},
		});

		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive required");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive initial");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive delayed");
		cy.get("@consoleInfo").should("not.be.calledWith", "lazy passive regular");
	});
});
