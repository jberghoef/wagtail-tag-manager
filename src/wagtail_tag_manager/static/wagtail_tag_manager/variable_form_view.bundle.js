!function(e){var t={};function n(i){if(t[i])return t[i].exports;var r=t[i]={i:i,l:!1,exports:{}};return e[i].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,i){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:i})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(i,r,function(t){return e[t]}.bind(null,r));return i},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=9)}({10:function(e,t){var n=function(){function e(){this.variableSelect=document.getElementById("id_variable_type"),this.valueInput=document.getElementById("id_value"),this.initialize=this.initialize.bind(this),this.handleVariableChange=this.handleVariableChange.bind(this),this.variableSelect.addEventListener("change",this.handleVariableChange),this.initialize()}return e.prototype.initialize=function(){this.handleVariableChange()},e.prototype.handleVariableChange=function(e){void 0===e&&(e=null),"+"!==this.variableSelect.options[this.variableSelect.selectedIndex].value.slice(-1)?(this.valueInput.disabled=!0,this.valueInput.value=""):this.valueInput.disabled=!1},e}();document.addEventListener("DOMContentLoaded",(function(e){new n}))},9:function(e,t,n){e.exports=n(10)}});