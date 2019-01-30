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
    this.handleDeclarationClick = this.handleDeclarationClick.bind(this);

    if (this.el) {
      this.initialize();
    }
  }

  initialize() {
    const buttons = this.el.querySelectorAll(".js-choice");
    [].forEach.call(buttons, (button: HTMLButtonElement) => {
      button.addEventListener("click", this.handleClick, false);
    });

    const declarationChoices = this.el.querySelectorAll(".js-declaration-choice");
    [].forEach.call(declarationChoices, (a: HTMLAnchorElement) => {
      a.addEventListener("click", this.handleDeclarationClick, false);
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

  handleDeclarationClick(event: MouseEvent) {
    event.preventDefault();

    const target = event.currentTarget as HTMLElement;

    const declarationChoices = this.el.querySelectorAll(".js-declaration-choice");
    [].forEach.call(declarationChoices, (a: HTMLAnchorElement) => {
      if (`${a.getAttribute("href")}` === target.getAttribute("href")) {
        a.classList.add("active");
      } else if (a.classList.contains("active")) {
        a.classList.remove("active");
      }
    });

    const declarationTables = this.el.querySelectorAll(".js-declaration-table");
    [].forEach.call(declarationTables, (table: HTMLTableElement) => {
      if (`#${table.id}` === target.getAttribute("href")) {
        table.classList.remove("hidden");
      } else if (!table.classList.contains("hidden")) {
        table.classList.add("hidden");
      }
    });
  }
}
