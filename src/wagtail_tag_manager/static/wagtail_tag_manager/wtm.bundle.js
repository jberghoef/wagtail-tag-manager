/******/ (function() { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./frontend/client/components/cookie_bar.scss":
/*!****************************************************!*\
  !*** ./frontend/client/components/cookie_bar.scss ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ "./frontend/client/components/cookie_bar.ts":
/*!**************************************************!*\
  !*** ./frontend/client/components/cookie_bar.ts ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _cookie_bar_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./cookie_bar.scss */ "./frontend/client/components/cookie_bar.scss");

var CookieBar = /** @class */ (function () {
    function CookieBar(manager) {
        this.manager = manager;
        this.el = document.getElementById("wtm_cookie_bar");
        this.initialize = this.initialize.bind(this);
        this.showCookieBar = this.showCookieBar.bind(this);
        this.hideCookieBar = this.hideCookieBar.bind(this);
        if (this.el) {
            this.initialize();
        }
    }
    CookieBar.prototype.initialize = function () {
        this.showCookieBar();
    };
    CookieBar.prototype.showCookieBar = function () {
        this.el.classList.remove("hidden");
    };
    CookieBar.prototype.hideCookieBar = function () {
        this.el.classList.add("hidden");
    };
    return CookieBar;
}());
/* harmony default export */ __webpack_exports__["default"] = (CookieBar);


/***/ }),

/***/ "./frontend/client/components/tag_manager.ts":
/*!***************************************************!*\
  !*** ./frontend/client/components/tag_manager.ts ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var js_cookie__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! js-cookie */ "./node_modules/js-cookie/dist/js.cookie.mjs");
/* harmony import */ var whatwg_fetch__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! whatwg-fetch */ "./node_modules/whatwg-fetch/fetch.js");
/* harmony import */ var _cookie_bar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./cookie_bar */ "./frontend/client/components/cookie_bar.ts");
/* harmony import */ var _trigger_monitor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./trigger_monitor */ "./frontend/client/components/trigger_monitor.ts");
var __assign = (undefined && undefined.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};




var TagManager = /** @class */ (function () {
    function TagManager() {
        this.window = window;
        this.data = {};
        this.config = {};
        this.state = {};
        var body = document.body;
        this.configUrl = body.getAttribute("data-wtm-config") || this.window.wtm.config_url;
        this.lazyUrl = body.getAttribute("data-wtm-lazy") || this.window.wtm.lazy_url;
        this.requestInit = {
            method: "GET",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                "X-CSRFToken": js_cookie__WEBPACK_IMPORTED_MODULE_0__["default"].get("csrftoken"),
            },
            redirect: "follow",
            referrer: "no-referrer",
        };
        this.showCookiebar = false;
        this.initialize();
    }
    TagManager.prototype.initialize = function () {
        var _this = this;
        this.loadConfig(function () {
            var cookie = js_cookie__WEBPACK_IMPORTED_MODULE_0__["default"].get("wtm");
            if (cookie) {
                var items = cookie.split("|");
                items.map(function (item) {
                    var parts = item.split(":", 2);
                    if (parts.length > 0)
                        _this.state[parts[0]] = parts[1];
                });
                _this.validate();
                _this.loadData(null);
            }
        });
    };
    TagManager.prototype.validate = function () {
        var _this = this;
        // Verify the browser allows cookies.
        var enabled = navigator.cookieEnabled;
        if (!enabled) {
            js_cookie__WEBPACK_IMPORTED_MODULE_0__["default"].set("wtm_verification", "verification");
            enabled = js_cookie__WEBPACK_IMPORTED_MODULE_0__["default"].get("wtm_verification") !== undefined;
        }
        if (enabled) {
            Object.keys(this.config.tag_types).forEach(function (tagType) {
                if (_this.state[tagType] === "unset" ||
                    _this.state[tagType] == "none" ||
                    _this.state[tagType] == "pending") {
                    _this.showCookiebar = true;
                }
            });
        }
        if (this.showCookiebar) {
            new _cookie_bar__WEBPACK_IMPORTED_MODULE_2__["default"](this);
        }
        if (this.config.triggers && this.config.triggers.length > 0) {
            var triggers = this.config.triggers;
            new _trigger_monitor__WEBPACK_IMPORTED_MODULE_3__["default"](this, triggers);
        }
    };
    TagManager.prototype.loadConfig = function (callback) {
        var _this = this;
        fetch(this.configUrl, this.requestInit)
            .then(function (response) { return response.json(); })
            .then(function (json) {
            _this.config = json;
            if (callback)
                callback();
        })
            .catch(function (error) {
            console.error(error);
        });
    };
    TagManager.prototype.loadData = function (trigger, callback) {
        var _this = this;
        fetch(this.lazyUrl, __assign(__assign({}, this.requestInit), { method: "POST", body: JSON.stringify(__assign(__assign({}, window.location), { trigger: trigger })) }))
            .then(function (response) { return response.json(); })
            .then(function (json) {
            _this.data = json;
            _this.handleLoad();
            if (callback)
                callback();
        })
            .catch(function (error) {
            console.error(error);
        });
    };
    TagManager.prototype.handleLoad = function () {
        this.data.tags.forEach(function (tag) {
            var element = document.createElement(tag.name);
            for (var property in tag.attributes) {
                if (tag.attributes.hasOwnProperty(property)) {
                    element.setAttribute(property, tag.attributes[property]);
                }
            }
            element.appendChild(document.createTextNode(tag.string));
            document.head.appendChild(element);
        });
    };
    return TagManager;
}());
/* harmony default export */ __webpack_exports__["default"] = (TagManager);


