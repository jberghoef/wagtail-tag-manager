class TagFormView {
  loadSelect: HTMLSelectElement;
  locationSelect: HTMLSelectElement;
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
    this.handleLoadChange();
  }

  handleLoadChange() {
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
