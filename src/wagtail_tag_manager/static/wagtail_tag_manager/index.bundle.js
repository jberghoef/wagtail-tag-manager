/******/ (function() { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./frontend/admin/index.scss":
/*!***********************************!*\
  !*** ./frontend/admin/index.scss ***!
  \***********************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	!function() {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = function(exports) {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	}();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
!function() {
/*!*********************************!*\
  !*** ./frontend/admin/index.ts ***!
  \*********************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _index_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index.scss */ "./frontend/admin/index.scss");

var IndexView = /** @class */ (function () {
    function IndexView() {
        this.el = document.getElementById("wtm_help_block");
        this.close_el = this.el.querySelector("a.close-link");
        this.showHelpBlock = this.showHelpBlock.bind(this);
        this.hideHelpBlock = this.hideHelpBlock.bind(this);
        this.initialize = this.initialize.bind(this);
        this.close_el.addEventListener("click", this.hideHelpBlock);
        if (this.el) {
            this.initialize();
        }
    }
    IndexView.prototype.initialize = function () {
        if (localStorage.getItem(this.identifier) === null) {
            this.showHelpBlock();
        }
    };
    IndexView.prototype.showHelpBlock = function () {
        this.el.style.display = "block";
    };
    IndexView.prototype.hideHelpBlock = function () {
        localStorage.setItem(this.identifier, "hidden");
        this.el.style.display = "none";
    };
    Object.defineProperty(IndexView.prototype, "identifier", {
        get: function () {
            return "wtm_help_block:" + location.pathname;
        },
        enumerable: false,
        configurable: true
    });
    return IndexView;
}());
document.addEventListener("DOMContentLoaded", function () {
    new IndexView();
});

}();
/******/ })()
;
//# sourceMappingURL=sourcemaps/index.bundle.js.map