/***/ }),

/***/ "./frontend/client/components/trigger_monitor.ts":
/*!*******************************************************!*\
  !*** ./frontend/client/components/trigger_monitor.ts ***!
  \*******************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
var CLICK_ALL_ELEMENTS = "click_all_elements";
var CLICK_SOME_ELEMENTS = "click_some_elements";
var VISIBILITY_ONCE_PER_PAGE = "visibility_once_per_page";
var VISIBILITY_ONCE_PER_ELEMENT = "visibility_once_per_element";
var VISIBILITY_RECURRING = "visibility_recurring";
var FORM_SUBMIT = "form_submit";
var HISTORY_CHANGE = "history_change";
var JAVASCRIPT_ERROR = "javascript_error";
var SCROLL_VERTICAL = "scroll_vertical";
var SCROLL_HORIZONTAL = "scroll_horizontal";
var TIMER_TIMEOUT = "timer_timeout";
var TIMER_INTERVAL = "timer_interval";
var TriggerMonitor = /** @class */ (function () {
    function TriggerMonitor(manager, triggers) {
        this.manager = manager;
        this.triggers = triggers;
        this.wtm = {};
        this.initialize = this.initialize.bind(this);
        this.initialize();
    }
    TriggerMonitor.prototype.initialize = function () {
        for (var _i = 0, _a = this.triggers; _i < _a.length; _i++) {
            var trigger = _a[_i];
            switch (trigger.type) {
                case CLICK_ALL_ELEMENTS:
                case CLICK_SOME_ELEMENTS:
                    this.bindClickListener(trigger);
                    break;
                case VISIBILITY_ONCE_PER_PAGE:
                case VISIBILITY_ONCE_PER_ELEMENT:
                case VISIBILITY_RECURRING:
                    this.bindVisibilityListener(trigger);
                    break;
                case FORM_SUBMIT:
                    this.bindFormSubmitListener(trigger);
                    break;
                case HISTORY_CHANGE:
                    this.bindHistoryChangeListener(trigger);
                    break;
                case JAVASCRIPT_ERROR:
                    this.bindErrorListener(trigger);
                    break;
                case SCROLL_VERTICAL:
                case SCROLL_HORIZONTAL:
                    this.bindScrollListener(trigger);
                    break;
                case TIMER_TIMEOUT:
                case TIMER_INTERVAL:
                    this.bindTimerListener(trigger);
                    break;
                default:
                    console.error("trigger type '".concat(trigger.type, "' not implemented."));
                    break;
            }
        }
    };
    TriggerMonitor.prototype.bindClickListener = function (trigger) {
        var _this = this;
        var handleEvent = function (event) {
            event.stopPropagation();
            var target = event.target;
            _this.sendTrigger(trigger, _this.createElementID(target));
        };
        if (trigger.type === CLICK_ALL_ELEMENTS) {
            document.addEventListener("click", handleEvent);
        }
        else if (trigger.type === CLICK_SOME_ELEMENTS) {
            [].forEach.call(document.querySelectorAll(trigger.value), function (element) {
                element.addEventListener("click", handleEvent);
            });
        }
    };
    TriggerMonitor.prototype.bindVisibilityListener = function (trigger) {
        var _this = this;
        var handleEvent = function (event) {
            [].forEach.call(document.querySelectorAll(trigger.value), function (element) {
                var rect = element.getBoundingClientRect();
                var in_view = rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth);
                if (element.wtm == undefined)
                    element.wtm = {};
                if (in_view) {
                    if (trigger.type === VISIBILITY_ONCE_PER_PAGE && !_this.wtm[trigger.slug]) {
                        _this.wtm[trigger.slug] = true;
                        _this.sendTrigger(trigger, _this.createElementID(element));
                    }
                    else if (trigger.type === VISIBILITY_ONCE_PER_ELEMENT && !element.wtm[trigger.slug]) {
                        element.wtm[trigger.slug] = true;
                        _this.sendTrigger(trigger, _this.createElementID(element));
                    }
                    else if (trigger.type === VISIBILITY_RECURRING && !element.wtm[trigger.slug]) {
                        element.wtm[trigger.slug] = true;
                        _this.sendTrigger(trigger, _this.createElementID(element));
                    }
                }
                else if (trigger.type === VISIBILITY_RECURRING) {
                    element.wtm[trigger.slug] = false;
                }
            });
        };
        document.addEventListener("load", handleEvent, { passive: false });
        document.addEventListener("scroll", handleEvent, { passive: true });
        document.addEventListener("resize", handleEvent, { passive: true });
    };
    TriggerMonitor.prototype.bindFormSubmitListener = function (trigger) {
        var _this = this;
        var handleEvent = function (event) {
            event.preventDefault();
            var target = event.target;
            _this.sendTrigger(trigger, _this.createElementID(target));
            target.submit();
        };
        [].forEach.call(document.querySelectorAll("form"), function (element) {
            element.addEventListener("submit", handleEvent, { passive: false });
        });
    };
    TriggerMonitor.prototype.bindHistoryChangeListener = function (trigger) {
        var _this = this;
        var handleEvent = function (event) {
            _this.sendTrigger(trigger, event.type);
        };
        window.addEventListener("popstate", handleEvent);
    };
    TriggerMonitor.prototype.bindErrorListener = function (trigger) {
        var _this = this;
        var handleEvent = function (event) {
            _this.sendTrigger(trigger, event.message);
        };
        window.addEventListener("error", handleEvent);
    };
    TriggerMonitor.prototype.bindScrollListener = function (trigger) {
        var _this = this;
        var handleEvent = function () {
            var scrollPercentage = -1000;
            if (trigger.type === SCROLL_VERTICAL) {
                scrollPercentage = _this.yScrollPercentage;
            }
            else if (trigger.type === SCROLL_HORIZONTAL) {
                scrollPercentage = _this.xScrollPercentage;
            }
            if (scrollPercentage >= trigger.value && !_this.wtm[trigger.slug]) {
                _this.wtm[trigger.slug] = true;
                _this.sendTrigger(trigger, scrollPercentage);
            }
            else if (scrollPercentage < trigger.value) {
                _this.wtm[trigger.slug] = false;
            }
        };
        document.addEventListener("scroll", handleEvent, { passive: true });
    };
    TriggerMonitor.prototype.bindTimerListener = function (trigger) {
        var _this = this;
        var handleEvent = function () {
            var now = new Date();
            _this.sendTrigger(trigger, now.toISOString());
        };
        if (trigger.type === TIMER_TIMEOUT) {
            window.setTimeout(handleEvent, trigger.value);
        }
        else if (trigger.type === TIMER_INTERVAL) {
            window.setInterval(handleEvent, trigger.value);
        }
    };
    TriggerMonitor.prototype.sendTrigger = function (trigger, value) {
        trigger.value = value;
        this.manager.loadData(trigger);
    };
    Object.defineProperty(TriggerMonitor.prototype, "yScrollPercentage", {
        get: function () {
            var distance = document.documentElement["scrollTop"] || document.body["scrollTop"];
            var offset = (document.documentElement["scrollHeight"] || document.body["scrollHeight"]) -
                document.documentElement.clientHeight;
            return (distance / offset) * 100;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TriggerMonitor.prototype, "xScrollPercentage", {
        get: function () {
            var distance = document.documentElement["scrollLeft"] || document.body["scrollLeft"];
            var offset = (document.documentElement["scrollWidth"] || document.body["scrollWidth"]) -
                document.documentElement.clientHeight;
            return (distance / offset) * 100;
        },
        enumerable: false,
        configurable: true
    });
    TriggerMonitor.prototype.createElementID = function (el) {
        var tag = el.tagName.toLowerCase();
        var ids = [];
        var classes = [];
        var attributes = [];
        [].forEach.call(el.attributes, function (attr) {
            var name = attr.name, value = attr.value;
            switch (name) {
                case "id":
                    for (var _i = 0, _a = value.split(" "); _i < _a.length; _i++) {
                        var part = _a[_i];
                        if (part)
                            ids.push("#".concat(part));
                    }
                    break;
                case "class":
                    for (var _b = 0, _c = value.split(" "); _b < _c.length; _b++) {
                        var part = _c[_b];
                        if (part)
                            classes.push(".".concat(part));
                    }
                    break;
                default:
                    attributes.push("[".concat(name, "=").concat(value, "]"));
                    break;
            }
        });
        return tag + ids.join("") + classes.join("") + attributes.join("");
    };
    return TriggerMonitor;
}());
/* harmony default export */ __webpack_exports__["default"] = (TriggerMonitor);


/***/ }),

