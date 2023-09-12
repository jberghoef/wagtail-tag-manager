import Cookies from "js-cookie";

import TagManager from "./components/tag_manager";

import type { Cookie } from "../types";

(function () {
  if (window.wtm === undefined) window.wtm = {};
  (window as any).wtm.consent = () => {
    const cookie = Cookies.get("wtm");
    return JSON.parse(atob(decodeURIComponent(cookie))) as Cookie;
  };

  new TagManager();
})();
