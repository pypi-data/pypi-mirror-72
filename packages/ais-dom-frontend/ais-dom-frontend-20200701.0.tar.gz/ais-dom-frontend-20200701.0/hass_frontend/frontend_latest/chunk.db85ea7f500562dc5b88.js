(self.webpackJsonp=self.webpackJsonp||[]).push([[123,14],{120:function(e){e.exports=JSON.parse('{"version":"4.9.95","parts":[{"file":"ac96ae39d5ca52d23a4ca3d8c6efd5817270091d"},{"start":"alarm-o","file":"d561c36273559890cb6dd9ff93c52f65ebd813c1"},{"start":"arrow-decision-o","file":"c9b7511d0d2534fd6eb9a2d4096ae2d6986c5437"},{"start":"basket-","file":"bc336f888b18158e39d0bf49be0f4c6159b9cc85"},{"start":"blur","file":"119bbb7a5c295866fca20bccb3f56815ad7b9a3d"},{"start":"bus-d","file":"cb82b14ed371a8b31c33d1e86221168c88a2daa1"},{"start":"card-s","file":"c696f5a7ff858eed9b0360a22afa93a4e149f281"},{"start":"circle-slice-7","file":"0aa03086dceff355dce1a5fd76b655532d1ce106"},{"start":"comment-t","file":"b80a4774f52c2c2a5e4239cc559281cb5a46541e"},{"start":"cursor-m","file":"689ebae34d4c444f2ac79c845935f6a39d9cb55e"},{"start":"door-closed-","file":"e3d51e324319d10fd3e55ac99e0748aa4e5055ee"},{"start":"eraser-","file":"42a1c8b700556b7e088be85381b9ac492be31732"},{"start":"file-pdf-o","file":"6c687283fbb6d8413dccbaac610e5e91917d0197"},{"start":"folder-alert-","file":"8be2f984e49a6eaa69a04fd95bd805b3331d94ae"},{"start":"gamepad-circle-l","file":"986ac139fe53bb8be3fedc1ee88af3d7d3e5d53e"},{"start":"google-p","file":"dafb98730fb6f5fcb84b8b94daa920f839d40489"},{"start":"help-network-","file":"a9beb4f10e3575df275e888c1160fc0c1f479a6e"},{"start":"je","file":"df7feb02fe5538edfabb04344646a7318b595259"},{"start":"layers-ou","file":"d8a4c48654c6d31621b08d77a32a5960d64b010c"},{"start":"map-marker-radius-","file":"912daef373e4d5f510836a3b5d195046dfba22c2"},{"start":"music-","file":"cdd1042da2ee7f986e1b035f47901990602c2396"},{"start":"ou","file":"e0ca7b494b7d522f697b00bf83ef596485c7bb98"},{"start":"phone-paused-","file":"93595e945f217083b66408535f56938cb236e91a"},{"start":"qual","file":"d225ac5378ccb48ee4228521f7325526bec0ebd9"},{"start":"safe-square-","file":"bb47adffdf4b9ae3bdcddf438611375c79b73e22"},{"start":"shield-h","file":"344afc4666d56ca2265ec5b8e693b326350c8fcc"},{"start":"source-repository-","file":"369429d8708392e396580146ef6b5b29bdc980a2"},{"start":"table-p","file":"20834d5f95635fd28910309cbdf72cd5249db156"},{"start":"tow","file":"475e7121d81fbc25c95af2cf38622d5192dc005c"},{"start":"vibrate-","file":"56507ed6d56716b4e846f901e9d980a7cdb56555"},{"start":"weather-su","file":"22359538f304ca383bbc4401af6207227c68e4ec"},{"start":"zodiac-li","file":"ad46cd3ed385233a41d3bda8b2975dfcf14a02a3"}]}')},136:function(e,t,r){"use strict";r(138);var i=r(0);r(110);const o=window;"customIconsets"in o||(o.customIconsets={});const n=o.customIconsets;const a=r(120);var s=r(61);const c=new s.a("hass-icon-db","mdi-icon-store"),l=["mdi","hass","hassio","hademo"];let d=[];var p=r(76);function u(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const g={};Object(s.c)("_version",c).then(e=>{e?e!==a.version&&Object(s.b)(c).then(()=>Object(s.d)("_version",a.version,c)):Object(s.d)("_version",a.version,c)});const w=Object(p.a)(()=>(async e=>{const t=Object.keys(e),r=await Promise.all(Object.values(e));c._withIDBStore("readwrite",i=>{r.forEach((r,o)=>{Object.entries(r).forEach(([e,t])=>{i.put(t,e)}),delete e[t[o]]})})})(g),2e3),k={};!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(m(n.descriptor)||m(o.descriptor)){if(h(n)||h(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(h(n)){if(h(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}f(n,o)}else t.push(n)}return t}(a.d.map(u)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(i.d)("ha-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"icon",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_path",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_legacy",value:()=>!1},{kind:"method",key:"updated",value:function(e){e.has("icon")&&(this._path=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?i.f`<iron-icon .icon=${this.icon}></iron-icon>`:i.f`<ha-svg-icon
      .path=${this._path}
      .viewBox=${this._viewBox}
    ></ha-svg-icon>`:i.f``}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const[e,t]=this.icon.split(":",2);if(!e||!t)return;if(!l.includes(e)){if(e in n){const r=n[e];return void(r&&this._setCustomPath(r(t)))}return void(this._legacy=!0)}if(this._legacy=!1,t in k)return void(this._path=k[t]);let r;try{r=await(e=>new Promise((t,r)=>{if(d.push([e,t,r]),d.length>1)return;const i=[];c._withIDBStore("readonly",e=>{for(const[t,r]of d)i.push([r,e.get(t)]);d=[]}).then(()=>{for(const[e,t]of i)e(t.result)}).catch(()=>{for(const[,,e]of d)e();d=[]})}))(t)}catch(s){r=void 0}if(r)return this._path=r,void(k[t]=r);const i=(e=>{let t;for(const r of a.parts){if(void 0!==r.start&&e<r.start)break;t=r}return t.file})(t);if(i in g)return void this._setPath(g[i],t);const o=fetch(`/static/mdi/${i}.json`).then(e=>e.json());g[i]=o,this._setPath(o,t),w()}},{kind:"method",key:"_setCustomPath",value:async function(e){const t=await e;this._path=t.path,this._viewBox=t.viewBox}},{kind:"method",key:"_setPath",value:async function(e,t){const r=await e;this._path=r[t],k[t]=r[t]}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        fill: currentcolor;
      }
    `}}]}}),i.a)},211:function(e,t,r){"use strict";r.d(t,"a",(function(){return a})),r.d(t,"b",(function(){return s})),r.d(t,"c",(function(){return c}));var i=r(13);const o=()=>Promise.all([r.e(2),r.e(6),r.e(24),r.e(168),r.e(46)]).then(r.bind(null,268)),n=(e,t,r)=>new Promise(n=>{const a=t.cancel,s=t.confirm;Object(i.a)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:{...t,...r,cancel:()=>{n(!!(null==r?void 0:r.prompt)&&null),a&&a()},confirm:e=>{n(!(null==r?void 0:r.prompt)||e),s&&s(e)}}})}),a=(e,t)=>n(e,t),s=(e,t)=>n(e,t,{confirmation:!0}),c=(e,t)=>n(e,t,{prompt:!0})},213:function(e,t,r){"use strict";r.d(t,"a",(function(){return n}));var i=r(9),o=r(13);const n=Object(i.a)(e=>class extends e{fire(e,t,r){return r=r||{},Object(o.a)(r.node||this,e,t,r)}})},221:function(e,t,r){"use strict";r(261);var i=r(230),o=r(0),n=r(127);function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function f(e,t,r){return(f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=h(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function h(e){return(h=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const m=customElements.get("mwc-switch");!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var f=t((function(e){o.initializeInstanceElements(e,h.elements)}),r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(l(n.descriptor)||l(o.descriptor)){if(c(n)||c(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(c(n)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(f.d.map(a)),e);o.initializeClassElements(f.F,h.elements),o.runClassFinishers(f.F,h.finishers)}([Object(o.d)("ha-switch")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(o.h)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){f(h(r.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.addEventListener("change",()=>{this.haptic&&Object(n.a)("light")})}},{kind:"get",static:!0,key:"styles",value:function(){return[i.a,o.c`
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
      `]}}]}}),m)},279:function(e,t,r){"use strict";var i=r(4),o=r(31),n=r(211),a=r(213);r(284);class s extends(Object(a.a)(o.a)){static get template(){return i.a`
      <ha-progress-button
        id="progress"
        progress="[[progress]]"
        on-click="buttonTapped"
        tabindex="0"
        ><slot></slot
      ></ha-progress-button>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},domain:{type:String},service:{type:String},serviceData:{type:Object,value:{}},confirmation:{type:String}}}callService(){this.progress=!0;var e=this,t={domain:this.domain,service:this.service,serviceData:this.serviceData};this.hass.callService(this.domain,this.service,this.serviceData).then((function(){e.progress=!1,e.$.progress.actionSuccess(),t.success=!0}),(function(){e.progress=!1,e.$.progress.actionError(),t.success=!1})).then((function(){e.fire("hass-service-called",t)}))}buttonTapped(){this.confirmation?Object(n.b)(this,{text:this.confirmation,confirm:()=>this.callService()}):this.callService()}}customElements.define("ha-call-service-button",s)},284:function(e,t,r){"use strict";r(101),r(155);var i=r(4),o=r(31);class n extends o.a{static get template(){return i.a`
      <style>
        :host {
          outline: none;
        }
        .container {
          position: relative;
          display: inline-block;
        }

        mwc-button {
          transition: all 1s;
        }

        .success mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--success-color);
          transition: none;
        }

        .error mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--error-color);
          transition: none;
        }

        .progress {
          @apply --layout;
          @apply --layout-center-center;
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
        }
      </style>
      <div class="container" id="container">
        <mwc-button
          id="button"
          disabled="[[computeDisabled(disabled, progress)]]"
          on-click="buttonTapped"
        >
          <slot></slot>
        </mwc-button>
        <template is="dom-if" if="[[progress]]">
          <div class="progress">
            <ha-circular-progress active size="small"></ha-circular-progress>
          </div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1}}}tempClass(e){var t=this.$.container.classList;t.add(e),setTimeout(()=>{t.remove(e)},1e3)}ready(){super.ready(),this.addEventListener("click",e=>this.buttonTapped(e))}buttonTapped(e){this.progress&&e.stopPropagation()}actionSuccess(){this.tempClass("success")}actionError(){this.tempClass("error")}computeDisabled(e,t){return e||t}}customElements.define("ha-progress-button",n)},343:function(e,t,r){"use strict";r.r(t);var i=r(0),o=(r(249),r(257),r(183),r(158),r(55)),n=(r(203),r(271),r(226),r(178),r(137),r(136),r(377),r(111));function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const f={integrations:[{component:"ais_dom_config_update",path:"/config/ais_dom_config_update",translationKey:"ui.panel.config.ais_dom_config_update.caption",iconPath:n.o,core:!0},{component:"ais_dom_config_wifi",path:"/config/ais_dom_config_wifi",translationKey:"ui.panel.config.ais_dom_config_wifi.caption",iconPath:n.Z,core:!0},{component:"ais_dom_config_display",path:"/config/ais_dom_config_display",translationKey:"ui.panel.config.ais_dom_config_display.caption",iconPath:n.F,core:!0},{component:"ais_dom_config_tts",path:"/config/ais_dom_config_tts",translationKey:"ui.panel.config.ais_dom_config_tts.caption",iconPath:n.c,core:!0},{component:"ais_dom_config_night",path:"/config/ais_dom_config_night",translationKey:"ui.panel.config.ais_dom_config_night.caption",iconPath:n.X,core:!0},{component:"ais_dom_config_remote",path:"/config/ais_dom_config_remote",translationKey:"ui.panel.config.ais_dom_config_remote.caption",iconPath:n.Y,core:!0},{component:"ais_dom_config_logs",path:"/config/ais_dom_config_logs",translationKey:"ui.panel.config.ais_dom_config_logs.caption",iconPath:n.q,core:!0},{component:"ais_dom_config_power",path:"/config/ais_dom_config_power",translationKey:"ui.panel.config.ais_dom_config_power.caption",iconPath:n.P,core:!0}]};!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var f=t((function(e){o.initializeInstanceElements(e,h.elements)}),r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(l(n.descriptor)||l(o.descriptor)){if(c(n)||c(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(c(n)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(f.d.map(a)),e);o.initializeClassElements(f.F,h.elements),o.runClassFinishers(f.F,h.finishers)}([Object(i.d)("ha-config-ais-dom-navigation")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"showAdvanced",value:void 0},{kind:"method",key:"render",value:function(){return i.f`
      ${Object.values(f).map(e=>i.f`
          <ha-card>
            <ha-config-navigation
              .hass=${this.hass}
              .showAdvanced=${this.showAdvanced}
              .pages=${e}
            ></ha-config-navigation>
          </ha-card>
        `)}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      a {
        text-decoration: none;
        color: var(--primary-text-color);
      }
    `}}]}}),i.a);r(184);function h(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function b(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!v(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:b(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=b(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(y(n.descriptor)||y(o.descriptor)){if(v(n)||v(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(v(n)){if(v(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}m(n,o)}else t.push(n)}return t}(a.d.map(h)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(i.d)("ha-config-ais-dom-dashboard")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"narrow",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"isWide",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"showAdvanced",value:void 0},{kind:"method",key:"render",value:function(){return i.f`
      <hass-subpage
        header=${this.hass.localize("ui.panel.config.ais_dom_config.header")}
      >
        <div class$="[[computeClasses(isWide)]]">
          <div class="content">
            <ha-config-section is-wide="[[isWide]]">
              <div slot="header">
                ${this.hass.localize("ui.panel.config.ais_dom_config.header")}
              </div>
              <span slot="introduction">
                ${this.hass.localize("ui.panel.config.ais_dom_config.introduction")}
              </span>
              <ha-config-ais-dom-navigation
                .hass=${this.hass}
                .show-advanced=${this.showAdvanced}
              ></ha-config-ais-dom-navigation>
            </ha-config-section>
          </div>
        </div>
      </hass-subpage>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[o.b,i.c`
        app-header {
          --app-header-background-color: var(--primary-background-color);
        }
        ha-card:last-child {
          margin-bottom: 24px;
        }
        ha-config-section {
          margin-top: -20px;
        }
        ha-card {
          overflow: hidden;
        }
        ha-card a {
          text-decoration: none;
          color: var(--primary-text-color);
        }
        .promo-advanced {
          text-align: center;
          color: var(--secondary-text-color);
          margin-bottom: 24px;
        }
        .promo-advanced a {
          color: var(--secondary-text-color);
        }
      `]}}]}}),i.a)},603:function(e,t,r){"use strict";r.r(t);r(257),r(183),r(290),r(320);var i=r(4),o=r(31);r(184),r(129),r(343),r(221),r(279),r(136);class n extends o.a{static get template(){return i.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        table {
          width: 100%;
        }

        td:first-child {
          width: 33%;
        }

        .validate-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          min-height: 140px;
        }

        .validate-result {
          color: var(--google-green-500);
          font-weight: 500;
        }

        .config-invalid .text {
          color: var(--google-red-500);
          font-weight: 500;
        }

        .config-invalid {
          text-align: center;
          margin-top: 20px;
        }

        .validate-log {
          white-space: pre-wrap;
          direction: ltr;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Oprogramowanie bramki</span>
            <span slot="introduction"
              >Możesz zaktualizować system do najnowszej wersji, wykonać kopię
              zapasową ustawień i zsynchronizować bramkę z Portalem
              Integratora</span
            >
            <ha-card header="Wersja systemu Asystent domowy">
              <div class="card-content">
                [[aisVersionInfo]]
                <div>
                  <div style="margin-top:30px;" id="ha-switch-id">
                    <ha-switch
                      checked="{{autoUpdateMode}}"
                      on-change="changeAutoUpdateMode"
                      style="position: absolute; right: 20px;"
                    ></ha-switch
                    ><span
                      ><h3>
                        Autoaktualizacja
                        <ha-icon icon="[[aisAutoUpdateIcon]]"></ha-icon></h3
                    ></span>
                  </div>
                </div>

                <div style="display: inline-block;">
                  <div>
                    [[aisAutoUpdateInfo]]
                  </div>
                  <div style="margin-top: 15px;">
                    Aktualizacje dostarczają najnowsze funkcjonalności oraz
                    poprawki zapewniające bezpieczeństwo i stabilność działania
                    systemu.
                    <table style="margin-top: 10px;">
                      <template
                        is="dom-repeat"
                        items="[[aisAutoUpdatFullInfo]]"
                      >
                        <tr>
                          <td><ha-icon icon="[[item.name_icon]]"></ha-icon> [[item.name]]</td>
                          <td>[[item.value]]</td>
                          <td>[[item.new_value]]</td>
                          <td><ha-icon icon="[[item.icon]]"></ha-icon></td>
                        </tr>
                        <template
                            is="dom-if"
                            if="[[_isEqualTo(item.name, 'Status')]]"
                          >
                            <tr style="height: 1em;"></tr>
                          </template>
                      </template>
                    </table>
                  </div>
                </div>
                <div class="center-container">
                  <ha-call-service-button
                    class="warning"
                    hass="[[hass]]"
                    domain="ais_updater"
                    service="execute_upgrade"
                    service-data="[[aisUpdateSystemData]]"
                    >[[aisButtonVersionCheckUpgrade]]
                  </ha-call-service-button>
                </div>
              </div>
            </ha-card>

            <ha-card header="Kopia konfiguracji Bramki">
              <div class="card-content">
                W tym miejscu możesz, sprawdzić poprawność ustawień bramki,
                wykonać jej kopię i przesłać ją do portalu integratora. <b>Uwaga,
                ponieważ konfiguracja może zawierać hasła i tokeny dostępu do
                usług, zalecamy zaszyfrować ją hasłem</b>. Gdy kopia jest
                zabezpieczona hasłem, to można ją otworzyć/przywrócić tylko po
                podaniu hasła.
                <h2>
                  Nowa kopia ustawień
                  <ha-icon icon="mdi:cloud-upload-outline"></ha-icon>
                </h2>
                <br />
                <div class="center-container">
                  Kopia zapasowa ustawień:
                  <br />
                  <paper-radio-group selected="all" id="backup_type1">
                      <paper-radio-button name="all">Wszystkich</paper-radio-button>
                      <paper-radio-button name="ha">Home Assistant</paper-radio-button>
                      <paper-radio-button name="zigbee">Zigbee</paper-radio-button>
                  </paper-radio-group>
                  <br />
                  Przed wykonaniem nowej kopii ustawień sprawdź poprawność
                  konfiguracji
                </div>
                <br />
                <div style="border-bottom: 1px solid white;">
                  <template is="dom-if" if="[[!validateLog]]">
                    <div class="validate-container">
                      <div class="validate-result" id="result">
                        [[backupInfo]]
                      </div>
                      <template is="dom-if" if="[[!validating]]">
                        <div class="config-invalid">
                          <span class="text">
                            [[backupError]]
                          </span>
                        </div>
                        <template
                          is="dom-if"
                          if="[[_isEqualTo(backupStep, '1')]]"
                        >
                          <paper-input
                            placeholder="hasło"
                            no-label-float=""
                            type="password"
                            id="password1"
                          ></paper-input>
                        </template>
                        <mwc-button raised="" on-click="doBackup">
                          <template
                            is="dom-if"
                            if="[[_isEqualTo(backupStep, '0')]]"
                          >
                            Sprawdź konfigurację
                          </template>
                          <template
                            is="dom-if"
                            if="[[_isEqualTo(backupStep, '1')]]"
                          >
                            Wykonaj kopie konfiguracji
                          </template>
                        </mwc-button>
                      </template>
                      <template is="dom-if" if="[[validating]]">
                        <paper-spinner active=""></paper-spinner>
                      </template>
                    </div>
                  </template>
                  <template is="dom-if" if="[[validateLog]]">
                    <div class="config-invalid">
                      <mwc-button raised="" on-click="doBackup">
                        Popraw i sprawdź ponownie
                      </mwc-button>
                    </div>
                    <p></p>
                    <div id="configLog" class="validate-log">
                      [[validateLog]]
                    </div>
                  </template>
                </div>

                <template is="dom-if" if="[[isBackupValid]]">
                  <h2>
                    Przywracanie ustawień
                    <ha-icon icon="mdi:backup-restore"></ha-icon>
                  </h2>
                  <div class="validate-container">
                    <table style="margin-top: 40px; margin-bottom: 10px;">
                      <template is="dom-repeat" items="[[aisBackupFullInfo]]">
                        <tr>
                          <td><ha-icon icon="[[item.icon]]"></ha-icon> [[item.name]]</td>
                          <td>[[item.value]]</td>
                          <td>[[item.new_value]]</td>
                        </tr>
                      </template>
                    </table>
                      <div class="validate-container">
                        <div class="validate-result" id="result">
                          [[restoreInfo]]
                        </div>
                        <template is="dom-if" if="[[!validating]]">
                        <div class="config-invalid">
                          <span class="text">
                            [[restoreError]]
                          </span>
                        </div>
                        Przywracanie ustawień z kopii:
                        <br />
                        <paper-radio-group selected="all" id="backup_type2">
                            <paper-radio-button name="all">Wszystkich</paper-radio-button>
                            <paper-radio-button name="ha">Home Assistant</paper-radio-button>
                            <paper-radio-button name="zigbee">Zigbee</paper-radio-button>
                        </paper-radio-group>
                        <br />
                        <paper-input
                          placeholder="hasło"
                          no-label-float=""
                          type="password"
                          id="password2"
                        ></paper-input>
                        <mwc-button raised="" on-click="restoreBackup">
                          Przywróć konfigurację z kopii
                        </mwc-button>
                      </div>
                    </template>
                    <template is="dom-if" if="[[validating]]">
                      <paper-spinner active=""></paper-spinner>
                    </template>
                  </div>
                </template>
              </div>
            </ha-card>

            <ha-card header="Synchronizacja z Portalem Integratora">
              <div class="card-content">
                Jeśli ostatnio wprowadzałeś zmiany w Portalu Integratora, takie
                jak dodanie nowych typów audio czy też dostęp do zewnętrznych
                serwisów, to przyciskiem poniżej możesz uruchomić natychmiastowe
                pobranie tych zmian na bramkę bez czekania na automatyczną
                synchronizację.
                <div class="center-container">
                  <ha-call-service-button
                    class="warning"
                    hass="[[hass]]"
                    domain="script"
                    service="ais_cloud_sync"
                    >Synchronizuj z Portalem Integratora
                  </ha-call-service-button>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,aisVersionInfo:{type:String,computed:"_computeAisVersionInfo(hass)"},aisBackupInfo:{type:String,computed:"_computeAisBackupInfo(hass)"},aisAutoUpdateInfo:{type:String},aisAutoUpdateIcon:{type:String},aisAutoUpdatFullInfo:{type:Array,value:[]},aisBackupFullInfo:{type:Array,value:[]},aisButtonVersionCheckUpgrade:{type:String,computed:"_computeAisButtonVersionCheckUpgrade(hass)"},aisUpdateSystemData:{type:Object,value:{say:!0}},autoUpdateMode:{type:Boolean,computed:"_computeAutoUpdateMode(hass)"},validating:{type:Boolean,value:!1},backupStep:{type:String,value:"0",computed:"_computeAisBackupStep(hass)"},validateLog:{type:String,value:""},backupInfo:{type:String,value:""},backupError:{type:String,value:""},restoreInfo:{type:String,value:""},restoreError:{type:String,value:""},isBackupValid:{type:Boolean,value:null}}}ready(){super.ready(),this.hass.callService("ais_cloud","set_backup_step",{step:"0"}),this.hass.callService("ais_cloud","get_backup_info")}computeClasses(e){return e?"content":"content narrow"}_computeAisVersionInfo(e){var t=e.states["sensor.version_info"],r=t.attributes;return this.aisAutoUpdatFullInfo=[],"update_check_time"in r&&this.aisAutoUpdatFullInfo.push({name:"Sprawdzono o",name_icon:"",value:r.update_check_time,icon:""}),"update_status"in r&&this.aisAutoUpdatFullInfo.push({name:"Status",name_icon:"",value:this.getVersionName(r.update_status),icon:this.getVersionIcon(r.update_status)}),"zigbee2mqtt_current_version"in r&&this.aisAutoUpdatFullInfo.push({name:"Zigbee",name_icon:"mdi:zigbee",value:r.zigbee2mqtt_current_version,new_value:r.zigbee2mqtt_newest_version,icon:r.reinstall_zigbee2mqtt?"hass:alert":"hass:check"}),"dom_app_current_version"in r&&this.aisAutoUpdatFullInfo.push({name:"Home Assistant",name_icon:"mdi:home-assistant",value:r.dom_app_current_version,new_value:r.dom_app_newest_version,icon:r.reinstall_dom_app?"hass:alert":"hass:check"}),"android_app_current_version"in r&&this.aisAutoUpdatFullInfo.push({name:"Android",name_icon:"mdi:android",value:r.android_app_current_version,new_value:r.android_app_newest_version,icon:r.reinstall_android_app?"hass:alert":"hass:check"}),"linux_apt_current_version"in r&&this.aisAutoUpdatFullInfo.push({name:"Linux",name_icon:"mdi:linux",value:r.linux_apt_current_version,new_value:r.linux_apt_newest_version,icon:r.reinstall_linux_apt?"hass:alert":"hass:check"}),t.state}_computeAisBackupStep(e){var t=e.states["sensor.aisbackupinfo"];return"0"===t.state&&(this.validating=!1),t.state}_computeAisBackupInfo(e){var t=e.states["sensor.aisbackupinfo"],r=t.attributes;return this.aisBackupFullInfo=[],this.isBackupValid=!1,this.backupInfo=r.backup_info,this.backupError=r.backup_error,this.restoreInfo=r.restore_info,this.restoreError=r.restore_error,"file_size"in r&&(this.isBackupValid=!!r.file_name,this.aisBackupFullInfo.push({name:"Home Assistant",value:r.file_name,new_value:r.file_size,icon:"mdi:home-assistant"})),"file_zigbee_size"in r&&(this.isBackupValid=!!r.file_zigbee_name,this.aisBackupFullInfo.push({name:"Zigbee",value:r.file_zigbee_name,new_value:r.file_zigbee_size,icon:"mdi:zigbee"})),t.state}getVersionName(e){var t=e;return"checking"===e?t="Sprawdzanie":"outdated"===e?t="Nieaktualny":"downloading"===e?t="Pobieranie":"installing"===e?t="Instalowanie":"updated"===e?t="Aktualny":"unknown"===e?t="Nieznany":"restart"===e&&(t="Restartowanie"),t}getVersionIcon(e){var t="";return"checking"===e?t="mdi:cloud-sync":"outdated"===e?t="":"downloading"===e?t="mdi:progress-download":"installing"===e?t="mdi:progress-wrench":"updated"===e?t="mdi:emoticon-happy-outline":"unknown"===e?t="mdi:help-circle-outline":"restart"===e&&(t="mdi:restart-alert"),t}_computeAisButtonVersionCheckUpgrade(e){var t=e.states["sensor.version_info"].attributes;return t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt?"outdated"===t.update_status?"Zainstaluj teraz aktualizację":"unknown"===t.update_status?"Spróbuj ponownie":"Aktualizacja -> "+this.getVersionName(t.update_status):"Sprawdź dostępność aktualizacji"}_computeAutoUpdateMode(e){return"off"===e.states["input_boolean.ais_auto_update"].state?(this.aisAutoUpdateIcon="mdi:sync-off",this.aisAutoUpdateInfo="Możesz aktualizować system samodzielnie w dogodnym dla Ciebie czasie lub włączyć aktualizację automatyczną.",!1):(this.aisAutoUpdateIcon="mdi:sync",this.aisAutoUpdateInfo="Codziennie sprawdzimy i automatycznie zainstalujemy dostępne aktualizacje.",!0)}_isEqualTo(e,t){return e===t}changeAutoUpdateMode(){this.hass.callService("input_boolean","toggle",{entity_id:"input_boolean.ais_auto_update"})}doBackup(){if("0"===this.backupStep)this.validating=!0,this.validateLog="",this.hass.callApi("POST","config/core/check_config").then(e=>{this.validating=!1;var t="valid"===e.result?"1":"0";"0"===t?(this.hass.callService("ais_cloud","set_backup_step",{step:t,backup_error:"Konfiguracja niepoprawna"}),this.validateLog=e.errors):(this.hass.callService("ais_cloud","set_backup_step",{step:t,backup_info:"Konfiguracja poprawna można wykonać kopię"}),this.validateLog="")});else{this.validating=!0,this.validateLog="";var e=this.shadowRoot.getElementById("password1").value,t=this.shadowRoot.getElementById("backup_type1").selected;this.hass.callService("ais_cloud","do_backup",{password:e,type:t})}}restoreBackup(){this.validating=!0,this.validateLog="";var e=this.shadowRoot.getElementById("password2").value,t=this.shadowRoot.getElementById("backup_type2").selected;this.hass.callService("ais_cloud","restore_backup",{password:e,type:t})}}customElements.define("ha-config-ais-dom-config-update",n)}}]);
//# sourceMappingURL=chunk.db85ea7f500562dc5b88.js.map