/***/ "./node_modules/whatwg-fetch/fetch.js":
/*!********************************************!*\
  !*** ./node_modules/whatwg-fetch/fetch.js ***!
  \********************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DOMException": function() { return /* binding */ DOMException; },
/* harmony export */   "Headers": function() { return /* binding */ Headers; },
/* harmony export */   "Request": function() { return /* binding */ Request; },
/* harmony export */   "Response": function() { return /* binding */ Response; },
/* harmony export */   "fetch": function() { return /* binding */ fetch; }
/* harmony export */ });
var global =
  (typeof globalThis !== 'undefined' && globalThis) ||
  (typeof self !== 'undefined' && self) ||
  (typeof global !== 'undefined' && global)

var support = {
  searchParams: 'URLSearchParams' in global,
  iterable: 'Symbol' in global && 'iterator' in Symbol,
  blob:
    'FileReader' in global &&
    'Blob' in global &&
    (function() {
      try {
        new Blob()
        return true
      } catch (e) {
        return false
      }
    })(),
  formData: 'FormData' in global,
  arrayBuffer: 'ArrayBuffer' in global
}

function isDataView(obj) {
  return obj && DataView.prototype.isPrototypeOf(obj)
}

if (support.arrayBuffer) {
  var viewClasses = [
    '[object Int8Array]',
    '[object Uint8Array]',
    '[object Uint8ClampedArray]',
    '[object Int16Array]',
    '[object Uint16Array]',
    '[object Int32Array]',
    '[object Uint32Array]',
    '[object Float32Array]',
    '[object Float64Array]'
  ]

  var isArrayBufferView =
    ArrayBuffer.isView ||
    function(obj) {
      return obj && viewClasses.indexOf(Object.prototype.toString.call(obj)) > -1
    }
}

