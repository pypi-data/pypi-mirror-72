/*! For license information please see chunk.8a1a24e8d44eb55ca1e5.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[186],{120:function(t,e,i){"use strict";i.d(e,"a",function(){return r});i(5);var a=i(6),n=i(4);const r=Object(a.a)({_template:n.a`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},_text:{type:String,value:""}},created:function(){r.instance||(r.instance=this),document.body.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(t){this._text="",this.async(function(){this._text=t},100)},_onIronAnnounce:function(t){t.detail&&t.detail.text&&this.announce(t.detail.text)}});r.instance=null,r.requestAvailability=function(){r.instance||(r.instance=document.createElement("iron-a11y-announcer")),document.body.appendChild(r.instance)}},143:function(t,e,i){"use strict";i(5);var a=i(120),n=i(68),r=i(6),o=i(3),s=i(4);Object(r.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[n.a],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){a.a.requestAvailability(),this._previousValidInput="",this._patternAlreadyChecked=!1},attached:function(){this._observer=Object(o.a)(this).observeNodes(function(t){this._initSlottedInput()}.bind(this))},detached:function(){this._observer&&(Object(o.a)(this).unobserveNodes(this._observer),this._observer=null)},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0],this.inputElement&&this.inputElement.value&&(this.bindValue=this.inputElement.value),this.fire("iron-input-ready")},get _patternRegExp(){var t;if(this.allowedPattern)t=new RegExp(this.allowedPattern);else switch(this.inputElement.type){case"number":t=/[0-9.,e-]/}return t},_bindValueChanged:function(t,e){e&&(void 0===t?e.value=null:t!==e.value&&(this.inputElement.value=t),this.autoValidate&&this.validate(),this.fire("bind-value-changed",{value:t}))},_onInput:function(){this.allowedPattern&&!this._patternAlreadyChecked&&(this._checkPatternValidity()||(this._announceInvalidCharacter("Invalid string of characters not entered."),this.inputElement.value=this._previousValidInput));this.bindValue=this._previousValidInput=this.inputElement.value,this._patternAlreadyChecked=!1},_isPrintable:function(t){var e=8==t.keyCode||9==t.keyCode||13==t.keyCode||27==t.keyCode,i=19==t.keyCode||20==t.keyCode||45==t.keyCode||46==t.keyCode||144==t.keyCode||145==t.keyCode||t.keyCode>32&&t.keyCode<41||t.keyCode>111&&t.keyCode<124;return!(e||0==t.charCode&&i)},_onKeypress:function(t){if(this.allowedPattern||"number"===this.inputElement.type){var e=this._patternRegExp;if(e&&!(t.metaKey||t.ctrlKey||t.altKey)){this._patternAlreadyChecked=!0;var i=String.fromCharCode(t.charCode);this._isPrintable(t)&&!e.test(i)&&(t.preventDefault(),this._announceInvalidCharacter("Invalid character "+i+" not entered."))}}},_checkPatternValidity:function(){var t=this._patternRegExp;if(!t)return!0;for(var e=0;e<this.inputElement.value.length;e++)if(!t.test(this.inputElement.value[e]))return!1;return!0},validate:function(){if(!this.inputElement)return this.invalid=!1,!0;var t=this.inputElement.checkValidity();return t&&(this.required&&""===this.bindValue?t=!1:this.hasValidator()&&(t=n.a.validate.call(this,this.bindValue))),this.invalid=!t,this.fire("iron-input-validate"),t},_announceInvalidCharacter:function(t){this.fire("iron-announce",{text:t})},_computeValue:function(t){return t}})},208:function(t,e,i){"use strict";i.d(e,"a",function(){return r});var a=i(10);const n=new WeakMap,r=Object(a.f)(t=>e=>{const i=n.get(e);if(void 0===t&&e instanceof a.a){if(void 0!==i||!n.has(e)){const t=e.committer.name;e.committer.element.removeAttribute(t)}}else t!==i&&e.setValue(t);n.set(e,t)})},271:function(t,e,i){"use strict";var a=i(1),n=i(0),r=i(122),o=i(53);class s extends n.a{constructor(){super(...arguments),this.mini=!1,this.exited=!1,this.disabled=!1,this.extended=!1,this.showIconAtEnd=!1,this.icon="",this.label=""}createRenderRoot(){return this.attachShadow({mode:"open",delegatesFocus:!0})}render(){const t={"mdc-fab--mini":this.mini,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended,"icon-end":this.showIconAtEnd},e=""!==this.label&&this.extended;let i="";this.icon&&(i=n.f`
        <span class="material-icons mdc-fab__icon">${this.icon}</span>`);let a=n.f``;return e&&(a=n.f`<span class="mdc-fab__label">${this.label}</span>`),n.f`
      <button
          class="mdc-fab ${Object(o.a)(t)}"
          ?disabled="${this.disabled}"
          aria-label="${this.label||this.icon}"
          .ripple="${Object(r.a)()}">
        <div class="mdc-fab__ripple"></div>
        ${this.showIconAtEnd?a:""}
        <slot name="icon">
          ${i}
        </slot>
        ${this.showIconAtEnd?"":a}
      </button>`}}Object(a.b)([Object(n.h)({type:Boolean})],s.prototype,"mini",void 0),Object(a.b)([Object(n.h)({type:Boolean})],s.prototype,"exited",void 0),Object(a.b)([Object(n.h)({type:Boolean})],s.prototype,"disabled",void 0),Object(a.b)([Object(n.h)({type:Boolean})],s.prototype,"extended",void 0),Object(a.b)([Object(n.h)({type:Boolean})],s.prototype,"showIconAtEnd",void 0),Object(a.b)([Object(n.h)()],s.prototype,"icon",void 0),Object(a.b)([Object(n.h)()],s.prototype,"label",void 0);const p=n.c`.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-touch-target-wrapper{display:inline}.mdc-elevation-overlay{position:absolute;border-radius:inherit;opacity:0;pointer-events:none;transition:opacity 280ms cubic-bezier(0.4, 0, 0.2, 1);background-color:#fff}.mdc-fab{position:relative;box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2),0px 6px 10px 0px rgba(0, 0, 0, 0.14),0px 1px 18px 0px rgba(0,0,0,.12);display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1);background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);color:#fff;color:var(--mdc-theme-on-secondary, #fff)}.mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}.mdc-fab:not(.mdc-fab--extended){border-radius:50%}.mdc-fab:not(.mdc-fab--extended) .mdc-fab__ripple{border-radius:50%}.mdc-fab::-moz-focus-inner{padding:0;border:0}.mdc-fab:hover,.mdc-fab:focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}.mdc-fab:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}.mdc-fab:active,.mdc-fab:focus{outline:none}.mdc-fab:hover{cursor:pointer}.mdc-fab>svg{width:100%}.mdc-fab .mdc-fab__icon{width:24px;height:24px;font-size:24px}.mdc-fab--mini{width:40px;height:40px}.mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding:0 20px;width:auto;max-width:100%;height:48px;line-height:normal}.mdc-fab--extended .mdc-fab__ripple{border-radius:24px}.mdc-fab--extended .mdc-fab__icon{margin-left:-8px;margin-right:12px}[dir=rtl] .mdc-fab--extended .mdc-fab__icon,.mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:-8px}.mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:-8px}[dir=rtl] .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,.mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:-8px;margin-right:12px}.mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}.mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;right:0;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}.mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:""}.mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}.mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}.mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}.mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}.mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}.mdc-fab{--mdc-ripple-fg-size: 0;--mdc-ripple-left: 0;--mdc-ripple-top: 0;--mdc-ripple-fg-scale: 1;--mdc-ripple-fg-translate-end: 0;--mdc-ripple-fg-translate-start: 0;-webkit-tap-highlight-color:rgba(0,0,0,0)}.mdc-fab .mdc-fab__ripple::before,.mdc-fab .mdc-fab__ripple::after{position:absolute;border-radius:50%;opacity:0;pointer-events:none;content:""}.mdc-fab .mdc-fab__ripple::before{transition:opacity 15ms linear,background-color 15ms linear;z-index:1}.mdc-fab.mdc-ripple-upgraded .mdc-fab__ripple::before{transform:scale(var(--mdc-ripple-fg-scale, 1))}.mdc-fab.mdc-ripple-upgraded .mdc-fab__ripple::after{top:0;left:0;transform:scale(0);transform-origin:center center}.mdc-fab.mdc-ripple-upgraded--unbounded .mdc-fab__ripple::after{top:var(--mdc-ripple-top, 0);left:var(--mdc-ripple-left, 0)}.mdc-fab.mdc-ripple-upgraded--foreground-activation .mdc-fab__ripple::after{animation:mdc-ripple-fg-radius-in 225ms forwards,mdc-ripple-fg-opacity-in 75ms forwards}.mdc-fab.mdc-ripple-upgraded--foreground-deactivation .mdc-fab__ripple::after{animation:mdc-ripple-fg-opacity-out 150ms;transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}.mdc-fab .mdc-fab__ripple::before,.mdc-fab .mdc-fab__ripple::after{top:calc(50% - 100%);left:calc(50% - 100%);width:200%;height:200%}.mdc-fab.mdc-ripple-upgraded .mdc-fab__ripple::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-fab .mdc-fab__ripple::before,.mdc-fab .mdc-fab__ripple::after{background-color:#fff;background-color:var(--mdc-theme-on-secondary, #fff)}.mdc-fab:hover .mdc-fab__ripple::before{opacity:.08}.mdc-fab.mdc-ripple-upgraded--background-focused .mdc-fab__ripple::before,.mdc-fab:not(.mdc-ripple-upgraded):focus .mdc-fab__ripple::before{transition-duration:75ms;opacity:.24}.mdc-fab:not(.mdc-ripple-upgraded) .mdc-fab__ripple::after{transition:opacity 150ms linear}.mdc-fab:not(.mdc-ripple-upgraded):active .mdc-fab__ripple::after{transition-duration:75ms;opacity:.24}.mdc-fab.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.24}.mdc-fab .mdc-fab__ripple{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden}:host{outline:none}.mdc-fab{box-shadow:var(--mdc-fab-box-shadow, 0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12))}.mdc-fab:hover,.mdc-fab:focus{box-shadow:var(--mdc-fab-box-shadow-hover, 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12))}.mdc-fab:active{box-shadow:var(--mdc-fab-box-shadow-active, 0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12))}.mdc-fab ::slotted([slot=icon]){transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform;display:inline-flex;align-items:center;justify-content:center}.mdc-fab ::slotted([slot=icon]) .mdc-fab__icon{width:24px;height:24px;font-size:24px}.mdc-fab.mdc-fab--extended ::slotted([slot=icon]){margin-left:-8px;margin-right:12px}[dir=rtl] .mdc-fab.mdc-fab--extended ::slotted([slot=icon]),.mdc-fab.mdc-fab--extended ::slotted([slot=icon])[dir=rtl]{margin-left:12px;margin-right:-8px}.mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon,.mdc-fab.mdc-fab--extended.icon-end ::slotted([slot=icon]){margin-left:12px;margin-right:-8px}[dir=rtl] .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon,.mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon[dir=rtl],[dir=rtl] .mdc-fab.mdc-fab--extended.icon-end ::slotted([slot=icon]),.mdc-fab.mdc-fab--extended.icon-end ::slotted([slot=icon])[dir=rtl]{margin-left:-8px;margin-right:12px}.mdc-fab.mdc-fab--exited ::slotted([slot=icon]){transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}`;let c=class extends s{};c.styles=p,c=Object(a.b)([Object(n.d)("mwc-fab")],c)},594:function(t,e,i){"use strict";i(5);var a=i(6);Object(a.a)({is:"app-route",properties:{route:{type:Object,notify:!0},pattern:{type:String},data:{type:Object,value:function(){return{}},notify:!0},autoActivate:{type:Boolean,value:!1},_queryParamsUpdating:{type:Boolean,value:!1},queryParams:{type:Object,value:function(){return{}},notify:!0},tail:{type:Object,value:function(){return{path:null,prefix:null,__queryParams:null}},notify:!0},active:{type:Boolean,notify:!0,readOnly:!0},_matched:{type:String,value:""}},observers:["__tryToMatch(route.path, pattern)","__updatePathOnDataChange(data.*)","__tailPathChanged(tail.path)","__routeQueryParamsChanged(route.__queryParams)","__tailQueryParamsChanged(tail.__queryParams)","__queryParamsChanged(queryParams.*)"],created:function(){this.linkPaths("route.__queryParams","tail.__queryParams"),this.linkPaths("tail.__queryParams","route.__queryParams")},__routeQueryParamsChanged:function(t){if(t&&this.tail){if(this.tail.__queryParams!==t&&this.set("tail.__queryParams",t),!this.active||this._queryParamsUpdating)return;var e={},i=!1;for(var a in t)e[a]=t[a],!i&&this.queryParams&&t[a]===this.queryParams[a]||(i=!0);for(var a in this.queryParams)if(i||!(a in t)){i=!0;break}if(!i)return;this._queryParamsUpdating=!0,this.set("queryParams",e),this._queryParamsUpdating=!1}},__tailQueryParamsChanged:function(t){t&&this.route&&this.route.__queryParams!=t&&this.set("route.__queryParams",t)},__queryParamsChanged:function(t){this.active&&!this._queryParamsUpdating&&this.set("route.__"+t.path,t.value)},__resetProperties:function(){this._setActive(!1),this._matched=null},__tryToMatch:function(){if(this.route){var t=this.route.path,e=this.pattern;if(this.autoActivate&&""===t&&(t="/"),e)if(t){for(var i=t.split("/"),a=e.split("/"),n=[],r={},o=0;o<a.length;o++){var s=a[o];if(!s&&""!==s)break;var p=i.shift();if(!p&&""!==p)return void this.__resetProperties();if(n.push(p),":"==s.charAt(0))r[s.slice(1)]=p;else if(s!==p)return void this.__resetProperties()}this._matched=n.join("/");var c={};this.active||(c.active=!0);var d=this.route.prefix+this._matched,l=i.join("/");for(var u in i.length>0&&(l="/"+l),this.tail&&this.tail.prefix===d&&this.tail.path===l||(c.tail={prefix:d,path:l,__queryParams:this.route.__queryParams}),c.data=r,this._dataInUrl={},r)this._dataInUrl[u]=r[u];this.setProperties?this.setProperties(c,!0):this.__setMulti(c)}else this.__resetProperties()}},__tailPathChanged:function(t){if(this.active){var e=t,i=this._matched;e&&("/"!==e.charAt(0)&&(e="/"+e),i+=e),this.set("route.path",i)}},__updatePathOnDataChange:function(){if(this.route&&this.active){var t=this.__getLink({});t!==this.__getLink(this._dataInUrl)&&this.set("route.path",t)}},__getLink:function(t){var e={tail:null};for(var i in this.data)e[i]=this.data[i];for(var i in t)e[i]=t[i];var a=this.pattern.split("/").map(function(t){return":"==t[0]&&(t=e[t.slice(1)]),t},this);return e.tail&&e.tail.path&&(a.length>0&&"/"===e.tail.path.charAt(0)?a.push(e.tail.path.slice(1)):a.push(e.tail.path)),a.join("/")},__setMulti:function(t){for(var e in t)this._propertySetter(e,t[e]);void 0!==t.data&&(this._pathEffector("data",this.data),this._notifyChange("data")),void 0!==t.active&&(this._pathEffector("active",this.active),this._notifyChange("active")),void 0!==t.tail&&(this._pathEffector("tail",this.tail),this._notifyChange("tail"))}})},76:function(t,e,i){"use strict";i(5),i(143),i(144),i(145),i(146);var a=i(67),n=(i(47),i(6)),r=i(4),o=i(123);Object(n.a)({is:"paper-input",_template:r.a`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id$="[[_inputId]]" maxlength$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" disabled$="[[disabled]]" title$="[[title]]" type$="[[type]]" pattern$="[[pattern]]" required$="[[required]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" min$="[[min]]" max$="[[max]]" step$="[[step]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" list$="[[list]]" size$="[[size]]" autocapitalize$="[[autocapitalize]]" autocorrect$="[[autocorrect]]" on-change="_onChange" tabindex$="[[tabIndex]]" autosave$="[[autosave]]" results$="[[results]]" accept$="[[accept]]" multiple$="[[multiple]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[o.a,a.a],properties:{value:{type:String}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){this.$.nativeInput||(this.$.nativeInput=this.$$("input")),this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)&&(this.alwaysFloatLabel=!0),this.inputElement.bindValue&&this.$.container._handleValueAndAutoValidate(this.inputElement)}})}}]);
//# sourceMappingURL=chunk.8a1a24e8d44eb55ca1e5.js.map