import Cookies from 'js-cookie'


class TagManager {
    constructor() {
        this.client = {
            functional: true,
            analytical: false,
            traceable: false
        };

        this.initialize = this.initialize.bind(this);
        this.validate = this.validate.bind(this);
        this.setAnalytical = this.setAnalytical.bind(this);
        this.setTraceable = this.setTraceable.bind(this);
        this.loadData = this.loadData.bind(this);
        this.handleLoad = this.handleLoad.bind(this);

        this.initialize();
    }

    initialize() {
        this.validate();
        this.loadData(this.client);
    }

    validate() {
        let enabled = navigator.cookieEnabled;
        if (!enabled){
            Cookies.set('wtm_verification');
            enabled = Cookies.get('wtm_verification') !== undefined;
        }

        if (enabled) {
            if (!this.hasAnalytical() || !this.hasTraceable()) {
                new CookieBar(this);
            }
            this.setAnalytical(true)
            this.setTraceable(this.isTraceable())
        }
    }

    setAnalytical(value) {
        this.client.analytical = value;
    }

    hasAnalytical() {
        if (window.wtm_analytical) {
            return Cookies.get('wtm_analytical') !== undefined;
        }
        return true
    }

    setTraceable(value) {
        this.client.traceable = value;
    }

    hasTraceable() {
        if (window.wtm_traceable) {
            return Cookies.get('wtm_traceable') !== undefined;
        }
        return true
    }

    isTraceable() {
        if (window.wtm_traceable) {
            return Cookies.get('wtm_traceable') === 'true';
        }
        return false
    }

    loadData(args) {
        const xhttp = new XMLHttpRequest;
        xhttp.onreadystatechange = (event) => {
            if (event.target.readyState === 4 && event.target.status === 200) {
                this.data = JSON.parse(event.target.responseText)
                this.handleLoad()
            }
        }
        xhttp.open("POST", window.wtm_url, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
        xhttp.send(JSON.stringify(args));
    }

    handleLoad() {
        for (let i = 0; i < this.data['tags'].length; i++) {
            let tag = this.data['tags'][i];

            let element = document.createElement(tag.name);
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

        this.initialize();
    }

    initialize() {
        let buttons = this.el.querySelectorAll('.js-cookie-choice');
        for (let button of buttons) {
            button.addEventListener('click', this.handleClick)
        }

        this.showCookieBar();
    }

    showCookieBar() {
        this.el.style.display = 'flex';
    }

    hideCookieBar() {
        this.el.style.display = 'none';
    }

    handleClick(event) {
        event.preventDefault();

        const target = event.currentTarget;
        switch(target.dataset.choice) {
            case 'accept':
                this.manager.setTraceable(true);
                this.manager.loadData({traceable: true});
                break;
            case 'reject':
                this.manager.setTraceable(false);
                Cookies.set('wtm_traceable', false, { expires: 365 })
                break;
        }

        this.hideCookieBar();
    }
}


document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        new TagManager();
    }
};