function normalizeName(name) {
  if (typeof name !== 'string') {
    name = String(name)
  }
  if (/[^a-z0-9\-#$%&'*+.^_`|~!]/i.test(name) || name === '') {
    throw new TypeError('Invalid character in header field name: "' + name + '"')
  }
  return name.toLowerCase()
}

function normalizeValue(value) {
  if (typeof value !== 'string') {
    value = String(value)
  }
  return value
}

// Build a destructive iterator for the value list
function iteratorFor(items) {
  var iterator = {
    next: function() {
      var value = items.shift()
      return {done: value === undefined, value: value}
    }
  }

  if (support.iterable) {
    iterator[Symbol.iterator] = function() {
      return iterator
    }
  }

  return iterator
}

function Headers(headers) {
  this.map = {}

  if (headers instanceof Headers) {
    headers.forEach(function(value, name) {
      this.append(name, value)
    }, this)
  } else if (Array.isArray(headers)) {
    headers.forEach(function(header) {
      this.append(header[0], header[1])
    }, this)
  } else if (headers) {
    Object.getOwnPropertyNames(headers).forEach(function(name) {
      this.append(name, headers[name])
    }, this)
  }
}

Headers.prototype.append = function(name, value) {
  name = normalizeName(name)
  value = normalizeValue(value)
  var oldValue = this.map[name]
  this.map[name] = oldValue ? oldValue + ', ' + value : value
}

Headers.prototype['delete'] = function(name) {
  delete this.map[normalizeName(name)]
}

Headers.prototype.get = function(name) {
  name = normalizeName(name)
  return this.has(name) ? this.map[name] : null
}

Headers.prototype.has = function(name) {
  return this.map.hasOwnProperty(normalizeName(name))
}

Headers.prototype.set = function(name, value) {
  this.map[normalizeName(name)] = normalizeValue(value)
}

Headers.prototype.forEach = function(callback, thisArg) {
  for (var name in this.map) {
    if (this.map.hasOwnProperty(name)) {
      callback.call(thisArg, this.map[name], name, this)
    }
  }
}

Headers.prototype.keys = function() {
  var items = []
  this.forEach(function(value, name) {
    items.push(name)
  })
  return iteratorFor(items)
}

Headers.prototype.values = function() {
  var items = []
  this.forEach(function(value) {
    items.push(value)
  })
  return iteratorFor(items)
}

Headers.prototype.entries = function() {
  var items = []
  this.forEach(function(value, name) {
    items.push([name, value])
  })
  return iteratorFor(items)
}

if (support.iterable) {
  Headers.prototype[Symbol.iterator] = Headers.prototype.entries
}

function consumed(body) {
  if (body.bodyUsed) {
    return Promise.reject(new TypeError('Already read'))
  }
  body.bodyUsed = true
}

function fileReaderReady(reader) {
  return new Promise(function(resolve, reject) {
    reader.onload = function() {
      resolve(reader.result)
    }
    reader.onerror = function() {
      reject(reader.error)
    }
  })
}

function readBlobAsArrayBuffer(blob) {
  var reader = new FileReader()
  var promise = fileReaderReady(reader)
  reader.readAsArrayBuffer(blob)
  return promise
}

function readBlobAsText(blob) {
  var reader = new FileReader()
  var promise = fileReaderReady(reader)
  reader.readAsText(blob)
  return promise
}

function readArrayBufferAsText(buf) {
  var view = new Uint8Array(buf)
  var chars = new Array(view.length)

  for (var i = 0; i < view.length; i++) {
    chars[i] = String.fromCharCode(view[i])
  }
  return chars.join('')
}

function bufferClone(buf) {
  if (buf.slice) {
    return buf.slice(0)
  } else {
    var view = new Uint8Array(buf.byteLength)
    view.set(new Uint8Array(buf))
    return view.buffer
  }
}

function Body() {
  this.bodyUsed = false

  this._initBody = function(body) {
    /*
      fetch-mock wraps the Response object in an ES6 Proxy to
      provide useful test harness features such as flush. However, on
      ES5 browsers without fetch or Proxy support pollyfills must be used;
      the proxy-pollyfill is unable to proxy an attribute unless it exists
      on the object before the Proxy is created. This change ensures
      Response.bodyUsed exists on the instance, while maintaining the
      semantic of setting Request.bodyUsed in the constructor before
      _initBody is called.
    */
    this.bodyUsed = this.bodyUsed
    this._bodyInit = body
    if (!body) {
      this._bodyText = ''
    } else if (typeof body === 'string') {
      this._bodyText = body
    } else if (support.blob && Blob.prototype.isPrototypeOf(body)) {
      this._bodyBlob = body
    } else if (support.formData && FormData.prototype.isPrototypeOf(body)) {
      this._bodyFormData = body
    } else if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
      this._bodyText = body.toString()
    } else if (support.arrayBuffer && support.blob && isDataView(body)) {
      this._bodyArrayBuffer = bufferClone(body.buffer)
      // IE 10-11 can't handle a DataView body.
      this._bodyInit = new Blob([this._bodyArrayBuffer])
    } else if (support.arrayBuffer && (ArrayBuffer.prototype.isPrototypeOf(body) || isArrayBufferView(body))) {
      this._bodyArrayBuffer = bufferClone(body)
    } else {
      this._bodyText = body = Object.prototype.toString.call(body)
    }

    if (!this.headers.get('content-type')) {
      if (typeof body === 'string') {
        this.headers.set('content-type', 'text/plain;charset=UTF-8')
      } else if (this._bodyBlob && this._bodyBlob.type) {
        this.headers.set('content-type', this._bodyBlob.type)
      } else if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
        this.headers.set('content-type', 'application/x-www-form-urlencoded;charset=UTF-8')
      }
    }
  }

  if (support.blob) {
    this.blob = function() {
      var rejected = consumed(this)
      if (rejected) {
        return rejected
      }

      if (this._bodyBlob) {
        return Promise.resolve(this._bodyBlob)
      } else if (this._bodyArrayBuffer) {
        return Promise.resolve(new Blob([this._bodyArrayBuffer]))
      } else if (this._bodyFormData) {
        throw new Error('could not read FormData body as blob')
      } else {
        return Promise.resolve(new Blob([this._bodyText]))
      }
    }

    this.arrayBuffer = function() {
      if (this._bodyArrayBuffer) {
        var isConsumed = consumed(this)
        if (isConsumed) {
          return isConsumed
        }
        if (ArrayBuffer.isView(this._bodyArrayBuffer)) {
          return Promise.resolve(
            this._bodyArrayBuffer.buffer.slice(
              this._bodyArrayBuffer.byteOffset,
              this._bodyArrayBuffer.byteOffset + this._bodyArrayBuffer.byteLength
            )
          )
        } else {
          return Promise.resolve(this._bodyArrayBuffer)
        }
      } else {
        return this.blob().then(readBlobAsArrayBuffer)
      }
    }
  }

  this.text = function() {
    var rejected = consumed(this)
    if (rejected) {
      return rejected
    }

    if (this._bodyBlob) {
      return readBlobAsText(this._bodyBlob)
    } else if (this._bodyArrayBuffer) {
      return Promise.resolve(readArrayBufferAsText(this._bodyArrayBuffer))
    } else if (this._bodyFormData) {
      throw new Error('could not read FormData body as text')
    } else {
      return Promise.resolve(this._bodyText)
    }
  }

  if (support.formData) {
    this.formData = function() {
      return this.text().then(decode)
    }
  }

  this.json = function() {
    return this.text().then(JSON.parse)
  }

  return this
}

