describe("The home page", () => {
	beforeEach("login to admin", () => {
	  cy.visit("/cms/");
	  cy.get("#id_username").type("superuser");
	  cy.get("#id_password").type("testing");
	  cy.get("button[type='submit']").click();
	});
	
  it("can enable page tags", () => {
		cy.visit("/cms/pages/2/edit/");
		cy.get("a[href='#tab-settings']").click();
		
		cy.get("[for='id_wtm_tags_8']").click();
		cy.get("[for='id_wtm_tags_9']").click();
		cy.get("[for='id_wtm_tags_10']").click();
		cy.get("[for='id_wtm_tags_11']").click();
		
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
		cy.visit("/cms/pages/2/edit/");
		cy.get("a[href='#tab-settings']").click();
		
		cy.get("[for='id_wtm_tags_8']").click();
		cy.get("[for='id_wtm_tags_9']").click();
		cy.get("[for='id_wtm_tags_10']").click();
		cy.get("[for='id_wtm_tags_11']").click();
		
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
