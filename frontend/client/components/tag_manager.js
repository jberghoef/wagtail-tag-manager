import Cookies from "js-cookie";
import CookieBar from "./cookie_bar";

export default class TagManager {
  constructor() {
    const { body } = document;
    this.stateUrl = body.getAttribute("data-wtm-state") || window.wtm.state_url;
    this.lazyUrl = body.getAttribute("data-wtm-lazy") || window.wtm.lazy_url;

    this.showCookiebar = false;
    this.initialize();
  }

  initialize() {
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
        if (this.config[tagType] === "initial" && !this.has(tagType)) {
          Cookies.set(`wtm_${tagType}`, "unset", { expires: 365 });
          this.showCookiebar = true;
        } else if (Cookies.get(`wtm_${tagType}`) === "unset" || !this.has(tagType)) {
          this.showCookiebar = true;
        }
      });
    }

    if (this.showCookiebar) {
      this.cookieBar = new CookieBar(this);
    }
  }

  has(type) {
    if (type in this.config) {
      return Cookies.get(`wtm_${type}`) !== undefined;
    }
    return true;
  }

  loadData(consent = undefined) {
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
      body: JSON.stringify({
        consent,
        ...window.location
      })
    })
      .then(response => response.json())
      .then(json => {
        this.data = json;
        this.handleLoad();
      });
  }

  handleLoad() {
    this.data.tags.forEach(tag => {
      const element = document.createElement(tag.name);
      element.appendChild(document.createTextNode(tag.string));
      document.head.appendChild(element);
    });
  }
}
