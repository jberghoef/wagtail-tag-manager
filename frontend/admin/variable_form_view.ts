// TODO: Turn this into something reusable.

class VariableFormView {
  variableSelect: HTMLSelectElement;
  valueInput: HTMLInputElement;

  constructor() {
    this.variableSelect = document.getElementById("id_variable_type") as HTMLSelectElement;
    this.valueInput = document.getElementById("id_value") as HTMLInputElement;

    this.initialize = this.initialize.bind(this);
    this.handleVariableChange = this.handleVariableChange.bind(this);

    this.variableSelect.addEventListener("change", this.handleVariableChange);

    this.initialize();
  }

  initialize() {
    this.handleVariableChange();
  }

  handleVariableChange(event: Event = null) {
    const value = this.variableSelect.options[this.variableSelect.selectedIndex].value;

    if (value.slice(-1) !== "+") {
      this.valueInput.disabled = true;
      this.valueInput.value = "";
    } else {
      this.valueInput.disabled = false;
    }
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  new VariableFormView();
});