// HTTP methods whose capitalization should be normalized
var methods = ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST', 'PUT']

function normalizeMethod(method) {
  var upcased = method.toUpperCase()
  return methods.indexOf(upcased) > -1 ? upcased : method
}

function Request(input, options) {
  if (!(this instanceof Request)) {
    throw new TypeError('Please use the "new" operator, this DOM object constructor cannot be called as a function.')
  }

  options = options || {}
  var body = options.body

  if (input instanceof Request) {
    if (input.bodyUsed) {
      throw new TypeError('Already read')
    }
    this.url = input.url
    this.credentials = input.credentials
    if (!options.headers) {
      this.headers = new Headers(input.headers)
    }
    this.method = input.method
    this.mode = input.mode
    this.signal = input.signal
    if (!body && input._bodyInit != null) {
      body = input._bodyInit
      input.bodyUsed = true
    }
  } else {
    this.url = String(input)
  }

  this.credentials = options.credentials || this.credentials || 'same-origin'
  if (options.headers || !this.headers) {
    this.headers = new Headers(options.headers)
  }
  this.method = normalizeMethod(options.method || this.method || 'GET')
  this.mode = options.mode || this.mode || null
  this.signal = options.signal || this.signal
  this.referrer = null

  if ((this.method === 'GET' || this.method === 'HEAD') && body) {
    throw new TypeError('Body not allowed for GET or HEAD requests')
  }
  this._initBody(body)

  if (this.method === 'GET' || this.method === 'HEAD') {
    if (options.cache === 'no-store' || options.cache === 'no-cache') {
      // Search for a '_' parameter in the query string
      var reParamSearch = /([?&])_=[^&]*/
      if (reParamSearch.test(this.url)) {
        // If it already exists then set the value with the current time
        this.url = this.url.replace(reParamSearch, '$1_=' + new Date().getTime())
      } else {
        // Otherwise add a new '_' parameter to the end with the current time
        var reQueryString = /\?/
        this.url += (reQueryString.test(this.url) ? '&' : '?') + '_=' + new Date().getTime()
      }
    }
  }
}

