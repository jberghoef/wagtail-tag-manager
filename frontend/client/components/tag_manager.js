import Cookies from "js-cookie";
import CookieBar from "./cookie_bar";

export default class TagManager {
  constructor() {
    this.config = window.wtm_config;
    this.show_cookiebar = false;

    this.initialize();
  }

  initialize() {
    this.validate();
    this.loadData();
  }

  validate() {
    // Verify the browser allows cookies.
    let enabled = navigator.cookieEnabled;
    if (!enabled) {
      Cookies.set("wtm_verification");
      enabled = Cookies.get("wtm_verification") !== undefined;
    }

    if (enabled) {
      Object.keys(this.config).forEach(tagType => {
        if (this.config[tagType] === "initial" && !this.has(tagType)) {
          Cookies.set(`wtm_${tagType}`, "unset", { expires: 365 });
          this.show_cookiebar = true;
        } else if (!this.has(tagType)) {
          this.show_cookiebar = true;
        }
      });
    }

    if (this.show_cookiebar) {
      new CookieBar(this);
    }
  }

  has(type) {
    if (type in this.config) {
      return Cookies.get(`wtm_${type}`) !== undefined;
    }
    return true;
  }

  loadData(consent = undefined) {
    fetch(window.wtm_url, {
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
      .then(response => {
        return response.json();
      })
      .then(json => {
        this.data = json;
        this.handleLoad();
      });
  }

  handleLoad() {
    for (let i = 0; i < this.data["tags"].length; i++) {
      const tag = this.data["tags"][i];

      const element = document.createElement(tag.name);
      element.appendChild(document.createTextNode(tag.string));
      document.head.appendChild(element);
    }
  }
}
