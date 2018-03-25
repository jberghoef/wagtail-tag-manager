/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./frontend/admin/tag_form_view.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./frontend/admin/tag_form_view.js":
/*!*****************************************!*\
  !*** ./frontend/admin/tag_form_view.js ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("class FormView {\n    constructor() {\n        this.loadSelect = document.getElementById('id_tag_loading');\n        this.locationSelect = document.getElementById('id_tag_location');\n\n        this.initialize = this.initialize.bind(this);\n        this.handleLoadChange = this.handleLoadChange.bind(this);\n\n        this.loadSelect.addEventListener('change', this.handleLoadChange);\n\n        this.initialize();\n    }\n\n    initialize() {\n        this.handleLoadChange();\n    }\n\n    handleLoadChange(event) {\n        const value = this.loadSelect.options[this.loadSelect.selectedIndex].value;\n\n        if (value == 'lazy_load') {\n            this.locationSelect.disabled = true;\n            for (let option of this.locationSelect) {\n                if (option.value == 'top_head') {\n                    option.selected = true;\n                }\n            }\n\n            this.hiddenInput = document.createElement('input');\n            this.hiddenInput.id = this.locationSelect.id;\n            this.hiddenInput.name = this.locationSelect.name;\n            this.hiddenInput.type = 'hidden';\n            this.hiddenInput.value = 'top_head';\n            this.locationSelect.parentNode.insertBefore(this.hiddenInput, this.locationSelect.parentNode.childNodes[0]);\n        } else {\n            this.locationSelect.disabled = false;\n            this.hiddenInput.remove();\n        }\n    }\n}\n\ndocument.onreadystatechange = function () {\n    if (document.readyState === \"complete\") {\n        new FormView();\n    }\n};\n\n//# sourceURL=webpack:///./frontend/admin/tag_form_view.js?");

/***/ })

/******/ });