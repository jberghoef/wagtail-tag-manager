import * as Cookies from "js-cookie";
import "whatwg-fetch";
import CookieBar from "./cookie_bar";

interface WTMWindow extends Window {
  wtm: {
    state_url: string;
    lazy_url: string;
  };
}

interface Tag {
  name: string;
  attributes: {
    [s: string]: string;
  };
  string: string;
}

export default class TagManager {
  window: WTMWindow = window as WTMWindow;

  stateUrl: string;
  lazyUrl: string;

  showCookiebar: boolean;
  data: { [s: string]: any };
  config: { [s: string]: any };

  constructor() {
    const { body } = document;

    this.stateUrl = body.getAttribute("data-wtm-state") || this.window.wtm.state_url;
    this.lazyUrl = body.getAttribute("data-wtm-lazy") || this.window.wtm.lazy_url;

    this.showCookiebar = false;
    this.initialize();
  }

  initialize() {
    this.loadState(() => {
      this.validate();
      this.loadData();
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
      Object.keys(this.config).forEach(tagType => {
        if (Cookies.get(`wtm_${tagType}`) === "unset" || !this.has(tagType)) {
          this.showCookiebar = true;
        }
      });
    }

    if (this.showCookiebar) {
      new CookieBar(this);
    }
  }

  has(type: string) {
    if (type in this.config) {
      return Cookies.get(`wtm_${type}`) !== undefined;
    }
    return true;
  }

  loadState(callback?: Function) {
    fetch(this.stateUrl, {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json; charset=utf-8"
      },
      redirect: "follow",
      referrer: "no-referrer"
    })
      .then(response => response.json())
      .then(json => {
        this.config = json;
        if (callback) callback();
      });
  }

  loadData(callback?: Function) {
    fetch(this.lazyUrl, {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": Cookies.get("csrftoken")
      },
      redirect: "follow",
      referrer: "no-referrer",
      body: JSON.stringify({ ...window.location })
    })
      .then(response => response.json())
      .then(json => {
        this.data = json;
        this.handleLoad();
        if (callback) callback();
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
