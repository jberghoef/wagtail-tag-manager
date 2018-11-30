// TODO: Turn this into something reusable.

class CookieDeclarationFormView {
  durationPeriodSelect: HTMLSelectElement;
  durationValueInput: HTMLInputElement;

  constructor() {
    this.durationPeriodSelect = document.getElementById("id_duration_period") as HTMLSelectElement;
    this.durationValueInput = document.getElementById("id_duration_value") as HTMLInputElement;

    this.initialize = this.initialize.bind(this);
    this.handleDurationPeriodChange = this.handleDurationPeriodChange.bind(this);

    this.durationPeriodSelect.addEventListener("change", this.handleDurationPeriodChange);

    this.initialize();
  }

  initialize() {
    this.handleDurationPeriodChange();
  }

  handleDurationPeriodChange(event: Event = null) {
    const value = this.durationPeriodSelect.options[this.durationPeriodSelect.selectedIndex].value;

    if (value.slice(-1) !== "+") {
      this.durationValueInput.disabled = true;
      this.durationValueInput.value = "";
    } else {
      this.durationValueInput.disabled = false;
    }
  }
}

window.onload = () => new CookieDeclarationFormView();
