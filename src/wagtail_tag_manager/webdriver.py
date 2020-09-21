from datetime import datetime, timedelta

import django
import requests
from selenium import webdriver
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from wagtail_tag_manager.models import Tag, CookieDeclaration

__version__ = django.get_version()
if __version__.startswith("2"):
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _


class CookieScanner(object):  # pragma: no cover
    def __init__(self, request):
        self.request = request
        self.entry_url = request.build_absolute_uri(reverse("wtm:manage"))

        self.created = 0
        self.updated = 0

    def scan(self):
        self.now = datetime.utcnow()
        self.init_browser()

        if hasattr(self, "browser"):
            self.scan_webdriver()
        else:
            self.scan_requests()
            messages.warning(
                self.request,
                _("WebDriver not available. Falling back to GET request method."),
            )

        messages.success(
            self.request,
            _(
                "Created %d declaration(s) and updated %d declaration(s)."
                % (self.created, self.updated)
            ),
        )

    @staticmethod
    def chop_microseconds(delta):
        return delta - timedelta(microseconds=delta.microseconds)

    @property
    def wtm_cookie(self):
        return {
            "name": "wtm",
            "value": "|".join(
                ["{}:true".format(tag_type) for tag_type in Tag.get_types()]
            ),
            "path": "",
            "secure": False,
        }

    @property
    def wtm_debug_cookie(self):
        return {"name": "wtm_debug", "value": "true", "path": "", "secure": False}

    def increment_status(self, created=True):
        if created:
            self.created = self.created + 1
        else:
            self.updated = self.updated + 1

    def init_browser(self):
        chromedriver_url = getattr(settings, "WTM_CHROMEDRIVER_URL", None)
        if chromedriver_url is None:
            return

        options = webdriver.ChromeOptions()
        options.add_argument("disable-gpu")
        options.add_argument("headless")
        options.add_argument("no-default-browser-check")
        options.add_argument("no-first-run")
        options.add_argument("no-sandbox")

        self.browser = webdriver.Remote(
            chromedriver_url,
            DesiredCapabilities.CHROME,
            options=options,
        )
        self.browser.implicitly_wait(30)

    def scan_webdriver(self):
        self.browser.get(self.entry_url)

        try:
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException as e:
            messages.error(self.request, e)

        self.browser.delete_all_cookies()
        self.browser.add_cookie(self.wtm_cookie)
        self.browser.add_cookie(self.wtm_debug_cookie)
        self.browser.get(self.entry_url)

        for cookie in self.browser.get_cookies():
            self.process_webdriver_cookie(cookie)

        self.browser.quit()

    def process_webdriver_cookie(self, cookie):
        expiry = datetime.fromtimestamp(cookie.get("expiry", self.now))

        obj, created = CookieDeclaration.objects.update_or_create(
            name=cookie.get("name"),
            domain=cookie.get("domain"),
            defaults={
                "security": CookieDeclaration.INSECURE_COOKIE
                if cookie.get("httpOnly")
                else CookieDeclaration.SECURE_COOKIE,
                "purpose": _("Unknown"),
                "duration": self.chop_microseconds(expiry - self.now),
            },
        )

        self.increment_status(created)

    def scan_requests(self):
        response = requests.get(
            self.entry_url,
            cookies={
                "wtm": self.wtm_cookie.get("value"),
                "wtm_debug": self.wtm_debug_cookie.get("value"),
            },
        )

        for cookie in response.cookies:
            self.process_requests_cookie(cookie)

    def process_requests_cookie(self, cookie):
        cookie_expires = getattr(cookie, "expires")
        expiry = datetime.fromtimestamp(cookie_expires) if cookie_expires else self.now
        obj, created = CookieDeclaration.objects.update_or_create(
            name=getattr(cookie, "name"),
            domain=getattr(cookie, "domain"),
            defaults={
                "security": CookieDeclaration.SECURE_COOKIE
                if getattr(cookie, "secure", False)
                else CookieDeclaration.INSECURE_COOKIE,
                "purpose": _("Unknown"),
                "duration": self.chop_microseconds(expiry - self.now),
            },
        )

        self.increment_status(created)
