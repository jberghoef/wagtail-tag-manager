class TriggerFormView {
  triggerSelect: HTMLSelectElement;
  valueInput: HTMLInputElement;

  constructor() {
    this.triggerSelect = document.getElementById("id_trigger_type") as HTMLSelectElement;
    this.valueInput = document.getElementById("id_value") as HTMLInputElement;

    this.initialize = this.initialize.bind(this);
    this.handleTriggerChange = this.handleTriggerChange.bind(this);

    this.triggerSelect.addEventListener("change", this.handleTriggerChange);

    this.initialize();
  }

  initialize() {
    this.handleTriggerChange();
  }

  handleTriggerChange(event: Event = null) {
    const value = this.triggerSelect.options[this.triggerSelect.selectedIndex].value;

    if (value.slice(-1) !== "+") {
      this.valueInput.disabled = true;
      this.valueInput.value = "";
    } else {
      this.valueInput.disabled = false;
    }
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  new TriggerFormView();
});
