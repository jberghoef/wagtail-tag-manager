import "./index.scss";

class IndexView {
  el: HTMLElement;
  close_el: HTMLAnchorElement;

  constructor() {
    this.el = document.getElementById("wtm_help_block");
    this.close_el = this.el.querySelector("a.close-link");

    this.showHelpBlock = this.showHelpBlock.bind(this);
    this.hideHelpBlock = this.hideHelpBlock.bind(this);
    this.initialize = this.initialize.bind(this);

    this.close_el.addEventListener("click", this.hideHelpBlock);

    if (this.el) {
      this.initialize();
    }
  }

  initialize() {
    if (localStorage.getItem(this.identifier) === null) {
      this.showHelpBlock();
    }
  }

  showHelpBlock() {
    this.el.style.display = "block"
  }

  hideHelpBlock() {
    localStorage.setItem(this.identifier, "hidden");
    this.el.style.display = "none"
  }

  get identifier() {
    return "wtm_help_block:" + location.pathname
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new IndexView();
});
