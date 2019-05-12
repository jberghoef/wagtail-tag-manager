import TagManager from "./tag_manager";

const CLICK_ALL_ELEMENTS = "click_all_elements";
const CLICK_SOME_ELEMENTS = "click_some_elements";
const VISIBILITY_ONCE_PER_PAGE = "visibility_once_per_page";
const VISIBILITY_ONCE_PER_ELEMENT = "visibility_once_per_element";
const VISIBILITY_RECURRING = "visibility_recurring";
const FORM_SUBMIT = "form_submit";
const HISTORY_CHANGE = "history_change";
const JAVASCRIPT_ERROR = "javascript_error";
const SCROLL_VERTICAL = "scroll_vertical";
const SCROLL_HORIZONTAL = "scroll_horizontal";
const TIMER_TIMEOUT = "timer_timeout";
const TIMER_INTERVAL = "timer_interval";

export interface Trigger {
  slug: string;
  type: string;
  value: any;
}

export interface TriggerableHTMLElement extends HTMLElement {
  wtm: { [key: string]: boolean };
}

export default class TriggerMonitor {
  manager: TagManager;
  triggers: [Trigger];
  wtm: { [key: string]: boolean };

  constructor(manager: TagManager, triggers: [Trigger]) {
    this.manager = manager;
    this.triggers = triggers;
    this.wtm = {};

    this.initialize = this.initialize.bind(this);

    this.initialize();
  }

  initialize() {
    for (const trigger of this.triggers) {
      switch (trigger.type) {
        case CLICK_ALL_ELEMENTS:
        case CLICK_SOME_ELEMENTS:
          this.bindClickListener(trigger);
          break;
        case VISIBILITY_ONCE_PER_PAGE:
        case VISIBILITY_ONCE_PER_ELEMENT:
        case VISIBILITY_RECURRING:
          this.bindVisibilityListener(trigger);
          break;
        case FORM_SUBMIT:
          this.bindFormSubmitListener(trigger);
          break;
        case HISTORY_CHANGE:
          this.bindHistoryChangeListener(trigger);
          break;
        case JAVASCRIPT_ERROR:
          this.bindErrorListener(trigger);
          break;
        case SCROLL_VERTICAL:
        case SCROLL_HORIZONTAL:
          this.bindScrollListener(trigger);
          break;
        case TIMER_TIMEOUT:
        case TIMER_INTERVAL:
          this.bindTimerListener(trigger);
          break;
        default:
          console.error(`trigger type '${trigger.type}' not implemented.`);
          break;
      }
    }
  }

  bindClickListener(trigger: Trigger) {
    const handleEvent = (event: MouseEvent) => {
      event.stopPropagation();
      const target = event.target as HTMLElement;
      this.sendTrigger(trigger, this.createElementID(target));
    };

    if (trigger.type === CLICK_ALL_ELEMENTS) {
      document.addEventListener("click", handleEvent);
    } else if (trigger.type === CLICK_SOME_ELEMENTS) {
      [].forEach.call(document.querySelectorAll(trigger.value), (element: HTMLElement) => {
        element.addEventListener("click", handleEvent);
      });
    }
  }

  bindVisibilityListener(trigger: Trigger) {
    const handleEvent = (event: Event) => {
      [].forEach.call(
        document.querySelectorAll(trigger.value),
        (element: TriggerableHTMLElement) => {
          const rect = element.getBoundingClientRect();
          const in_view =
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth);

          if (in_view) {
            if (trigger.type === VISIBILITY_ONCE_PER_PAGE && !this.wtm[trigger.slug]) {
              this.wtm[trigger.slug] = true;
              this.sendTrigger(trigger, this.createElementID(element));
            } else if (trigger.type === VISIBILITY_ONCE_PER_ELEMENT && !element.wtm[trigger.slug]) {
              element.wtm[trigger.slug] = true;
              this.sendTrigger(trigger, this.createElementID(element));
            } else if (trigger.type === VISIBILITY_RECURRING && !element.wtm[trigger.slug]) {
              element.wtm[trigger.slug] = true;
              this.sendTrigger(trigger, this.createElementID(element));
            }
          } else if (trigger.type === VISIBILITY_RECURRING) {
            element.wtm[trigger.slug] = false;
          }
        }
      );
    };

