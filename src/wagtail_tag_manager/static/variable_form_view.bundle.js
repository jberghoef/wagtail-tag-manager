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
/******/ 	return __webpack_require__(__webpack_require__.s = "./frontend/admin/variable_form_view.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./frontend/admin/variable_form_view.js":
/*!**********************************************!*\
  !*** ./frontend/admin/variable_form_view.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("class VariableFormView {\n    constructor() {\n        this.variableSelect = document.getElementById('id_variable_type');\n        this.valueInput = document.getElementById('id_value');\n\n        this.initialize = this.initialize.bind(this);\n        this.handleVariableChange = this.handleVariableChange.bind(this);\n\n        this.variableSelect.addEventListener('change', this.handleVariableChange);\n\n        this.initialize();\n    }\n\n    initialize() {\n        this.handleVariableChange();\n    }\n\n    handleVariableChange(event) {\n        const value = this.variableSelect.options[this.variableSelect.selectedIndex].value;\n\n        if (value.slice(-1) !== '+') {\n            this.valueInput.disabled = true;\n            this.valueInput.value = '';\n        } else {\n            this.valueInput.disabled = false;\n        }\n    }\n}\n\ndocument.onreadystatechange = function () {\n    if (document.readyState === \"complete\") {\n        new VariableFormView();\n    }\n};\n\n//# sourceURL=webpack:///./frontend/admin/variable_form_view.js?");

/***/ })

/******/ });