class VariableFormView {
    constructor() {
        this.variableSelect = document.getElementById('id_variable_type');
        this.valueInput = document.getElementById('id_value');

        this.initialize = this.initialize.bind(this)
        this.handleVariableChange = this.handleVariableChange.bind(this);

        this.variableSelect.addEventListener('change', this.handleVariableChange);

        this.initialize()
    }

    initialize() {
        this.handleVariableChange()
    }

    handleVariableChange(event) {
        const value = this.variableSelect.options[this.variableSelect.selectedIndex].value;

        if (value.slice(-1) !== '+') {
            this.valueInput.disabled = true;
            this.valueInput.value = '';
        } else {
            this.valueInput.disabled = false;
        }
    }
}

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        new VariableFormView()
    }
 }
