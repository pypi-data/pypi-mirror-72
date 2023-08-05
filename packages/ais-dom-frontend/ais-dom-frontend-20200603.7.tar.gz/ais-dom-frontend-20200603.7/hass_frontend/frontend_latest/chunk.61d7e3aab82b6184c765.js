/*! For license information please see chunk.61d7e3aab82b6184c765.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[28],{157:function(e,t,r){"use strict";r(5);var i=r(67),o=r(68);const n={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},a=[i.a,o.a,n];var s=r(101),l=r(124);r.d(t,"a",function(){return c});const d={_checkedChanged:function(){n._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){l.a._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},c=[s.a,a,d]},178:function(e,t,r){"use strict";r(5),r(46),r(50),r(54);var i=r(6),o=r(4);Object(i.a)({_template:o.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},286:function(e,t,r){"use strict";r(5),r(50),r(46);var i=r(157),o=r(6),n=r(4),a=r(70);const s=n.a`
<style>
  :host {
    display: inline-block;
    line-height: 0;
    white-space: nowrap;
    cursor: pointer;
    @apply --paper-font-common-base;
    --calculated-paper-radio-button-size: var(--paper-radio-button-size, 16px);
    /* -1px is a sentinel for the default and is replace in \`attached\`. */
    --calculated-paper-radio-button-ink-size: var(--paper-radio-button-ink-size, -1px);
  }

  :host(:focus) {
    outline: none;
  }

  #radioContainer {
    @apply --layout-inline;
    @apply --layout-center-center;
    position: relative;
    width: var(--calculated-paper-radio-button-size);
    height: var(--calculated-paper-radio-button-size);
    vertical-align: middle;

    @apply --paper-radio-button-radio-container;
  }

  #ink {
    position: absolute;
    top: 50%;
    left: 50%;
    right: auto;
    width: var(--calculated-paper-radio-button-ink-size);
    height: var(--calculated-paper-radio-button-ink-size);
    color: var(--paper-radio-button-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  #ink[checked] {
    color: var(--paper-radio-button-checked-ink-color, var(--primary-color));
  }

  #offRadio, #onRadio {
    position: absolute;
    box-sizing: border-box;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
  }

  #offRadio {
    border: 2px solid var(--paper-radio-button-unchecked-color, var(--primary-text-color));
    background-color: var(--paper-radio-button-unchecked-background-color, transparent);
    transition: border-color 0.28s;
  }

  #onRadio {
    background-color: var(--paper-radio-button-checked-color, var(--primary-color));
    -webkit-transform: scale(0);
    transform: scale(0);
    transition: -webkit-transform ease 0.28s;
    transition: transform ease 0.28s;
    will-change: transform;
  }

  :host([checked]) #offRadio {
    border-color: var(--paper-radio-button-checked-color, var(--primary-color));
  }

  :host([checked]) #onRadio {
    -webkit-transform: scale(0.5);
    transform: scale(0.5);
  }

  #radioLabel {
    line-height: normal;
    position: relative;
    display: inline-block;
    vertical-align: middle;
    margin-left: var(--paper-radio-button-label-spacing, 10px);
    white-space: normal;
    color: var(--paper-radio-button-label-color, var(--primary-text-color));

    @apply --paper-radio-button-label;
  }

  :host([checked]) #radioLabel {
    @apply --paper-radio-button-label-checked;
  }

  #radioLabel:dir(rtl) {
    margin-left: 0;
    margin-right: var(--paper-radio-button-label-spacing, 10px);
  }

  #radioLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #offRadio {
    border-color: var(--paper-radio-button-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled][checked]) #onRadio {
    background-color: var(--paper-radio-button-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #radioLabel {
    /* slightly darker than the button, so that it's readable */
    opacity: 0.65;
  }
</style>

<div id="radioContainer">
  <div id="offRadio"></div>
  <div id="onRadio"></div>
</div>

<div id="radioLabel"><slot></slot></div>`;s.setAttribute("strip-whitespace",""),Object(o.a)({_template:s,is:"paper-radio-button",behaviors:[i.a],hostAttributes:{role:"radio","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},ready:function(){this._rippleContainer=this.$.radioContainer},attached:function(){Object(a.a)(this,function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-radio-button-ink-size").trim()){var e=parseFloat(this.getComputedStyleValue("--calculated-paper-radio-button-size").trim()),t=Math.floor(3*e);t%2!=e%2&&t++,this.updateStyles({"--paper-radio-button-ink-size":t+"px"})}})}})},318:function(e,t,r){"use strict";r(5),r(38),r(286);var i=r(332),o=r(116),n=r(6),a=r(4);Object(n.a)({_template:a.a`
    <style>
      :host {
        display: inline-block;
      }

      :host ::slotted(*) {
        padding: var(--paper-radio-group-item-padding, 12px);
      }
    </style>

    <slot></slot>
