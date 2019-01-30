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
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./frontend/client/wtm.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./frontend/client/components/cookie_bar.scss":
/*!****************************************************!*\
  !*** ./frontend/client/components/cookie_bar.scss ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// extracted by mini-css-extract-plugin\n\n//# sourceURL=webpack:///./frontend/client/components/cookie_bar.scss?");

/***/ }),

/***/ "./frontend/client/components/cookie_bar.ts":
/*!**************************************************!*\
  !*** ./frontend/client/components/cookie_bar.ts ***!
  \**************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _cookie_bar_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./cookie_bar.scss */ \"./frontend/client/components/cookie_bar.scss\");\n/* harmony import */ var _cookie_bar_scss__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_cookie_bar_scss__WEBPACK_IMPORTED_MODULE_0__);\n\nvar CookieBar = /** @class */ (function () {\n    function CookieBar(manager) {\n        this.manager = manager;\n        this.el = document.getElementById(\"wtm_cookie_bar\");\n        this.initialize = this.initialize.bind(this);\n        this.showCookieBar = this.showCookieBar.bind(this);\n        this.hideCookieBar = this.hideCookieBar.bind(this);\n        this.handleClick = this.handleClick.bind(this);\n        if (this.el) {\n            this.initialize();\n        }\n    }\n    CookieBar.prototype.initialize = function () {\n        var _this = this;\n        var buttons = this.el.querySelectorAll(\".js-choice\");\n        [].forEach.call(buttons, function (button) {\n            button.addEventListener(\"click\", _this.handleClick, false);\n        });\n        this.showCookieBar();\n    };\n    CookieBar.prototype.showCookieBar = function () {\n        this.el.classList.remove(\"hidden\");\n    };\n    CookieBar.prototype.hideCookieBar = function () {\n        this.el.classList.add(\"hidden\");\n    };\n    CookieBar.prototype.handleClick = function (event) {\n        event.preventDefault();\n        var target = event.currentTarget;\n        switch (target.dataset.choice) {\n            case \"accept\":\n                this.manager.loadData(true);\n                break;\n            case \"reject\":\n                this.manager.loadData(false);\n                break;\n            default:\n                break;\n        }\n        this.hideCookieBar();\n    };\n    return CookieBar;\n}());\n/* harmony default export */ __webpack_exports__[\"default\"] = (CookieBar);\n\n\n//# sourceURL=webpack:///./frontend/client/components/cookie_bar.ts?");

/***/ }),

/***/ "./frontend/client/components/tag_manager.ts":
/*!***************************************************!*\
  !*** ./frontend/client/components/tag_manager.ts ***!
  \***************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/src/js.cookie.js\");\n/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(js_cookie__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _cookie_bar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./cookie_bar */ \"./frontend/client/components/cookie_bar.ts\");\nvar __assign = (undefined && undefined.__assign) || function () {\n    __assign = Object.assign || function(t) {\n        for (var s, i = 1, n = arguments.length; i < n; i++) {\n            s = arguments[i];\n            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))\n                t[p] = s[p];\n        }\n        return t;\n    };\n    return __assign.apply(this, arguments);\n};\n\n\nvar TagManager = /** @class */ (function () {\n    function TagManager() {\n        this.window = window;\n        var body = document.body;\n        this.stateUrl = body.getAttribute(\"data-wtm-state\") || this.window.wtm.state_url;\n        this.lazyUrl = body.getAttribute(\"data-wtm-lazy\") || this.window.wtm.lazy_url;\n        this.showCookiebar = false;\n        this.initialize();\n    }\n    TagManager.prototype.initialize = function () {\n        var _this = this;\n        fetch(this.stateUrl, {\n            method: \"GET\",\n            mode: \"cors\",\n            cache: \"no-cache\",\n            credentials: \"same-origin\",\n            headers: {\n                \"Content-Type\": \"application/json; charset=utf-8\"\n            },\n            redirect: \"follow\",\n            referrer: \"no-referrer\"\n        })\n            .then(function (response) { return response.json(); })\n            .then(function (json) {\n            _this.config = json;\n            _this.validate();\n            _this.loadData();\n        });\n    };\n    TagManager.prototype.validate = function () {\n        var _this = this;\n        // Verify the browser allows cookies.\n        var enabled = navigator.cookieEnabled;\n        if (!enabled) {\n            js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"set\"](\"wtm_verification\", \"verification\");\n            enabled = js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"get\"](\"wtm_verification\") !== undefined;\n        }\n        if (enabled) {\n            Object.keys(this.config).forEach(function (tagType) {\n                if (js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"get\"](\"wtm_\" + tagType) === \"unset\" || !_this.has(tagType)) {\n                    _this.showCookiebar = true;\n                }\n            });\n        }\n        if (this.showCookiebar) {\n            new _cookie_bar__WEBPACK_IMPORTED_MODULE_1__[\"default\"](this);\n        }\n    };\n    TagManager.prototype.has = function (type) {\n        if (type in this.config) {\n            return js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"get\"](\"wtm_\" + type) !== undefined;\n        }\n        return true;\n    };\n    TagManager.prototype.loadData = function (consent) {\n        var _this = this;\n        if (consent === void 0) { consent = undefined; }\n        fetch(this.lazyUrl, {\n            method: \"POST\",\n            mode: \"cors\",\n            cache: \"no-cache\",\n            credentials: \"same-origin\",\n            headers: {\n                \"Content-Type\": \"application/json; charset=utf-8\",\n                \"X-CSRFToken\": js_cookie__WEBPACK_IMPORTED_MODULE_0__[\"get\"](\"csrftoken\")\n            },\n            redirect: \"follow\",\n            referrer: \"no-referrer\",\n            body: JSON.stringify(__assign({ consent: consent }, window.location))\n        })\n            .then(function (response) { return response.json(); })\n            .then(function (json) {\n            _this.data = json;\n            _this.handleLoad();\n        });\n    };\n    TagManager.prototype.handleLoad = function () {\n        this.data.tags.forEach(function (tag) {\n            var element = document.createElement(tag.name);\n            for (var property in tag.attributes) {\n                if (tag.attributes.hasOwnProperty(property)) {\n                    element.setAttribute(property, tag.attributes[property]);\n                }\n            }\n            element.appendChild(document.createTextNode(tag.string));\n            document.head.appendChild(element);\n        });\n    };\n    return TagManager;\n}());\n/* harmony default export */ __webpack_exports__[\"default\"] = (TagManager);\n\n\n//# sourceURL=webpack:///./frontend/client/components/tag_manager.ts?");

/***/ }),

/***/ "./frontend/client/wtm.ts":
/*!********************************!*\
  !*** ./frontend/client/wtm.ts ***!
  \********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _components_tag_manager__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components/tag_manager */ \"./frontend/client/components/tag_manager.ts\");\n\n(function () {\n    new _components_tag_manager__WEBPACK_IMPORTED_MODULE_0__[\"default\"]();\n})();\n\n\n//# sourceURL=webpack:///./frontend/client/wtm.ts?");

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