Request.prototype.clone = function() {
  return new Request(this, {body: this._bodyInit})
}

function decode(body) {
  var form = new FormData()
  body
    .trim()
    .split('&')
    .forEach(function(bytes) {
      if (bytes) {
        var split = bytes.split('=')
        var name = split.shift().replace(/\+/g, ' ')
        var value = split.join('=').replace(/\+/g, ' ')
        form.append(decodeURIComponent(name), decodeURIComponent(value))
      }
    })
  return form
}

function parseHeaders(rawHeaders) {
  var headers = new Headers()
  // Replace instances of \r\n and \n followed by at least one space or horizontal tab with a space
  // https://tools.ietf.org/html/rfc7230#section-3.2
  var preProcessedHeaders = rawHeaders.replace(/\r?\n[\t ]+/g, ' ')
  // Avoiding split via regex to work around a common IE11 bug with the core-js 3.6.0 regex polyfill
  // https://github.com/github/fetch/issues/748
  // https://github.com/zloirock/core-js/issues/751
  preProcessedHeaders
    .split('\r')
    .map(function(header) {
      return header.indexOf('\n') === 0 ? header.substr(1, header.length) : header
    })
    .forEach(function(line) {
      var parts = line.split(':')
      var key = parts.shift().trim()
      if (key) {
        var value = parts.join(':').trim()
        headers.append(key, value)
      }
    })
  return headers
}

