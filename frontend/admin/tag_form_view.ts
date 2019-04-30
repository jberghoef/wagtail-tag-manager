import "./tag_form_view.scss";

import * as CodeMirror from "codemirror";
import "codemirror/mode/django/django";
import "codemirror/addon/display/panel";

interface VariableGroup {
  verbose_name: string;
  items: [VariableItem];
}

interface VariableItem {
  name: string;
  description: string;
  key: string;
}

interface Editor extends CodeMirror.EditorFromTextArea {
  doc: CodeMirror.Doc;
  addPanel(el: HTMLElement, options: object): void;
}

const { document } = window;

class TagFormView {
  loadSelect: HTMLSelectElement;
  locationSelect: HTMLSelectElement;
  textArea: HTMLTextAreaElement;
  editor: Editor;
  hiddenInput: HTMLInputElement;

  constructor() {
    this.loadSelect = document.getElementById("id_tag_loading") as HTMLSelectElement;
    this.locationSelect = document.getElementById("id_tag_location") as HTMLSelectElement;

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
    this.editor = CodeMirror.fromTextArea(this.textArea, { mode: "django" }) as Editor;

    fetch("/wtm/variables/")
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.addPanel(data);
      });
  }

  addPanel(data: Array<VariableGroup>) {
    const panelEl = document.createElement("ul");
    panelEl.classList.add("panel");

    for (const group of data) {
      const groupEl = document.createElement("ul");
      groupEl.classList.add("listing");

      const h3 = document.createElement("h3");
      h3.appendChild(document.createTextNode(group.verbose_name));
      panelEl.appendChild(h3);

      for (let item of group.items) {
        const a = document.createElement("a");
        a.appendChild(document.createTextNode(item.name));
        a.href = "#";
        a.title = item.description;
        a.dataset.key = item.key;

        a.addEventListener("click", event => {
          event.preventDefault();
          const target = event.currentTarget as HTMLElement;
          this.editor.doc.replaceSelection(`{{ ${target.dataset.key} }}`, "end");
          this.editor.focus();
        });

        const li = document.createElement("li");
        li.appendChild(a);

        groupEl.appendChild(li);
      }

      panelEl.appendChild(groupEl);
    }

    this.editor.addPanel(panelEl, { position: "top" });
  }

  handleLoadChange(event: Event = null) {
    const value = this.loadSelect.options[this.loadSelect.selectedIndex].value;

    if (value !== "instant_load") {
      this.locationSelect.disabled = true;
      [].forEach.call(this.locationSelect, (option: HTMLOptionElement) => {
        if (option.value === "0_top_head") {
          option.selected = true;
        }
      });

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

document.addEventListener("DOMContentLoaded", () => {
  new TagFormView();
});
