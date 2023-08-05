/*! For license information please see chunk.ded9894a4eb8bea69e52.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[116,114],{177:function(t,e,a){"use strict";a(5),a(46),a(54),a(137);var o=a(6),i=a(4),r=a(100);Object(o.a)({_template:i.a`
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
`,is:"paper-icon-item",behaviors:[r.a]})},207:function(t,e,a){"use strict";var o=a(9);e.a=Object(o.a)(t=>(class extends t{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(t){return t}}))},250:function(t,e,a){"use strict";a(5),a(46);var o=a(6),i=a(3),r=a(4),n=a(159);Object(o.a)({_template:r.a`
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
`,is:"app-header-layout",behaviors:[n.a],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return Object(i.a)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),a=document.documentElement.clientWidth-e.right;t.style.left=e.left+"px",t.style.right=a+"px"}.bind(this));var a=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(a.marginTop=e+"px",a.paddingTop=""):(a.paddingTop=e+"px",a.marginTop="")}}})},763:function(t,e,a){"use strict";a.r(e);a(255),a(182);var o=a(4),i=a(31),r=(a(184),a(129),a(354),a(207));customElements.define("ha-config-ais-dom-config-display",class extends(Object(r.a)(i.a)){static get template(){return o.a`
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
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
        .buttons {
          position: relative;
          width: 200px;
          height: 200px;
        }

        .button {
          position: absolute;
          width: 50px;
          height: 50px;
        }

        .arrow {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        .arrow-up {
          border-left: 12px solid transparent;
          border-right: 12px solid transparent;
          border-bottom: 16px solid black;
        }

        .arrow-right {
          border-top: 12px solid transparent;
          border-bottom: 12px solid transparent;
          border-left: 16px solid black;
        }

        .arrow-left {
          border-top: 12px solid transparent;
          border-bottom: 12px solid transparent;
          border-right: 16px solid black;
        }

        .arrow-down {
          border-left: 12px solid transparent;
          border-right: 12px solid transparent;
          border-top: 16px solid black;
        }

        .down {
          bottom: 0;
          left: 75px;
        }

        .left {
          top: 75px;
          left: 0;
        }

        .right {
          top: 75px;
          right: 0;
        }

        .up {
          top: 0;
          left: 75px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Ustawienia ekranu</span>
            <span slot="introduction"
              >Jeżeli obraz na monitorze lub telewizorze podłączonym do bramki
              za pomocą złącza HDMI jest ucięty lub przesunięty, to w tym
              miejscu możesz dostosować obraz do rozmiaru ekranu.</span
            >
            <ha-card header="Dostosuj obraz do rozmiaru ekranu">
              <div class="card-content">
                <div class="card-content" style="text-align: center;">
                  <div style="display: inline-block;">
                    <p>Powiększanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table; border:solid 1px;"
                    >
                      <button
                        class="button up"
                        data-value="top"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button down"
                        data-value="bottom"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="right"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="left"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                    </div>
                  </div>
                  <div
                    style="text-align: center; display: inline-block; margin: 30px;"
                  >
                    <p>Zmniejszanie</p>
                    <div
                      class="buttons"
                      style="margin: 0 auto; display: table;"
                    >
                      <button
                        class="button up"
                        data-value="-top"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-down arrow"></span>
                      </button>
                      <div
                        style="margin: 0 auto; height: 98px; width:98px; margin-top: 50px; margin-left: 50px; display: flex; border:solid 1px;"
                      ></div>
                      <button
                        class="button down"
                        data-value="-bottom"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-up arrow"></span>
                      </button>
                      <button
                        class="button right"
                        data-value="-right"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-left arrow"></span>
                      </button>
                      <button
                        class="button left"
                        data-value="-left"
                        on-click="wmOverscan"
                      >
                        <span class="arrow-right arrow"></span>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="card-actions" style="margin-top: 30px;">
                  <div>
                    <ha-icon-button
                      class="user-button"
                      icon="mdi:restore"
                      on-click="wmRestoreSettings"
                    ></ha-icon-button
                    ><mwc-button on-click="wmOverscan" data-value="reset"
                      >Reset ekranu do ustawień domyślnych</mwc-button
                    >
                  </div>
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean}}ready(){super.ready()}wmOverscan(t){this.hass.callService("ais_shell_command","change_wm_overscan",{value:t.currentTarget.getAttribute("data-value")})}})}}]);
//# sourceMappingURL=chunk.ded9894a4eb8bea69e52.js.map