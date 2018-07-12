import Cookies from 'js-cookie'


class TagManager {
    constructor() {
        this._history = [];
        this.client = {
            functional: true,
            analytical: undefined,
            traceable: undefined,
        };

        this.initialize();
    }

    initialize() {
        this.validate();
        this.loadData();
    }

    validate() {
        // Verify the browser allows cookies.
        let enabled = navigator.cookieEnabled;
        if (!enabled){
            Cookies.set('wtm_verification');
            enabled = Cookies.get('wtm_verification') !== undefined;
        }

        if (enabled) {
            if (!this.has('analytical')) {
                // Cookies are enabled and no preference is set.
                // Analytical cookies can be used until stated otherwise.
                this.set('analytical', true);
            }

            if (!this.has('analytical') || !this.has('traceable')) {
                new CookieBar(this);
            }

            // Set remaining states from cookies.
            for (let key in this.client) {
                if (!this.client[key]) this.set(key, this.allows(key));
            }
        }
    }

    set(type, value) {
        this.client[type] = value;
    }

    has(type) {
        if (window[`wtm_${type}`]) {
            return Cookies.get(`wtm_${type}`) !== undefined;
        }
        return true
    }

    allows(type) {
        if (window[`wtm_${type}`]) {
            if (this.has(type)) {
                return Cookies.get(`wtm_${type}`) === 'true';
            } else {
                return undefined
            }
        }
        return false
    }

    loadData() {
        // Only send changed values.
        let data = {};
        for (let key in this.client) {
            if (this._history.length === 0) {
                // For the initial load, only send `true` values.
                if (this.client[key]) data[key] = this.client[key];
            } else {
                // Otherwise, only send values that differ from the previous load.
                const previous = this._history[this._history.length - 1];
                if (this.client[key] !== previous[key]) data[key] = this.client[key];
            }
        }

        this._history.push({...this.client});

        const xhttp = new XMLHttpRequest;
        xhttp.onreadystatechange = (event) => {
            if (event.target.readyState === 4 && event.target.status === 200) {
                this.data = JSON.parse(event.target.responseText);
                this.handleLoad();
            }
        };
        xhttp.open("POST", window.wtm_url, true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));

        if (Object.keys(data).length > 0) xhttp.send(JSON.stringify(data));
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
        const buttons = this.el.querySelectorAll('.js-cookie-choice');
        for (let button of buttons) {
            button.addEventListener('click', this.handleClick, false);
        }

        this.showCookieBar();
    }

    showCookieBar() {
        this.el.style.display = 'block';
    }

    hideCookieBar() {
        this.el.style.display = 'none';
    }

    handleClick(event) {
        event.preventDefault();

        switch(event.currentTarget.dataset.choice) {
            case 'accept':
                this.manager.set('analytical', true);
                this.manager.set('traceable', true);
                this.manager.loadData();
                break;

            case 'reject':
                this.manager.set('analytical', false);
                this.manager.set('traceable', false);
                this.manager.loadData();
                break;

            default:
                break;
        }

        this.hideCookieBar();
    }
}


document.onreadystatechange = () => {
    if (document.readyState === "complete") {
        new TagManager();
    }
};
