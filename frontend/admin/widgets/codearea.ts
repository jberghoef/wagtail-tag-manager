import "./codearea.scss";

import * as CodeMirror from "codemirror";
import "codemirror/mode/django/django";
import "codemirror/addon/display/panel";

declare global {
  interface Window {
    wtm: any;
  }
}

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
  addPanel(el: HTMLElement, options: object): HTMLElement;
}

class Codearea {
  el: HTMLTextAreaElement;
  editor: Editor;

  constructor(el: HTMLTextAreaElement) {
    this.el = el;

    this.initialize();
  }

  initialize() {
    this.editor = CodeMirror.fromTextArea(this.el, { mode: "django" }) as Editor;

    fetch("/wtm/variables/")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
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

        a.addEventListener("click", (event) => {
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
}

window.wtm = window.wtm || {};
window.wtm.initCodearea = (selector: string, currentScript: HTMLScriptElement) => {
  const context = currentScript ? currentScript.parentNode : document.body;
  const field = context.querySelector(selector) || document.body.querySelector(selector);
  new Codearea(field as HTMLTextAreaElement);
};
