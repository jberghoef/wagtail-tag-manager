import Cookies from 'js-cookie';


class TagManager {
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
      Cookies.set('wtm_verification');
      enabled = Cookies.get('wtm_verification') !== undefined;
    }

    if (enabled) {
      Object.keys(this.config).forEach((tagType) => {
        if (this.config[tagType] === 'initial' && !this.has(tagType)) {
          Cookies.set(`wtm_${tagType}`, 'unset', { expires: 365 });
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
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = (event) => {
      if (event.target.readyState === 4 && event.target.status === 200) {
        this.data = JSON.parse(event.target.responseText);
        this.handleLoad();
      }
    };
    xhttp.open('POST', window.wtm_url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));

    xhttp.send(JSON.stringify({ consent: consent }));
  }

  handleLoad() {
    for (let i = 0; i < this.data['tags'].length; i++) {
      const tag = this.data['tags'][i];

      const element = document.createElement(tag.name);
      element.appendChild(document.createTextNode(tag.string));
      document.head.appendChild(element);
    }
  }
}


class CookieBar {
  constructor(manager) {
    this.manager = manager;
    this.el = document.getElementById('wtm_cookie_bar');

    this.initialize = this.initialize.bind(this);
    this.showCookieBar = this.showCookieBar.bind(this);
    this.hideCookieBar = this.hideCookieBar.bind(this);
    this.handleClick = this.handleClick.bind(this);

    if (this.el) {
      this.initialize();
    }
  }

  initialize() {
    const buttons = this.el.querySelectorAll('.js-cookie-choice');
    for (let button of buttons) {
      button.addEventListener('click', this.handleClick, false);
    }

    this.showCookieBar();
  }

  showCookieBar() {
    this.el.classList.remove('hidden');
  }

  hideCookieBar() {
    this.el.classList.add('hidden');
  }

  handleClick(event) {
    event.preventDefault();

    switch (event.currentTarget.dataset.choice) {
      case 'accept':
        this.manager.loadData(true);
        break;

      case 'reject':
        this.manager.loadData(false);
        break;

      default:
        break;
    }

    this.hideCookieBar();
  }
}


document.onreadystatechange = () => {
  if (document.readyState === 'complete') {
    new TagManager();
  }
};
