(self.webpackJsonp=self.webpackJsonp||[]).push([[130],{236:function(e,t,a){"use strict";a(46);var l=a(54);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${l.b.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(n.content)},755:function(e,t,a){"use strict";a.r(t);a(181);var l=a(4),n=a(31);a(160),a(236);class o extends n.a{static get template(){return l.a`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          position: absolute;
          height: calc(100% - 64px);
          background-color: var(--primary-background-color);
        }
      </style>
      <app-toolbar>
        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{hass:Object,narrow:Boolean,panel:Object}}}customElements.define("ha-panel-iframe",o)}}]);
//# sourceMappingURL=chunk.8320eb042179262d17b0.js.map