import Cookies from "js-cookie";
import CookieBar from "./cookie_bar";

export default class TagManager {
  constructor() {
    const { body } = document;
    this.state_url = body.getAttribute("data-wtm-state") || window.wtm.state_url;
    this.lazy_url = body.getAttribute("data-wtm-lazy") || window.wtm.lazy_url;

    this.show_cookiebar = false;
    this.initialize();
  }

  initialize() {
    fetch(this.state_url, {
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
      Cookies.set("wtm_verification");
      enabled = Cookies.get("wtm_verification") !== undefined;
    }

    if (enabled) {
      Object.keys(this.config).forEach(tagType => {
        if (this.config[tagType] === "initial" && !this.has(tagType)) {
          Cookies.set(`wtm_${tagType}`, "unset", { expires: 365 });
          this.show_cookiebar = true;
        } else if (Cookies.get(`wtm_${tagType}`) == "unset" || !this.has(tagType)) {
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
    fetch(this.lazy_url, {
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
    for (let i = 0; i < this.data["tags"].length; i++) {
      const tag = this.data["tags"][i];

      const element = document.createElement(tag.name);
      element.appendChild(document.createTextNode(tag.string));
      document.head.appendChild(element);
    }
  }
}
