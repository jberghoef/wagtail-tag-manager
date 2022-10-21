/******/ (function() { // webpackBootstrap
var __webpack_exports__ = {};
/*!**********************************************!*\
  !*** ./frontend/admin/variable_form_view.ts ***!
  \**********************************************/
// TODO: Turn this into something reusable.
var VariableFormView = /** @class */ (function () {
    function VariableFormView() {
        this.variableSelect = document.getElementById("id_variable_type");
        this.valueInput = document.getElementById("id_value");
        this.initialize = this.initialize.bind(this);
        this.handleVariableChange = this.handleVariableChange.bind(this);
        this.variableSelect.addEventListener("change", this.handleVariableChange);
        this.initialize();
    }
    VariableFormView.prototype.initialize = function () {
        this.handleVariableChange();
    };
    VariableFormView.prototype.handleVariableChange = function (event) {
        if (event === void 0) { event = null; }
        var value = this.variableSelect.options[this.variableSelect.selectedIndex].value;
        if (value.slice(-1) !== "+") {
            this.valueInput.disabled = true;
            this.valueInput.value = "";
        }
        else {
            this.valueInput.disabled = false;
        }
    };
    return VariableFormView;
}());
document.addEventListener("DOMContentLoaded", function (event) {
    new VariableFormView();
});

/******/ })()
;
//# sourceMappingURL=sourcemaps/variable_form_view.bundle.js.map