    window.addEventListener("load", handleEvent, { passive: true });
    document.addEventListener("scroll", handleEvent, { passive: true });
    document.addEventListener("resize", handleEvent, { passive: true });
  }

  bindFormSubmitListener(trigger: Trigger) {
    const handleEvent = (event: Event) => {
      event.preventDefault();
      const target = event.target as HTMLFormElement;
      this.sendTrigger(trigger, this.createElementID(target));
      target.submit();
    };

    [].forEach.call(document.querySelectorAll("form"), (element: HTMLElement) => {
      element.addEventListener("submit", handleEvent, { passive: true });
    });
  }

  bindHistoryChangeListener(trigger: Trigger) {
    const handleEvent = (event: PopStateEvent) => {
      this.sendTrigger(trigger, event.type);
    };

    window.addEventListener("popstate", handleEvent);
  }

  bindErrorListener(trigger: Trigger) {
    const handleEvent = (event: ErrorEvent) => {
      this.sendTrigger(trigger, event.message);
    };
    window.addEventListener("error", handleEvent);
  }

  bindScrollListener(trigger: Trigger) {
    const handleEvent = () => {
      let scrollPercentage = -1000;
      if (trigger.type === SCROLL_VERTICAL) {
        scrollPercentage = this.yScrollPercentage;
      } else if (trigger.type === SCROLL_HORIZONTAL) {
        scrollPercentage = this.xScrollPercentage;
      }

      if (scrollPercentage >= trigger.value && !this.wtm[trigger.slug]) {
        this.wtm[trigger.slug] = true;
        this.sendTrigger(trigger, scrollPercentage);
      } else if (scrollPercentage < trigger.value) {
        this.wtm[trigger.slug] = false;
      }
    };

    document.addEventListener("scroll", handleEvent, { passive: true });
  }

  bindTimerListener(trigger: Trigger) {
    const handleEvent = () => {
      const now = new Date();
      this.sendTrigger(trigger, now.toISOString());
    };

    if (trigger.type === TIMER_TIMEOUT) {
      window.setTimeout(handleEvent, trigger.value);
    } else if (trigger.type === TIMER_INTERVAL) {
      window.setInterval(handleEvent, trigger.value);
    }
  }

  sendTrigger(trigger: Trigger, value: string | number) {
    trigger.value = value;
    this.manager.loadData(trigger);
  }

  get yScrollPercentage() {
    const distance = document.documentElement["scrollTop"] || document.body["scrollTop"];
    const offset =
      (document.documentElement["scrollHeight"] || document.body["scrollHeight"]) -
      document.documentElement.clientHeight;
    return (distance / offset) * 100;
  }

  get xScrollPercentage() {
    const distance = document.documentElement["scrollLeft"] || document.body["scrollLeft"];
    const offset =
      (document.documentElement["scrollWidth"] || document.body["scrollWidth"]) -
      document.documentElement.clientHeight;
    return (distance / offset) * 100;
  }

  createElementID(el: HTMLElement) {
    const tag = el.tagName.toLowerCase();
    const ids: [string?] = [];
    const classes: [string?] = [];
    const attributes: [string?] = [];

    [].forEach.call(el.attributes, (attr: any) => {
      const { name, value } = attr;
      switch (name) {
        case "id":
          for (let part of value.split(" ")) {
            if (part) ids.push(`#${part}`);
          }
          break;
        case "class":
          for (let part of value.split(" ")) {
            if (part) classes.push(`.${part}`);
          }
          break;
        default:
          attributes.push(`[${name}=${value}]`);
          break;
      }
    });

    return tag + ids.join("") + classes.join("") + attributes.join("");
  }
}
