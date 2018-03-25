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
/******/ 	return __webpack_require__(__webpack_require__.s = "./frontend/client/wtm.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./frontend/client/wtm.js":
/*!********************************!*\
  !*** ./frontend/client/wtm.js ***!
  \********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/src/js.cookie.js\");\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(js_cookie__WEBPACK_IMPORTED_MODULE_0__);\n\n\nclass TagManager {\n    constructor() {\n        this.client = {\n            functional: true,\n            analytical: false,\n            traceable: false\n        };\n\n        this.initialize = this.initialize.bind(this);\n        this.validate = this.validate.bind(this);\n        this.setAnalytical = this.setAnalytical.bind(this);\n        this.setTraceable = this.setTraceable.bind(this);\n        this.loadData = this.loadData.bind(this);\n        this.handleLoad = this.handleLoad.bind(this);\n\n        this.initialize();\n    }\n\n    initialize() {\n        this.validate();\n        this.loadData(this.client);\n    }\n\n    validate() {\n        let enabled = navigator.cookieEnabled;\n        if (!enabled) {\n            js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.set('wtm_verification');\n            enabled = js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.get('wtm_verification') !== undefined;\n        }\n\n        if (enabled) {\n            if (!this.hasAnalytical() || !this.hasTraceable()) {\n                new CookieBar(this);\n            }\n            this.setAnalytical(true);\n            this.setTraceable(this.isTraceable());\n        }\n    }\n\n    setAnalytical(value) {\n        this.client.analytical = value;\n    }\n\n    hasAnalytical() {\n        if (window.wtm_analytical) {\n            return js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.get('wtm_analytical') !== undefined;\n        }\n        return true;\n    }\n\n    setTraceable(value) {\n        this.client.traceable = value;\n    }\n\n    hasTraceable() {\n        if (window.wtm_traceable) {\n            return js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.get('wtm_traceable') !== undefined;\n        }\n        return true;\n    }\n\n    isTraceable() {\n        if (window.wtm_traceable) {\n            return js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.get('wtm_traceable') === 'true';\n        }\n        return false;\n    }\n\n    loadData(args) {\n        const xhttp = new XMLHttpRequest();\n        xhttp.onreadystatechange = event => {\n            if (event.target.readyState === 4 && event.target.status === 200) {\n                this.data = JSON.parse(event.target.responseText);\n                this.handleLoad();\n            }\n        };\n        xhttp.open(\"POST\", window.wtm_url, true);\n        xhttp.setRequestHeader('Content-Type', 'application/json');\n        xhttp.setRequestHeader('X-CSRFToken', js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.get('csrftoken'));\n        xhttp.send(JSON.stringify(args));\n    }\n\n    handleLoad() {\n        for (let i = 0; i < this.data['tags'].length; i++) {\n            let tag = this.data['tags'][i];\n\n            let element = document.createElement(tag.name);\n            element.appendChild(document.createTextNode(tag.string));\n            document.head.appendChild(element);\n        }\n    }\n}\n\nclass CookieBar {\n    constructor(manager) {\n        this.manager = manager;\n        this.el = document.getElementById('wtm_cookie_bar');\n\n        this.initialize = this.initialize.bind(this);\n        this.showCookieBar = this.showCookieBar.bind(this);\n        this.hideCookieBar = this.hideCookieBar.bind(this);\n        this.handleClick = this.handleClick.bind(this);\n\n        this.initialize();\n    }\n\n    initialize() {\n        let buttons = this.el.querySelectorAll('.js-cookie-choice');\n        for (let button of buttons) {\n            button.addEventListener('click', this.handleClick);\n        }\n\n        this.showCookieBar();\n    }\n\n    showCookieBar() {\n        this.el.style.display = 'flex';\n    }\n\n    hideCookieBar() {\n        this.el.style.display = 'none';\n    }\n\n    handleClick(event) {\n        event.preventDefault();\n\n        const target = event.currentTarget;\n        switch (target.dataset.choice) {\n            case 'accept':\n                this.manager.setTraceable(true);\n                this.manager.loadData({ traceable: true });\n                break;\n            case 'reject':\n                this.manager.setTraceable(false);\n                js_cookie__WEBPACK_IMPORTED_MODULE_0___default.a.set('wtm_traceable', false, { expires: 365 });\n                break;\n        }\n\n        this.hideCookieBar();\n    }\n}\n\ndocument.onreadystatechange = function () {\n    if (document.readyState === \"complete\") {\n        new TagManager();\n    }\n};\n\n//# sourceURL=webpack:///./frontend/client/wtm.js?");

/***/ }),

