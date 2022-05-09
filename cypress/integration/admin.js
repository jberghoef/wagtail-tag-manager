describe("The admin dashboard", () => {
  it("shows the summary panels", () => {
    cy.visit("/cms/");

    cy.get(".icon-code").contains("Tags");
    cy.get(".icon-snippet").contains("Constants");
    cy.get(".icon-snippet").contains("Variables");
    cy.get(".icon-media").contains("Triggers");
    cy.get(".icon-help").contains("Cookie declarations");
    cy.get(".icon-success").contains("Cookie consents");
  });
});

describe("The cookie bar settings", () => {
  it("allows changeing of the title", () => {
    cy.visit("/cms/settings/wagtail_tag_manager/cookiebarsettings/1/");

    cy.get("#id_title").type("{selectall}{del}We use cookies");
    cy.get(".actions button[type='submit']").click();

    cy.visit("/");
    cy.get("#wtm_cookie_bar h4").contains("We use cookies");
  });

  it("allows resetting the title", () => {
    cy.visit("/cms/settings/wagtail_tag_manager/cookiebarsettings/1/");

    cy.get("#id_title").type("{selectall}{del}");
    cy.get(".actions button[type='submit']").click();

    cy.visit("/");
    cy.get("#wtm_cookie_bar h4").contains("This website uses cookies");
  });
});

describe("Tag management", () => {
  it("can close the help block", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/");
    cy.get("#wtm_help_block a").click();
    cy.get("#wtm_help_block").should("not.be.visible");
  });

  it("can create a new tag", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/");

    cy.get("a").contains("Add tag").click();

    cy.get("#id_name").type("A new tag");
    cy.get("#id_description").type("Lorem ipsum");
    cy.get(".CodeMirror").click().type("console.info('test')");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("A new tag");
  });

  it("can update a tag", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/");
    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_name").type("{selectall}{del}An updated tag");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("An updated tag");
  });

  it("can't select the location when loaded lazily", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/");
    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_tag_loading").select("lazy_load", { force: true });
    cy.get("input#id_tag_location").should("have.value", "0_top_head");
    cy.get("select#id_tag_location").should("be.disabled");
  });

  it("can delete a tag", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/");
    cy.get("[data-object-pk]").first().find("a").contains("Delete").click({ force: true });
    cy.get("input[type='submit']").click();
    cy.get(".messages .success").contains("tag 'An updated tag' deleted.");
  });
});

describe("Constants management", () => {
  it("can close the help block", () => {
    cy.visit("/cms/wagtail_tag_manager/constant/");
    cy.get("#wtm_help_block a").click();
    cy.get("#wtm_help_block").should("not.be.visible");
  });

  it("can create a new constant", () => {
    cy.visit("/cms/wagtail_tag_manager/constant/");

    cy.get("a").contains("Add constant").click();

    cy.get("#id_name").type("A new constant");
    cy.get("#id_description").type("Lorem ipsum");
    cy.get("#id_key").type("test");
    cy.get("#id_value").type("Some cool test");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("A new constant");
  });

  it("can use the constant", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/create/");
    cy.get("[data-key='test']").scrollIntoView().contains("A new constant");
  });

  it("can update a constant", () => {
    cy.visit("/cms/wagtail_tag_manager/constant/");
    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_name").type("{selectall}{del}An updated constant");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("An updated constant");
  });

  it("can delete a constant", () => {
    cy.visit("/cms/wagtail_tag_manager/constant/");
    cy.get("[data-object-pk]").first().find("a").contains("Delete").click({ force: true });
    cy.get("input[type='submit']").click();
    cy.get(".messages .success").contains("constant 'An updated constant' deleted.");
  });
});

describe("Variable management", () => {
  it("can close the help block", () => {
    cy.visit("/cms/wagtail_tag_manager/variable/");
    cy.get("#wtm_help_block a").click();
    cy.get("#wtm_help_block").should("not.be.visible");
  });

  it("can create a new variable", () => {
    cy.visit("/cms/wagtail_tag_manager/variable/");

    cy.get("a").contains("Add variable").click();

    cy.get("#id_name").type("A new variable");
    cy.get("#id_description").type("Lorem ipsum");
    cy.get("#id_key").type("test");
    cy.get("#id_variable_type").select("_repath+", { force: true });
    cy.get("#id_value").type("/wtm/is/cool/");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("A new variable");
  });

  it("can use the variable", () => {
    cy.visit("/cms/wagtail_tag_manager/tag/create/");
    cy.get("[data-key='test']").scrollIntoView().contains("A new variable");
  });

  it("can update a variable", () => {
    cy.visit("/cms/wagtail_tag_manager/variable/");
    cy.get("[data-object-pk]").first().find("a").contains("Edit").click({ force: true });
    cy.get("#id_name").type("{selectall}{del}An updated variable");
    cy.get("#id_variable_type").select("_cookie+", { force: true });
    cy.get("#id_value").type("{selectall}{del}wtm_id");
    cy.get(".actions button[type='submit']").click();
    cy.get(".field-name_display").first().contains("An updated variable");
  });

  it("can delete a variable", () => {
    cy.visit("/cms/wagtail_tag_manager/variable/");
    cy.get("[data-object-pk]").first().find("a").contains("Delete").click({ force: true });
    cy.get("input[type='submit']").click();
    cy.get(".messages .success").contains("variable 'An updated variable' deleted.");
  });
});

describe("Cookie consent", () => {
  it("will be registered", () => {
    cy.visit("/");

    cy.get("#wtm_cookie_bar").should("be.visible");
    cy.get("#wtm_cookie_bar input#id_marketing").click();
    cy.get("#wtm_cookie_bar input[type='submit']").click();

    cy.visit("/cms/wagtail_tag_manager/cookieconsent/");
    cy.get("[data-object-pk]").first().find("a").contains("Delete").click({ force: true });
    cy.get("input[type='submit']").click();
    cy.get(".messages .success").should("exist");
  });
});
