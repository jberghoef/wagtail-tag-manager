class TagFormView {
    constructor() {
        this.loadSelect = document.getElementById('id_tag_loading');
        this.locationSelect = document.getElementById('id_tag_location');

        this.initialize = this.initialize.bind(this)
        this.handleLoadChange = this.handleLoadChange.bind(this);

        this.loadSelect.addEventListener('change', this.handleLoadChange);

        this.initialize()
    }

    initialize() {
        this.handleLoadChange()
    }

    handleLoadChange(event) {
        const value = this.loadSelect.options[this.loadSelect.selectedIndex].value;

        if (value === 'lazy_load') {
            this.locationSelect.disabled = true;
            for (let option of this.locationSelect) {
                if (option.value === 'top_head') {
                    option.selected = true;
                }
            }

            this.hiddenInput = document.createElement('input');
            this.hiddenInput.id = this.locationSelect.id;
            this.hiddenInput.name = this.locationSelect.name;
            this.hiddenInput.type = 'hidden';
            this.hiddenInput.value = 'top_head';
            this.locationSelect.parentNode.insertBefore(this.hiddenInput, this.locationSelect.parentNode.childNodes[0])
        } else {
            this.locationSelect.disabled = false;
            this.hiddenInput.remove();
        }
    }
}

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        new TagFormView()
    }
 }
