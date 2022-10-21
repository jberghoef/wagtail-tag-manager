/******/ (function() { // webpackBootstrap
var __webpack_exports__ = {};
/*!*********************************************!*\
  !*** ./frontend/admin/trigger_form_view.ts ***!
  \*********************************************/
var TriggerFormView = /** @class */ (function () {
    function TriggerFormView() {
        this.triggerSelect = document.getElementById("id_trigger_type");
        this.valueInput = document.getElementById("id_value");
        this.initialize = this.initialize.bind(this);
        this.handleTriggerChange = this.handleTriggerChange.bind(this);
        this.triggerSelect.addEventListener("change", this.handleTriggerChange);
        this.initialize();
    }
    TriggerFormView.prototype.initialize = function () {
        this.handleTriggerChange();
    };
    TriggerFormView.prototype.handleTriggerChange = function (event) {
        if (event === void 0) { event = null; }
        var value = this.triggerSelect.options[this.triggerSelect.selectedIndex].value;
        if (value.slice(-1) !== "+") {
            this.valueInput.disabled = true;
            this.valueInput.value = "";
        }
        else {
            this.valueInput.disabled = false;
        }
    };
    return TriggerFormView;
}());
document.addEventListener("DOMContentLoaded", function (event) {
    new TriggerFormView();
});

/******/ })()
;
//# sourceMappingURL=sourcemaps/trigger_form_view.bundle.js.map