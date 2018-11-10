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

    fetch("/wtm/variables/")
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.variables = data.constants.concat(data.variables);
        this.addVariablePanel(this.variables);
      });
  }

  addVariablePanel(items) {
    const panel = document.createElement("div");
    panel.classList.add("panel");

    for (let item of items) {
      const button = document.createElement("button");
      button.classList.add("button", "button-small", "bicolor", "icon", "icon-plus");

      button.appendChild(document.createTextNode(item.name));
      button.type = "button";
      button.title = item.description;
      button.dataset.key = item.key;

      button.addEventListener("click", event => {
        event.preventDefault();
        const target = event.currentTarget;
        this.editor.doc.replaceSelection(`{{ ${target.dataset.key} }}`, "end");
        this.editor.focus();
      });

      panel.appendChild(button);
    }

    this.editor.addPanel(panel, { position: "top", stable: true });
  }

  handleLoadChange(event) {
    const value = this.loadSelect.options[this.loadSelect.selectedIndex].value;

    if (value !== "instant_load") {
      this.locationSelect.disabled = true;
      for (let option of this.locationSelect) {
        if (option.value === "0_top_head") {
          option.selected = true;
        }
      }

      this.hiddenInput = document.createElement("input");
      this.hiddenInput.id = this.locationSelect.id;
      this.hiddenInput.name = this.locationSelect.name;
      this.hiddenInput.type = "hidden";
      this.hiddenInput.value = "0_top_head";
      this.locationSelect.parentNode.insertBefore(
        this.hiddenInput,
        this.locationSelect.parentNode.childNodes[0]
      );
    } else {
      this.locationSelect.disabled = false;
      if (this.hiddenInput) {
        this.hiddenInput.remove();
      }
    }
  }
}

document.onreadystatechange = function() {
  if (document.readyState === "complete") {
    new TagFormView();
  }
};