/***/ "./node_modules/js-cookie/src/js.cookie.js":
/*!*************************************************!*\
  !*** ./node_modules/js-cookie/src/js.cookie.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!\n * JavaScript Cookie v2.2.0\n * https://github.com/js-cookie/js-cookie\n *\n * Copyright 2006, 2015 Klaus Hartl & Fagner Brack\n * Released under the MIT license\n */\n;(function (factory) {\n\tvar registeredInModuleLoader = false;\n\tif (true) {\n\t\t!(__WEBPACK_AMD_DEFINE_FACTORY__ = (factory),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?\n\t\t\t\t(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :\n\t\t\t\t__WEBPACK_AMD_DEFINE_FACTORY__),\n\t\t\t\t__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));\n\t\tregisteredInModuleLoader = true;\n\t}\n\tif (true) {\n\t\tmodule.exports = factory();\n\t\tregisteredInModuleLoader = true;\n\t}\n\tif (!registeredInModuleLoader) {\n\t\tvar OldCookies = window.Cookies;\n\t\tvar api = window.Cookies = factory();\n\t\tapi.noConflict = function () {\n\t\t\twindow.Cookies = OldCookies;\n\t\t\treturn api;\n\t\t};\n\t}\n}(function () {\n\tfunction extend () {\n\t\tvar i = 0;\n\t\tvar result = {};\n\t\tfor (; i < arguments.length; i++) {\n\t\t\tvar attributes = arguments[ i ];\n\t\t\tfor (var key in attributes) {\n\t\t\t\tresult[key] = attributes[key];\n\t\t\t}\n\t\t}\n\t\treturn result;\n\t}\n\n\tfunction init (converter) {\n\t\tfunction api (key, value, attributes) {\n\t\t\tvar result;\n\t\t\tif (typeof document === 'undefined') {\n\t\t\t\treturn;\n\t\t\t}\n\n\t\t\t// Write\n\n\t\t\tif (arguments.length > 1) {\n\t\t\t\tattributes = extend({\n\t\t\t\t\tpath: '/'\n\t\t\t\t}, api.defaults, attributes);\n\n\t\t\t\tif (typeof attributes.expires === 'number') {\n\t\t\t\t\tvar expires = new Date();\n\t\t\t\t\texpires.setMilliseconds(expires.getMilliseconds() + attributes.expires * 864e+5);\n\t\t\t\t\tattributes.expires = expires;\n\t\t\t\t}\n\n\t\t\t\t// We're using \"expires\" because \"max-age\" is not supported by IE\n\t\t\t\tattributes.expires = attributes.expires ? attributes.expires.toUTCString() : '';\n\n\t\t\t\ttry {\n\t\t\t\t\tresult = JSON.stringify(value);\n\t\t\t\t\tif (/^[\\{\\[]/.test(result)) {\n\t\t\t\t\t\tvalue = result;\n\t\t\t\t\t}\n\t\t\t\t} catch (e) {}\n\n\t\t\t\tif (!converter.write) {\n\t\t\t\t\tvalue = encodeURIComponent(String(value))\n\t\t\t\t\t\t.replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent);\n\t\t\t\t} else {\n\t\t\t\t\tvalue = converter.write(value, key);\n\t\t\t\t}\n\n\t\t\t\tkey = encodeURIComponent(String(key));\n\t\t\t\tkey = key.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent);\n\t\t\t\tkey = key.replace(/[\\(\\)]/g, escape);\n\n\t\t\t\tvar stringifiedAttributes = '';\n\n\t\t\t\tfor (var attributeName in attributes) {\n\t\t\t\t\tif (!attributes[attributeName]) {\n\t\t\t\t\t\tcontinue;\n\t\t\t\t\t}\n\t\t\t\t\tstringifiedAttributes += '; ' + attributeName;\n\t\t\t\t\tif (attributes[attributeName] === true) {\n\t\t\t\t\t\tcontinue;\n\t\t\t\t\t}\n\t\t\t\t\tstringifiedAttributes += '=' + attributes[attributeName];\n\t\t\t\t}\n\t\t\t\treturn (document.cookie = key + '=' + value + stringifiedAttributes);\n\t\t\t}\n\n\t\t\t// Read\n\n\t\t\tif (!key) {\n\t\t\t\tresult = {};\n\t\t\t}\n\n\t\t\t// To prevent the for loop in the first place assign an empty array\n\t\t\t// in case there are no cookies at all. Also prevents odd result when\n\t\t\t// calling \"get()\"\n\t\t\tvar cookies = document.cookie ? document.cookie.split('; ') : [];\n\t\t\tvar rdecode = /(%[0-9A-Z]{2})+/g;\n\t\t\tvar i = 0;\n\n\t\t\tfor (; i < cookies.length; i++) {\n\t\t\t\tvar parts = cookies[i].split('=');\n\t\t\t\tvar cookie = parts.slice(1).join('=');\n\n\t\t\t\tif (!this.json && cookie.charAt(0) === '\"') {\n\t\t\t\t\tcookie = cookie.slice(1, -1);\n\t\t\t\t}\n\n\t\t\t\ttry {\n\t\t\t\t\tvar name = parts[0].replace(rdecode, decodeURIComponent);\n\t\t\t\t\tcookie = converter.read ?\n\t\t\t\t\t\tconverter.read(cookie, name) : converter(cookie, name) ||\n\t\t\t\t\t\tcookie.replace(rdecode, decodeURIComponent);\n\n\t\t\t\t\tif (this.json) {\n\t\t\t\t\t\ttry {\n\t\t\t\t\t\t\tcookie = JSON.parse(cookie);\n\t\t\t\t\t\t} catch (e) {}\n\t\t\t\t\t}\n\n\t\t\t\t\tif (key === name) {\n\t\t\t\t\t\tresult = cookie;\n\t\t\t\t\t\tbreak;\n\t\t\t\t\t}\n\n\t\t\t\t\tif (!key) {\n\t\t\t\t\t\tresult[name] = cookie;\n\t\t\t\t\t}\n\t\t\t\t} catch (e) {}\n\t\t\t}\n\n\t\t\treturn result;\n\t\t}\n\n\t\tapi.set = api;\n\t\tapi.get = function (key) {\n\t\t\treturn api.call(api, key);\n\t\t};\n\t\tapi.getJSON = function () {\n\t\t\treturn api.apply({\n\t\t\t\tjson: true\n\t\t\t}, [].slice.call(arguments));\n\t\t};\n\t\tapi.defaults = {};\n\n\t\tapi.remove = function (key, attributes) {\n\t\t\tapi(key, '', extend(attributes, {\n\t\t\t\texpires: -1\n\t\t\t}));\n\t\t};\n\n\t\tapi.withConverter = init;\n\n\t\treturn api;\n\t}\n\n\treturn init(function () {});\n}));\n\n\n//# sourceURL=webpack:///./node_modules/js-cookie/src/js.cookie.js?");

/***/ })

/******/ });