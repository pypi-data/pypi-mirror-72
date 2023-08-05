/*! For license information please see chunk.50b6fceadded3046daf6.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[122,114],{177:function(t,e,i){"use strict";i(5),i(46),i(54),i(137);var a=i(6),n=i(4),s=i(100);Object(a.a)({_template:n.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[s.a]})},207:function(t,e,i){"use strict";var a=i(9);e.a=Object(a.a)(t=>(class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},215:function(t,e,i){"use strict";i(5),i(77),i(183);var a=i(6),n=i(4),s=i(158);const o=n.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
`;o.setAttribute("strip-whitespace",""),Object(a.a)({_template:o,is:"paper-spinner",behaviors:[s.a]})},220:function(t,e,i){"use strict";i.d(e,"b",function(){return a}),i.d(e,"a",function(){return n});const a=(t,e)=>t<e?-1:t>e?1:0,n=(t,e)=>a(t.toLowerCase(),e.toLowerCase())},230:function(t,e,i){"use strict";i.d(e,"a",function(){return a}),i.d(e,"c",function(){return n}),i.d(e,"b",function(){return s});const a=function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}return!1}(),n=function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}return!1}(),s=function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}return!1}()},233:function(t,e,i){"use strict";i.d(e,"a",function(){return x});var a=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,n="[^\\s]+",s=/\[([^]*?)\]/gm;function o(t,e){for(var i=[],a=0,n=t.length;a<n;a++)i.push(t[a].substr(0,e));return i}var r=function(t){return function(e,i){var a=i[t].map(function(t){return t.toLowerCase()}).indexOf(e.toLowerCase());return a>-1?a:null}};function l(t){for(var e=[],i=1;i<arguments.length;i++)e[i-1]=arguments[i];for(var a=0,n=e;a<n.length;a++){var s=n[a];for(var o in s)t[o]=s[o]}return t}var c=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],d=["January","February","March","April","May","June","July","August","September","October","November","December"],h=o(d,3),u={dayNamesShort:o(c,3),dayNames:c,monthNamesShort:h,monthNames:d,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},p=l({},u),m=function(t,e){for(void 0===e&&(e=2),t=String(t);t.length<e;)t="0"+t;return t},g={D:function(t){return String(t.getDate())},DD:function(t){return m(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return String(t.getDay())},dd:function(t){return m(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return String(t.getMonth()+1)},MM:function(t){return m(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return m(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return m(t.getFullYear(),4)},h:function(t){return String(t.getHours()%12||12)},hh:function(t){return m(t.getHours()%12||12)},H:function(t){return String(t.getHours())},HH:function(t){return m(t.getHours())},m:function(t){return String(t.getMinutes())},mm:function(t){return m(t.getMinutes())},s:function(t){return String(t.getSeconds())},ss:function(t){return m(t.getSeconds())},S:function(t){return String(Math.round(t.getMilliseconds()/100))},SS:function(t){return m(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return m(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+m(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)},Z:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+m(Math.floor(Math.abs(e)/60),2)+":"+m(Math.abs(e)%60,2)}},f=function(t){return+t-1},b=[null,"[1-9]\\d?"],y=[null,n],v=["isPm",n,function(t,e){var i=t.toLowerCase();return i===e.amPm[0]?0:i===e.amPm[1]?1:null}],_=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var e=(t+"").match(/([+-]|\d\d)/gi);if(e){var i=60*+e[1]+parseInt(e[2],10);return"+"===e[0]?i:-i}return 0}],w=(r("monthNamesShort"),r("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"}),x=function(t,e,i){if(void 0===e&&(e=w.default),void 0===i&&(i={}),"number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date pass to format");e=w[e]||e;var n=[];e=e.replace(s,function(t,e){return n.push(e),"@@@"});var o=l(l({},p),i);return(e=e.replace(a,function(e){return g[e](t,o)})).replace(/@@@/g,function(){return n.shift()})}},239:function(t,e,i){"use strict";i.d(e,"d",function(){return a}),i.d(e,"a",function(){return n}),i.d(e,"c",function(){return s}),i.d(e,"b",function(){return o});const a=(t,e)=>e.issue_tracker||`https://github.com/home-assistant/home-assistant/issues?q=is%3Aissue+is%3Aopen+label%3A%22integration%3A+${t}%22`,n=(t,e)=>t(`component.${e}.title`)||e,s=t=>t.callWS({type:"manifest/list"}),o=(t,e)=>t.callWS({type:"manifest/get",integration:e})},240:function(t,e,i){"use strict";i.d(e,"a",function(){return s}),i.d(e,"b",function(){return o});var a=i(233),n=i(230);const s=n.b?(t,e)=>t.toLocaleString(e,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):t=>Object(a.a)(t,"MMMM D, YYYY, HH:mm"),o=n.b?(t,e)=>t.toLocaleString(e,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit"}):t=>Object(a.a)(t,"MMMM D, YYYY, HH:mm:ss")},250:function(t,e,i){"use strict";i(5),i(46);var a=i(6),n=i(3),s=i(4),o=i(159);Object(a.a)({_template:s.a`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[o.a],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return Object(n.a)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),i=document.documentElement.clientWidth-e.right;t.style.left=e.left+"px",t.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(i.marginTop=e+"px",i.paddingTop=""):(i.paddingTop=e+"px",i.marginTop="")}}})},257:function(t,e,i){"use strict";i.d(e,"a",function(){return s}),i.d(e,"b",function(){return o});var a=i(233),n=i(230);const s=n.c?(t,e)=>t.toLocaleTimeString(e,{hour:"numeric",minute:"2-digit"}):t=>Object(a.a)(t,"shortTime"),o=n.c?(t,e)=>t.toLocaleTimeString(e,{hour:"numeric",minute:"2-digit",second:"2-digit"}):t=>Object(a.a)(t,"mediumTime")},270:function(t,e,i){"use strict";i.d(e,"b",function(){return n}),i.d(e,"a",function(){return s});const a=/^(\w+)\.(\w+)$/,n=t=>a.test(t),s=t=>t.toLowerCase().replace(/\s|'/g,"_").replace(/\W/g,"").replace(/_{2,}/g,"_").replace(/_$/,"")},279:function(t,e,i){"use strict";i.d(e,"a",function(){return n});var a=i(270);const n=t=>{if(!t||!Array.isArray(t))throw new Error("Entities need to be an array");return t.map((t,e)=>{if("object"==typeof t&&!Array.isArray(t)&&t.type)return t;let i;if("string"==typeof t)i={entity:t};else{if("object"!=typeof t||Array.isArray(t))throw new Error(`Invalid entity specified at position ${e}.`);if(!t.entity)throw new Error(`Entity object at position ${e} is missing entity field.`);i=t}if(!Object(a.b)(i.entity))throw new Error(`Invalid entity ID at position ${e}: ${i.entity}`);return i})}},312:function(t,e,i){"use strict";i.d(e,"a",function(){return o}),i.d(e,"b",function(){return r}),i.d(e,"d",function(){return l}),i.d(e,"g",function(){return c}),i.d(e,"h",function(){return d}),i.d(e,"c",function(){return h}),i.d(e,"e",function(){return u}),i.d(e,"f",function(){return g}),i.d(e,"j",function(){return f}),i.d(e,"i",function(){return b});var a=i(19),n=i(61),s=i(239);const o=["unignore","homekit","ssdp","zeroconf"],r=(t,e)=>{var i;return t.callApi("POST","config/config_entries/flow",{handler:e,show_advanced_options:Boolean(null===(i=t.userData)||void 0===i?void 0:i.showAdvanced)})},l=(t,e)=>t.callApi("GET",`config/config_entries/flow/${e}`),c=(t,e,i)=>t.callApi("POST",`config/config_entries/flow/${e}`,i),d=(t,e)=>t.callWS({type:"config_entries/ignore_flow",flow_id:e}),h=(t,e)=>t.callApi("DELETE",`config/config_entries/flow/${e}`),u=t=>t.callApi("GET","config/config_entries/flow_handlers"),p=t=>t.sendMessagePromise({type:"config_entries/flow/progress"}),m=(t,e)=>t.subscribeEvents(Object(n.a)(()=>p(t).then(t=>e.setState(t,!0)),500,!0),"config_entry_discovered"),g=t=>Object(a.b)(t,"_configFlowProgress",p,m),f=(t,e)=>g(t.connection).subscribe(e),b=(t,e)=>{const i=e.context.title_placeholders||{},a=Object.keys(i);if(0===a.length)return Object(s.a)(t,e.handler);const n=[];return a.forEach(t=>{n.push(t),n.push(i[t])}),t(`component.${e.handler}.config.flow_title`,...n)}},317:function(t,e,i){"use strict";i.d(e,"a",function(){return n}),i.d(e,"b",function(){return s});var a=i(12);const n=()=>Promise.all([i.e(0),i.e(1),i.e(2),i.e(3),i.e(50)]).then(i.bind(null,377)),s=(t,e,i)=>{Object(a.a)(t,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:Object.assign({},e,{flowConfig:i})})}},321:function(t,e,i){"use strict";i.d(e,"a",function(){return c}),i.d(e,"b",function(){return d});var a=i(0),n=i(220),s=i(78),o=i(312),r=i(239),l=i(317);const c=l.a,d=(t,e)=>Object(l.b)(t,e,{loadDevicesAndAreas:!0,getFlowHandlers:async t=>{const[e]=await Promise.all([Object(o.e)(t),t.loadBackendTranslation("title",void 0,!0)]);return e.sort((e,i)=>Object(n.a)(Object(r.a)(t.localize,e),Object(r.a)(t.localize,i)))},createFlow:async(t,e)=>{const[i]=await Promise.all([Object(o.b)(t,e),t.loadBackendTranslation("config",e)]);return i},fetchFlow:async(t,e)=>{const i=await Object(o.d)(t,e);return await t.loadBackendTranslation("config",i.handler),i},handleFlowStep:o.g,deleteFlow:o.c,renderAbortDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.abort.${e.reason}`,e.description_placeholders);return i?a.f`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(t,e)=>t.localize(`component.${e.handler}.config.step.${e.step_id}.title`)||t.localize(`component.${e.handler}.title`),renderShowFormStepDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.step.${e.step_id}.description`,e.description_placeholders);return i?a.f`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(t,e,i)=>t.localize(`component.${e.handler}.config.step.${e.step_id}.data.${i.name}`),renderShowFormStepFieldError:(t,e,i)=>t.localize(`component.${e.handler}.config.error.${i}`),renderExternalStepHeader:(t,e)=>t.localize(`component.${e.handler}.config.step.${e.step_id}.title`),renderExternalStepDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.${e.step_id}.description`,e.description_placeholders);return a.f`
        <p>
          ${t.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?a.f`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(t,e){const i=Object(s.b)(t.localize,`component.${e.handler}.config.create_entry.${e.description||"default"}`,e.description_placeholders);return a.f`
        ${i?a.f`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
        <p>
          ${t.localize("ui.panel.config.integrations.config_flow.created_config","name",e.title)}
        </p>
      `}})},337:function(t,e,i){"use strict";i(215);var a=i(4),n=i(31),s=i(207),o=i(22),r=i(240),l=i(128),c=(i(140),i(89)),d=i(13),h=i(257);let u=null;customElements.define("ha-chart-base",class extends(Object(c.b)([l.a],n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        ha-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=(()=>{this._debouncer=o.a.debounce(this._debouncer,d.d.after(10),()=>{this._isAttached&&this.resizeChart()})}),"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver(t=>{t.forEach(()=>{this._resizeListener()})}),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===u&&(u=Promise.all([i.e(178),i.e(98)]).then(i.bind(null,757))),u.then(t=>{this.ChartClass=t.default,this.onPropsChange()})}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(t){if(0===t.opacity)return void this.set(["tooltip","opacity"],0);t.yAlign?this.set(["tooltip","yAlign"],t.yAlign):this.set(["tooltip","yAlign"],"no-transform");const e=t.title&&t.title[0]||"";this.set(["tooltip","title"],e);const i=t.body.map(t=>t.lines);t.body&&this.set(["tooltip","lines"],i.map((e,i)=>{const a=t.labelColors[i];return{color:a.borderColor,bgColor:a.backgroundColor,text:e.join("\n")}}));const a=this.$.chartTarget.clientWidth;let n=t.caretX;const s=this._chart.canvas.offsetTop+t.caretY;t.caretX+100>a?n=a-100:t.caretX<100&&(n=100),n+=this._chart.canvas.offsetLeft,this.tooltip=Object.assign({},this.tooltip,{opacity:1,left:`${n}px`,top:`${s}px`})}_legendClick(t){(t=t||window.event).stopPropagation();let e=t.target||t.srcElement;for(;"LI"!==e.nodeName;)e=e.parentElement;const i=t.model.itemsIndex,a=this._chart.getDatasetMeta(i);a.hidden=null===a.hidden?!this._chart.data.datasets[i].hidden:null,this.set(["metas",i,"hidden"],this._chart.isDatasetVisible(i)?null:"hidden"),this._chart.update()}_drawLegend(){const t=this._chart,e=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map((i,a)=>({label:i.label,color:i.color,bgColor:i.backgroundColor,hidden:e&&a<this.metas.length?this.metas[a].hidden:!t.isDatasetVisible(a)})));let i=!1;if(e)for(let a=0;a<this.metas.length;a++){const e=t.getDatasetMeta(a);!!e.hidden!=!!this.metas[a].hidden&&(i=!0),e.hidden=!!this.metas[a].hidden||null}i&&t.update(),this.unit=this.data.unit}_formatTickValue(t,e,i){if(0===i.length)return t;const a=new Date(i[e].value);return Object(h.a)(a)}drawChart(){const t=this.data.data,e=this.$.chartCanvas;if(t.datasets&&t.datasets.length||this._chart){if("timeline"!==this.data.type&&t.datasets.length>0){const e=t.datasets.length,i=this.constructor.getColorList(e);for(let a=0;a<e;a++)t.datasets[a].borderColor=i[a].rgbString(),t.datasets[a].backgroundColor=i[a].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=t,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=t.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!t.datasets)return;this._customTooltips({opacity:0});const i=[{afterRender:()=>this._setRendered(!0)}];let a={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};(a=Chart.helpers.merge(a,this.data.options)).scales.xAxes[0].ticks.callback=this._formatTickValue,"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(a.elements.colorFunction=this._colorFunc),1===t.datasets.length&&(a.scales.yAxes[0].ticks?a.scales.yAxes[0].ticks.display=!1:a.scales.yAxes[0].ticks={display:!1},a.scales.yAxes[0].gridLines?a.scales.yAxes[0].gridLines.display=!1:a.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const n={type:this.data.type,data:this.data.data,options:a,plugins:i};this._chart=new this.ChartClass(e,n),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const t=this.$.chartTarget,e=this.data.data;if(0===e.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const i=this._chart.chartArea.top,a=this._chart.chartArea.bottom,n=this._chart.canvas.clientHeight;if(a>0&&(this._axisHeight=n-a+i),!this._axisHeight)return t.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const i=30*e.datasets.length+this._axisHeight+"px";t.style.height!==i&&(t.style.height=i),this._chart.resize()}}static getColorList(t){let e=!1;t>10&&(e=!0,t=Math.ceil(t/2));const i=360/t,a=[];for(let n=0;n<t;n++)a[n]=Color().hsl(i*n,80,38),e&&(a[n+t]=Color().hsl(i*n,80,62));return a}static getColorGenerator(t,e){const i=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function a(t){return Color("#"+i[t%i.length])}const n={};let s=0;return e>0&&(s=e),t&&Object.keys(t).forEach(e=>{const i=t[e];isFinite(i)?n[e.toLowerCase()]=a(i):n[e.toLowerCase()]=Color(t[e])}),function(t,e){let i;const o=e[3];if(null===o)return Color().hsl(0,40,38);if(void 0===o)return Color().hsl(120,40,38);const r=o.toLowerCase();return void 0===i&&(i=n[r]),void 0===i&&(i=a(s),s++,n[r]=i),i}}});customElements.define("state-history-chart-line",class extends(Object(s.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}_onRenderedChanged(t){t&&this.animateHeight()}animateHeight(){requestAnimationFrame(()=>requestAnimationFrame(()=>{this.style.height=this.$.chart.scrollHeight+"px"}))}drawChart(){const t=this.unit,e=this.data,i=[];let a;if(!this._isAttached)return;if(0===e.length)return;function n(t){const e=parseFloat(t);return isFinite(e)?e:null}(a=this.endTime||new Date(Math.max.apply(null,e.map(t=>new Date(t.states[t.states.length-1].last_changed)))))>new Date&&(a=new Date);const s=this.names||{};e.forEach(e=>{const o=e.domain,r=s[e.entity_id]||e.name;let l;const c=[];function d(t,e){e&&(t>a||(c.forEach((i,a)=>{i.data.push({x:t,y:e[a]})}),l=e))}function h(e,i,a){let n=!1,s=!1;a&&(n="origin"),i&&(s="before"),c.push({label:e,fill:n,steppedLine:s,pointRadius:0,data:[],unitText:t})}if("thermostat"===o||"climate"===o||"water_heater"===o){const t=e.states.some(t=>t.attributes&&t.attributes.hvac_action),i="climate"===o&&t?t=>"heating"===t.attributes.hvac_action:t=>"heat"===t.state,a="climate"===o&&t?t=>"cooling"===t.attributes.hvac_action:t=>"cool"===t.state,s=e.states.some(i),l=e.states.some(a),c=e.states.some(t=>t.attributes&&t.attributes.target_temp_high!==t.attributes.target_temp_low);h(`${this.hass.localize("ui.card.climate.current_temperature","name",r)}`,!0),s&&h(`${this.hass.localize("ui.card.climate.heating","name",r)}`,!0,!0),l&&h(`${this.hass.localize("ui.card.climate.cooling","name",r)}`,!0,!0),c?(h(`${this.hass.localize("ui.card.climate.target_temperature_mode","name",r,"mode",this.hass.localize("ui.card.climate.high"))}`,!0),h(`${this.hass.localize("ui.card.climate.target_temperature_mode","name",r,"mode",this.hass.localize("ui.card.climate.low"))}`,!0)):h(`${this.hass.localize("ui.card.climate.target_temperature_entity","name",r)}`,!0),e.states.forEach(t=>{if(!t.attributes)return;const e=n(t.attributes.current_temperature),o=[e];if(s&&o.push(i(t)?e:null),l&&o.push(a(t)?e:null),c){const e=n(t.attributes.target_temp_high),i=n(t.attributes.target_temp_low);o.push(e,i),d(new Date(t.last_changed),o)}else{const e=n(t.attributes.temperature);o.push(e),d(new Date(t.last_changed),o)}})}else{h(r,"sensor"===o);let t=null,i=null,a=null;e.states.forEach(e=>{const s=n(e.state),o=new Date(e.last_changed);if(null!==s&&null!==a){const e=o.getTime(),n=a.getTime(),r=i.getTime();d(a,[(n-r)/(e-r)*(s-t)+t]),d(new Date(n+1),[null]),d(o,[s]),i=o,t=s,a=null}else null!==s&&null===a?(d(o,[s]),i=o,t=s):null===s&&null===a&&null!==t&&(a=o)})}d(a,l),Array.prototype.push.apply(i,c)});const o={type:"line",unit:t,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(t,e)=>{const i=t[0],a=e.datasets[i.datasetIndex].data[i.index].x;return Object(r.b)(a,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:i}};this.chartData=o}});var p=i(126);customElements.define("state-history-chart-timeline",class extends(Object(s.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let t=this.data;if(!this._isAttached)return;t||(t=[]);const e=new Date(t.reduce((t,e)=>Math.min(t,new Date(e.data[0].last_changed)),new Date));let i=this.endTime||new Date(t.reduce((t,e)=>Math.max(t,new Date(e.data[e.data.length-1].last_changed)),e));i>new Date&&(i=new Date);const a=[],n=[],s=this.names||{};t.forEach(t=>{let o,r=null,l=null,c=e;const d=s[t.entity_id]||t.name,h=[];t.data.forEach(t=>{let e=t.state;void 0!==e&&""!==e||(e=null),new Date(t.last_changed)>i||(null!==r&&e!==r?(o=new Date(t.last_changed),h.push([c,o,l,r]),r=e,l=t.state_localize,c=o):null===r&&(r=e,l=t.state_localize,c=new Date(t.last_changed)))}),null!==r&&h.push([c,i,l,r]),n.push({data:h}),a.push(d)});const o={type:"timeline",options:{tooltips:{callbacks:{label:(t,e)=>{const i=e.datasets[t.datasetIndex].data[t.index],a=Object(r.b)(i[0],this.hass.language),n=Object(r.b)(i[1],this.hass.language);return[i[2],a,n]}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:t=>{t.maxWidth=.18*t.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:a,datasets:n},colors:{staticColors:{on:1,off:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=o}_computeRTL(t){return Object(p.a)(t)}});customElements.define("state-history-charts",class extends(Object(s.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          /* height of single timeline chart = 58px */
          min-height: 58px;
        }
        .info {
          text-align: center;
          line-height: 58px;
          color: var(--secondary-text-color);
        }
      </style>
      <template
        is="dom-if"
        class="info"
        if="[[_computeIsLoading(isLoadingData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.loading_history')]]
        </div>
      </template>

      <template
        is="dom-if"
        class="info"
        if="[[_computeIsEmpty(isLoadingData, historyData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.no_history_found')]]
        </div>
      </template>

      <template is="dom-if" if="[[historyData.timeline.length]]">
        <state-history-chart-timeline
          hass="[[hass]]"
          data="[[historyData.timeline]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          no-single="[[noSingle]]"
          names="[[names]]"
        ></state-history-chart-timeline>
      </template>

      <template is="dom-repeat" items="[[historyData.line]]">
        <state-history-chart-line
          hass="[[hass]]"
          unit="[[item.unit]]"
          data="[[item.data]]"
          identifier="[[item.identifier]]"
          is-single-device="[[_computeIsSingleLineChart(item.data, noSingle)]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          names="[[names]]"
        ></state-history-chart-line>
      </template>
    `}static get properties(){return{hass:Object,historyData:{type:Object,value:null},names:Object,isLoadingData:Boolean,endTime:{type:Object},upToNow:Boolean,noSingle:Boolean}}_computeIsSingleLineChart(t,e){return!e&&t&&1===t.length}_computeIsEmpty(t,e){const i=!e||!e.timeline||!e.line||0===e.timeline.length&&0===e.line.length;return!t&&i}_computeIsLoading(t){return t&&!this.historyData}_computeEndTime(t,e){return e?new Date:t}})},762:function(t,e,i){"use strict";i.r(e);i(255),i(182);var a=i(4),n=i(31),s=(i(184),i(129),i(354),i(321)),o=i(12),r=(i(337),i(279));customElements.define("ha-config-ais-dom-config-wifi",class extends n.a{static get template(){return a.a`
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
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-icon-button {
          vertical-align: middle;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button on-click="showLocalIpInfo"
                      >[[aisLocalHostName]]</mwc-button
                    ><ha-icon-button
                      class="user-button"
                      icon="hass:settings"
                      on-click="createFlowHostName"
                    ></ha-icon-button>
                  </div>
                </div>
                <div on-click="showLocalIpInfo" style="text-align: center;">
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisLocalIP]]</mwc-button>
                  </div>
                </div>
                <div on-click="showWiFiSpeedInfo" style="text-align: center;">
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisWiFiSpeed]]</mwc-button>
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:wifi"
                    on-click="showWiFiGroup"
                  ></ha-icon-button
                  ><mwc-button on-click="createFlowWifi"
                    >Konfigurator połączenia z siecą WiFi</mwc-button
                  >
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,aisLocalHostName:{type:String,computed:"_computeAisLocalHostName(hass)"},aisLocalIP:{type:String,computed:"_computeAisLocalIP(hass)"},aisWiFiSpeed:{type:String,computed:"_computeAisWiFiSpeed(hass)"},_config:Object,_names:Object,_entities:Array,_cacheConfig:Object}}computeClasses(t){return t?"content":"content narrow"}_computeAisLocalHostName(t){return t.states["sensor.local_host_name"].state}_computeAisLocalIP(t){return t.states["sensor.internal_ip_address"].state}_computeAisWiFiSpeed(t){return t.states["sensor.ais_wifi_service_current_network_info"].state}showWiFiGroup(){Object(o.a)(this,"hass-more-info",{entityId:"group.internet_status"})}showWiFiSpeedInfo(){Object(o.a)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}showLocalIpInfo(){Object(o.a)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}_continueFlow(t){Object(s.b)(this,{continueFlowId:t,dialogClosedCallback:()=>{console.log("OK")}})}createFlowHostName(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then(t=>{this._continueFlow(t.flow_id)})}createFlowWifi(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then(t=>{console.log(t),this._continueFlow(t.flow_id)})}ready(){super.ready();const t=Object(r.a)(["sensor.ais_wifi_service_current_network_info"]),e=[],i={};for(const a of t)e.push(a.entity),a.name&&(i[a.entity]=a.name);this.setProperties({_cacheConfig:{cacheKey:e.join(),hoursToShow:24,refresh:0},_entities:e,_names:i})}})}}]);
//# sourceMappingURL=chunk.50b6fceadded3046daf6.js.map