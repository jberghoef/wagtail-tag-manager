import "./tag_form_view.scss";

import CodeMirror from "codemirror";
import "codemirror/mode/django/django";
import "codemirror/addon/display/panel";

const { document } = window;

class TagFormView {
  constructor() {
    this.loadSelect = document.getElementById("id_tag_loading");
    this.locationSelect = document.getElementById("id_tag_location");

    this.initialize = this.initialize.bind(this);
    this.handleLoadChange = this.handleLoadChange.bind(this);

    this.loadSelect.addEventListener("change", this.handleLoadChange);

    this.initialize();
  }

  initialize() {
    this.injectEditor();
    this.handleLoadChange();
  }

  injectEditor() {
    this.textArea = document.querySelector(".code .input textarea");
    this.editor = CodeMirror.fromTextArea(this.textArea, { mode: "django" });

    // Create constant panel
    const constantPanel = document.createElement("div");
    constantPanel.appendChild(document.createTextNode("Constants!"));
    this.editor.addPanel(constantPanel, { position: "before-bottom", stable: true });

    // Create variable panel
    const variablePanel = document.createElement("div");
    variablePanel.appendChild(document.createTextNode("Variables!"));
    this.editor.addPanel(variablePanel, { position: "before-bottom", stable: true });
  }

  handleLoadChange(event) {
    const value = this.loadSelect.options[this.loadSelect.selectedIndex].value;

    if (value !== "instant_load") {
      this.locationSelect.disabled = true;
      for (let option of this.locationSelect) {
        if (option.value === "top_head") {
          option.selected = true;
        }
      }

      this.hiddenInput = document.createElement("input");
      this.hiddenInput.id = this.locationSelect.id;
      this.hiddenInput.name = this.locationSelect.name;
      this.hiddenInput.type = "hidden";
      this.hiddenInput.value = "top_head";
      this.locationSelect.parentNode.insertBefore(
        this.hiddenInput,
        this.locationSelect.parentNode.childNodes[0]
      );
    } else {
      this.locationSelect.disabled = false;
      this.hiddenInput.remove();
    }
  }
}

document.onreadystatechange = function() {
  if (document.readyState === "complete") {
    new TagFormView();
  }
};
