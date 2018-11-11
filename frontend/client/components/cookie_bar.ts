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
    this.handleClick = this.handleClick.bind(this);

    if (this.el) {
      this.initialize();
    }
  }

  initialize() {
    const buttons = this.el.querySelectorAll(".js-cookie-choice");
    [].forEach.call(buttons, (button: HTMLButtonElement) => {
      button.addEventListener("click", this.handleClick, false);
    });

    this.showCookieBar();
  }

  showCookieBar() {
    this.el.classList.remove("hidden");
  }

  hideCookieBar() {
    this.el.classList.add("hidden");
  }

  handleClick(event: MouseEvent) {
    event.preventDefault();

    const target = event.currentTarget as HTMLElement;

    switch (target.dataset.choice) {
      case "accept":
        this.manager.loadData(true);
        break;

      case "reject":
        this.manager.loadData(false);
        break;

      default:
        break;
    }

    this.hideCookieBar();
  }
}
