describe("Trigger management", () => {
  it("can close the help block", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");
    cy.get("#wtm_help_block a").click();
    cy.get("#wtm_help_block").should("not.be.visible");
  });

  it("can create a new trigger", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("a").contains("Add trigger").click();

    cy.get("#id_name").type("A new trigger");
    cy.get("#id_description").type("Lorem ipsum");
    cy.get("[value='9']").scrollIntoView().click({ force: true });
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("A new trigger");
  });

  it("can update a trigger", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_name").type("{selectall}{del}An updated trigger");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("An updated trigger");
  });

  it("can update a trigger to 'history change'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("history_change");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'javascript error'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("javascript_error");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'click all elements'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("click_all_elements");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'click some elements'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("click_some_elements+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}input");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'visibility once per page'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("visibility_once_per_page+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}input");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'visibility once per element'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("visibility_once_per_element+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}input");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'visibility recurring'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("visibility_recurring+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}input");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'scroll vertical'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("scroll_vertical+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}5");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'scroll horizontal'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("scroll_horizontal+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}5");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'timer timeout'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("timer_timeout+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}100");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can update a trigger to 'timer interval'", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");

    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_trigger_type").scrollIntoView().select("timer_interval+");
    cy.get("#id_value").scrollIntoView().type("{selectall}{del}100");
    cy.get(".actions button[type='submit']").click();
    cy.get(".messages .success").contains("Trigger 'An updated trigger' updated.");
  });

  it("can delete a trigger", () => {
    cy.visit("/cms/wagtail_tag_manager/trigger/");
    cy.get("[data-object-pk]").first().find("a").contains("Delete").click({ force: true });
    cy.get("input[type='submit']").click();
    cy.get(".messages .success").contains("trigger 'An updated trigger' deleted.");
  });
});