Body.call(Request.prototype)

function Response(bodyInit, options) {
  if (!(this instanceof Response)) {
    throw new TypeError('Please use the "new" operator, this DOM object constructor cannot be called as a function.')
  }
  if (!options) {
    options = {}
  }

  this.type = 'default'
  this.status = options.status === undefined ? 200 : options.status
  this.ok = this.status >= 200 && this.status < 300
  this.statusText = options.statusText === undefined ? '' : '' + options.statusText
  this.headers = new Headers(options.headers)
  this.url = options.url || ''
  this._initBody(bodyInit)
}

Body.call(Response.prototype)

Response.prototype.clone = function() {
  return new Response(this._bodyInit, {
    status: this.status,
    statusText: this.statusText,
    headers: new Headers(this.headers),
    url: this.url
  })
}

Response.error = function() {
  var response = new Response(null, {status: 0, statusText: ''})
  response.type = 'error'
  return response
}

var redirectStatuses = [301, 302, 303, 307, 308]

Response.redirect = function(url, status) {
  if (redirectStatuses.indexOf(status) === -1) {
    throw new RangeError('Invalid status code')
  }

  return new Response(null, {status: status, headers: {location: url}})
}

var DOMException = global.DOMException
try {
  new DOMException()
} catch (err) {
  DOMException = function(message, name) {
    this.message = message
    this.name = name
    var error = Error(message)
    this.stack = error.stack
  }
  DOMException.prototype = Object.create(Error.prototype)
  DOMException.prototype.constructor = DOMException
}

function fetch(input, init) {
  return new Promise(function(resolve, reject) {
    var request = new Request(input, init)

    if (request.signal && request.signal.aborted) {
      return reject(new DOMException('Aborted', 'AbortError'))
    }

    var xhr = new XMLHttpRequest()

    function abortXhr() {
      xhr.abort()
    }

    xhr.onload = function() {
      var options = {
        status: xhr.status,
        statusText: xhr.statusText,
        headers: parseHeaders(xhr.getAllResponseHeaders() || '')
      }
      options.url = 'responseURL' in xhr ? xhr.responseURL : options.headers.get('X-Request-URL')
      var body = 'response' in xhr ? xhr.response : xhr.responseText
      setTimeout(function() {
        resolve(new Response(body, options))
      }, 0)
    }

    xhr.onerror = function() {
      setTimeout(function() {
        reject(new TypeError('Network request failed'))
      }, 0)
    }

    xhr.ontimeout = function() {
      setTimeout(function() {
        reject(new TypeError('Network request failed'))
      }, 0)
    }

    xhr.onabort = function() {
      setTimeout(function() {
        reject(new DOMException('Aborted', 'AbortError'))
      }, 0)
    }

    function fixUrl(url) {
      try {
        return url === '' && global.location.href ? global.location.href : url
      } catch (e) {
        return url
      }
    }

    xhr.open(request.method, fixUrl(request.url), true)

    if (request.credentials === 'include') {
      xhr.withCredentials = true
    } else if (request.credentials === 'omit') {
      xhr.withCredentials = false
    }

    if ('responseType' in xhr) {
      if (support.blob) {
        xhr.responseType = 'blob'
      } else if (
        support.arrayBuffer &&
        request.headers.get('Content-Type') &&
        request.headers.get('Content-Type').indexOf('application/octet-stream') !== -1
      ) {
        xhr.responseType = 'arraybuffer'
      }
    }

    if (init && typeof init.headers === 'object' && !(init.headers instanceof Headers)) {
      Object.getOwnPropertyNames(init.headers).forEach(function(name) {
        xhr.setRequestHeader(name, normalizeValue(init.headers[name]))
      })
    } else {
      request.headers.forEach(function(value, name) {
        xhr.setRequestHeader(name, value)
      })
    }

    if (request.signal) {
      request.signal.addEventListener('abort', abortXhr)

      xhr.onreadystatechange = function() {
        // DONE (success or failure)
        if (xhr.readyState === 4) {
          request.signal.removeEventListener('abort', abortXhr)
        }
      }
    }

    xhr.send(typeof request._bodyInit === 'undefined' ? null : request._bodyInit)
  })
}

