import Cookies from "js-cookie";
import "whatwg-fetch";

import CookieBar from "./cookie_bar";
import TriggerMonitor from "./trigger_monitor";

import { Trigger } from "./trigger_monitor";
import type { WTMWindow, Tag, Meta, Cookie } from "../../types";

export default class TagManager {
  window: WTMWindow = window as WTMWindow;

  configUrl: string;
  lazyUrl: string;

  showCookiebar: boolean;
  requestInit: RequestInit;
  data: { [s: string]: any } = {};
  config: { [s: string]: any } = {};
  meta: Meta = {};
  state: { [s: string]: any } = {};

  constructor() {
    const { body } = document;

    this.configUrl = body.getAttribute("data-wtm-config") || this.window.wtm.config_url;
    this.lazyUrl = body.getAttribute("data-wtm-lazy") || this.window.wtm.lazy_url;

    this.requestInit = {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
      redirect: "follow",
      referrer: "no-referrer",
    };

    this.showCookiebar = false;
    this.initialize();
  }

  initialize() {
    this.loadConfig(() => {
      const cookie = Cookies.get("wtm");
      if (cookie) {
        const { meta, state } = window.wtm.consent() as Cookie;
        this.meta = meta;
        this.state = state;

        this.validate();
        this.loadData(null);
      }
    });
  }

  validate() {
    // Verify the browser allows cookies.
    let enabled = navigator.cookieEnabled;
    if (!enabled) {
      Cookies.set("wtm_verification", "verification");
      enabled = Cookies.get("wtm_verification") !== undefined;
    }

    if (enabled) {
      Object.keys(this.config.tag_types).forEach((tagType) => {
        if (
          this.state[tagType] === "unset" ||
          this.state[tagType] == "none" ||
          this.state[tagType] == "pending"
        ) {
          this.showCookiebar = true;
        }
      });
    }

    if (this.showCookiebar) {
      new CookieBar(this);
    }

    if (this.config.triggers && this.config.triggers.length > 0) {
      const { triggers } = this.config;
      new TriggerMonitor(this, triggers);
    }
  }

  loadConfig(callback?: Function) {
    fetch(this.configUrl, this.requestInit)
      .then((response) => response.json())
      .then((json) => {
        this.config = json;
        if (callback) callback();
      })
      .catch((error) => {
        console.error(error);
      });
  }

  loadData(trigger: Trigger, callback?: Function) {
    fetch(this.lazyUrl, {
      ...this.requestInit,
      method: "POST",
      body: JSON.stringify({ ...window.location, trigger }),
    })
      .then((response) => response.json())
      .then((json) => {
        this.data = json;
        this.handleLoad();
        if (callback) callback();
      })
      .catch((error) => {
        console.error(error);
      });
  }

  handleLoad() {
    this.data.tags.forEach((tag: Tag) => {
      const element = document.createElement(tag.name);
      for (let property in tag.attributes) {
        if (tag.attributes.hasOwnProperty(property)) {
          element.setAttribute(property, tag.attributes[property]);
        }
      }
      element.appendChild(document.createTextNode(tag.string));
      document.head.appendChild(element);
    });
  }
}
