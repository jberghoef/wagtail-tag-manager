import "./cookie_bar.scss";

import TagManager from "./tag_manager";

export default class CookieBar {
  manager: TagManager;
  el: HTMLElement;

  constructor(manager: TagManager) {
    this.manager = manager;
    this.el = document.getElementById("wtm_cookie_bar");

    this.initialize = this.initialize.bind(this);
    this.showCookieBar = this.showCookieBar.bind(this);
    this.hideCookieBar = this.hideCookieBar.bind(this);

    if (this.el) {
      this.initialize();
    }
  }

  initialize() {
    this.showCookieBar();
  }

  showCookieBar() {
    this.el.classList.remove("hidden");
  }

  hideCookieBar() {
    this.el.classList.add("hidden");
  }
}