`,is:"paper-radio-group",behaviors:[i.a],hostAttributes:{role:"radiogroup"},properties:{attrForSelected:{type:String,value:"name"},selectedAttribute:{type:String,value:"checked"},selectable:{type:String,value:"paper-radio-button"},allowEmptySelection:{type:Boolean,value:!1}},select:function(e){var t=this._valueToItem(e);if(!t||!t.hasAttribute("disabled")){if(this.selected){var r=this._valueToItem(this.selected);if(this.selected==e){if(!this.allowEmptySelection)return void(r&&(r.checked=!0));e=""}r&&(r.checked=!1)}o.a.select.apply(this,[e]),this.fire("paper-radio-group-changed")}},_activateFocusedItem:function(){this._itemActivate(this._valueForItem(this.focusedItem),this.focusedItem)},_onUpKey:function(e){this._focusPrevious(),e.preventDefault(),this._activateFocusedItem()},_onDownKey:function(e){this._focusNext(),e.preventDefault(),this._activateFocusedItem()},_onLeftKey:function(e){i.b._onLeftKey.apply(this,arguments),this._activateFocusedItem()},_onRightKey:function(e){i.b._onRightKey.apply(this,arguments),this._activateFocusedItem()}})},584:function(e,t,r){"use strict";r.r(t);var i=r(0),o=r(254),n=r(164),a=r(12),s=r(267),l=r(573),d=r(478),c=r(574),p=r(405),h=r(411),u=r(210),f=(r(575),r(576),r(577),r(578),r(579),r(76),r(151));r(218);function y(e){var t,r=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function _(e,t,r){return(_="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=E(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function E(e){return(E=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!v(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=k(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=g(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(b(n.descriptor)||b(o.descriptor)){if(v(n)||v(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(v(n)){if(v(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}m(n,o)}else t.push(n)}return t}(a.d.map(y)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(i.d)("ha-registry-basic-editor")],function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(i.h)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"entry",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_origEntityId",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_entityId",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_disabledBy",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_submitting",value:void 0},{kind:"method",key:"updateEntry",value:async function(){this._submitting=!0;const e={new_entity_id:this._entityId.trim()};null!==this._disabledBy&&"user"!==this._disabledBy||(e.disabled_by=this._disabledBy);try{await Object(s.f)(this.hass,this._origEntityId,e)}finally{this._submitting=!1}}},{kind:"method",key:"updated",value:function(e){_(E(r.prototype),"updated",this).call(this,e),e.has("entry")&&this.entry&&(this._origEntityId=this.entry.entity_id,this._entityId=this.entry.entity_id,this._disabledBy=this.entry.disabled_by)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.entry||this.entry.entity_id!==this._origEntityId)return i.f``;const e=Object(f.a)(this._entityId.trim())!==Object(f.a)(this.entry.entity_id);return i.f`
      <paper-input
        .value=${this._entityId}
        @value-changed=${this._entityIdChanged}
        .label=${this.hass.localize("ui.dialogs.entity_registry.editor.entity_id")}
        error-message="Domain needs to stay the same"
        .invalid=${e}
        .disabled=${this._submitting}
      ></paper-input>
      <div class="row">
        <ha-switch
          .checked=${!this._disabledBy}
          @change=${this._disabledByChanged}
        >
          <div>
            <div>
              ${this.hass.localize("ui.dialogs.entity_registry.editor.enabled_label")}
            </div>
            <div class="secondary">
              ${this._disabledBy&&"user"!==this._disabledBy?this.hass.localize("ui.dialogs.entity_registry.editor.enabled_cause","cause",this.hass.localize(`config_entry.disabled_by.${this._disabledBy}`)):""}
              ${this.hass.localize("ui.dialogs.entity_registry.editor.enabled_description")}
              <br />${this.hass.localize("ui.dialogs.entity_registry.editor.note")}
            </div>
          </div>
        </ha-switch>
      </div>
    `}},{kind:"method",key:"_entityIdChanged",value:function(e){this._entityId=e.detail.value}},{kind:"method",key:"_disabledByChanged",value:function(e){this._disabledBy=e.target.checked?null:"user"}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      .row {
        margin-top: 8px;
        color: var(--primary-text-color);
      }
      .secondary {
        color: var(--secondary-text-color);
      }
    `}}]}},i.a);function O(e){var t,r=A(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function j(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function x(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function P(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function A(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function D(e,t,r){return(D="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=S(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function S(e){return(S=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}r.d(t,"EntityRegistrySettingsHelper",function(){return T});const I={input_boolean:{fetch:l.c,update:l.d,delete:l.b},input_text:{fetch:h.c,update:h.e,delete:h.b},input_number:{fetch:c.c,update:c.d,delete:c.b},input_datetime:{fetch:d.c,update:d.e,delete:d.b},input_select:{fetch:p.c,update:p.e,delete:p.b}};let T=function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!x(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=A(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=P(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=P(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(C(n.descriptor)||C(o.descriptor)){if(x(n)||x(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(x(n)){if(x(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}j(n,o)}else t.push(n)}return t}(a.d.map(O)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(i.d)("entity-settings-helper-tab")],function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(i.h)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"entry",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"dialogElement",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_error",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_item",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_submitting",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_componentLoaded",value:void 0},{kind:"field",decorators:[Object(i.i)("ha-registry-basic-editor")],key:"_registryEditor",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){D(S(r.prototype),"firstUpdated",this).call(this,e),this._componentLoaded=Object(o.a)(this.hass,this.entry.platform)}},{kind:"method",key:"updated",value:function(e){D(S(r.prototype),"updated",this).call(this,e),e.has("entry")&&(this._error=void 0,this._item=void 0,this._getItem())}},{kind:"method",key:"render",value:function(){if(void 0===this._item)return i.f``;const e=this.hass.states[this.entry.entity_id];return i.f`
      <paper-dialog-scrollable .dialogElement=${this.dialogElement}>
        ${this._error?i.f` <div class="error">${this._error}</div> `:""}
        <div class="form">
          ${this._componentLoaded?null===this._item?this.hass.localize("ui.dialogs.helper_settings.yaml_not_editable"):i.f`
                <div @value-changed=${this._valueChanged}>
                  ${Object(n.a)(`ha-${this.entry.platform}-form`,{hass:this.hass,item:this._item,entry:this.entry})}
                </div>
              `:this.hass.localize("ui.dialogs.helper_settings.platform_not_loaded","platform",this.entry.platform)}
          <ha-registry-basic-editor
            .hass=${this.hass}
            .entry=${this.entry}
          ></ha-registry-basic-editor>
        </div>
      </paper-dialog-scrollable>
      <div class="buttons">
        <mwc-button
          class="warning"
          @click=${this._confirmDeleteItem}
          .disabled=${this._submitting||!this._item&&!(null==e?void 0:e.attributes.restored)}
        >
          ${this.hass.localize("ui.dialogs.entity_registry.editor.delete")}
        </mwc-button>
        <mwc-button
          @click=${this._updateItem}
          .disabled=${this._submitting||this._item&&!this._item.name}
        >
          ${this.hass.localize("ui.dialogs.entity_registry.editor.update")}
        </mwc-button>
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(e){this._error=void 0,this._item=e.detail.value}},{kind:"method",key:"_getItem",value:async function(){const e=await I[this.entry.platform].fetch(this.hass);this._item=e.find(e=>e.id===this.entry.unique_id)||null,await this.updateComplete,Object(a.a)(this.dialogElement,"iron-resize")}},{kind:"method",key:"_updateItem",value:async function(){this._submitting=!0;try{var e;this._componentLoaded&&this._item&&await I[this.entry.platform].update(this.hass,this._item.id,this._item),await(null===(e=this._registryEditor)||void 0===e?void 0:e.updateEntry()),Object(a.a)(this,"close-dialog")}catch(t){this._error=t.message||"Unknown error"}finally{this._submitting=!1}}},{kind:"method",key:"_confirmDeleteItem",value:async function(){if(await Object(u.b)(this,{text:this.hass.localize("ui.dialogs.entity_registry.editor.confirm_delete")})){this._submitting=!0;try{if(this._componentLoaded&&this._item)await I[this.entry.platform].delete(this.hass,this._item.id);else{const e=this.hass.states[this.entry.entity_id];if(!(null==e?void 0:e.attributes.restored))return;await Object(s.d)(this.hass,this.entry.entity_id)}Object(a.a)(this,"close-dialog")}finally{this._submitting=!1}}}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        display: block;
        padding: 0 !important;
      }
      .form {
        padding-bottom: 24px;
      }
      .buttons {
        display: flex;
        justify-content: space-between;
        padding: 8px;
        margin-bottom: -20px;
      }
      mwc-button.warning {
        --mdc-theme-primary: var(--google-red-500);
      }
      .error {
        color: var(--google-red-500);
      }
      .row {
        margin-top: 8px;
        color: var(--primary-text-color);
      }
      .secondary {
        color: var(--secondary-text-color);
      }
    `}}]}},i.a)}}]);
//# sourceMappingURL=chunk.61d7e3aab82b6184c765.js.map