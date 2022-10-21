/******/ (function() { // webpackBootstrap
var __webpack_exports__ = {};
/*!*****************************************!*\
  !*** ./frontend/admin/tag_form_view.ts ***!
  \*****************************************/
var TagFormView = /** @class */ (function () {
    function TagFormView() {
        this.loadSelect = document.getElementById("id_tag_loading");
        this.locationSelect = document.getElementById("id_tag_location");
        this.initialize = this.initialize.bind(this);
        this.handleLoadChange = this.handleLoadChange.bind(this);
        this.loadSelect.addEventListener("change", this.handleLoadChange);
        this.initialize();
    }
    TagFormView.prototype.initialize = function () {
        this.handleLoadChange();
    };
    TagFormView.prototype.handleLoadChange = function () {
        var value = this.loadSelect.options[this.loadSelect.selectedIndex].value;
        if (value !== "instant_load") {
            this.locationSelect.disabled = true;
            [].forEach.call(this.locationSelect, function (option) {
                if (option.value === "0_top_head") {
                    option.selected = true;
                }
            });
            this.hiddenInput = document.createElement("input");
            this.hiddenInput.id = this.locationSelect.id;
            this.hiddenInput.name = this.locationSelect.name;
            this.hiddenInput.type = "hidden";
            this.hiddenInput.value = "0_top_head";
            this.locationSelect.parentNode.insertBefore(this.hiddenInput, this.locationSelect.parentNode.childNodes[0]);
        }
        else {
            this.locationSelect.disabled = false;
            if (this.hiddenInput) {
                this.hiddenInput.remove();
            }
        }
    };
    return TagFormView;
}());
document.addEventListener("DOMContentLoaded", function () {
    new TagFormView();
});

/******/ })()
;
//# sourceMappingURL=sourcemaps/tag_form_view.bundle.js.map