fetch.polyfill = true

if (!global.fetch) {
  global.fetch = fetch
  global.Headers = Headers
  global.Request = Request
  global.Response = Response
}


/***/ }),

/***/ "./node_modules/js-cookie/dist/js.cookie.mjs":
/*!***************************************************!*\
  !*** ./node_modules/js-cookie/dist/js.cookie.mjs ***!
  \***************************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/*! js-cookie v3.0.1 | MIT */
/* eslint-disable no-var */
function assign (target) {
  for (var i = 1; i < arguments.length; i++) {
    var source = arguments[i];
    for (var key in source) {
      target[key] = source[key];
    }
  }
  return target
}
/* eslint-enable no-var */

/* eslint-disable no-var */
var defaultConverter = {
  read: function (value) {
    if (value[0] === '"') {
      value = value.slice(1, -1);
    }
    return value.replace(/(%[\dA-F]{2})+/gi, decodeURIComponent)
  },
  write: function (value) {
    return encodeURIComponent(value).replace(
      /%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g,
      decodeURIComponent
    )
  }
};
/* eslint-enable no-var */

/* eslint-disable no-var */

function init (converter, defaultAttributes) {
  function set (key, value, attributes) {
    if (typeof document === 'undefined') {
      return
    }

    attributes = assign({}, defaultAttributes, attributes);

    if (typeof attributes.expires === 'number') {
      attributes.expires = new Date(Date.now() + attributes.expires * 864e5);
    }
    if (attributes.expires) {
      attributes.expires = attributes.expires.toUTCString();
    }

    key = encodeURIComponent(key)
      .replace(/%(2[346B]|5E|60|7C)/g, decodeURIComponent)
      .replace(/[()]/g, escape);

    var stringifiedAttributes = '';
    for (var attributeName in attributes) {
      if (!attributes[attributeName]) {
        continue
      }

      stringifiedAttributes += '; ' + attributeName;

      if (attributes[attributeName] === true) {
        continue
      }

      // Considers RFC 6265 section 5.2:
      // ...
      // 3.  If the remaining unparsed-attributes contains a %x3B (";")
      //     character:
      // Consume the characters of the unparsed-attributes up to,
      // not including, the first %x3B (";") character.
      // ...
      stringifiedAttributes += '=' + attributes[attributeName].split(';')[0];
    }

    return (document.cookie =
      key + '=' + converter.write(value, key) + stringifiedAttributes)
  }

  function get (key) {
    if (typeof document === 'undefined' || (arguments.length && !key)) {
      return
    }

    // To prevent the for loop in the first place assign an empty array
    // in case there are no cookies at all.
    var cookies = document.cookie ? document.cookie.split('; ') : [];
    var jar = {};
    for (var i = 0; i < cookies.length; i++) {
      var parts = cookies[i].split('=');
      var value = parts.slice(1).join('=');

      try {
        var foundKey = decodeURIComponent(parts[0]);
        jar[foundKey] = converter.read(value, foundKey);

        if (key === foundKey) {
          break
        }
      } catch (e) {}
    }

    return key ? jar[key] : jar
  }

  return Object.create(
    {
      set: set,
      get: get,
      remove: function (key, attributes) {
        set(
          key,
          '',
          assign({}, attributes, {
            expires: -1
          })
        );
      },
      withAttributes: function (attributes) {
        return init(this.converter, assign({}, this.attributes, attributes))
      },
      withConverter: function (converter) {
        return init(assign({}, this.converter, converter), this.attributes)
      }
    },
    {
      attributes: { value: Object.freeze(defaultAttributes) },
      converter: { value: Object.freeze(converter) }
    }
  )
}

var api = init(defaultConverter, { path: '/' });
/* eslint-enable no-var */

/* harmony default export */ __webpack_exports__["default"] = (api);


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
/******/ 	/* webpack/runtime/define property getters */
/******/ 	!function() {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = function(exports, definition) {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	!function() {
/******/ 		__webpack_require__.o = function(obj, prop) { return Object.prototype.hasOwnProperty.call(obj, prop); }
/******/ 	}();
/******/ 	
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
/*!********************************!*\
  !*** ./frontend/client/wtm.ts ***!
  \********************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_tag_manager__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components/tag_manager */ "./frontend/client/components/tag_manager.ts");

(function () {
    new _components_tag_manager__WEBPACK_IMPORTED_MODULE_0__["default"]();
})();

}();
/******/ })()
;
//# sourceMappingURL=sourcemaps/wtm.bundle.js.map