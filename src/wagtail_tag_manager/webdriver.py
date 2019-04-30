from datetime import datetime, timedelta

from selenium import webdriver
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from wagtail_tag_manager.models import Tag, CookieDeclaration


def scan_cookies(request):  # pragma: no cover
    def chop_microseconds(delta):
        return delta - timedelta(microseconds=delta.microseconds)

    try:
        entry_url = request.site.root_page.full_url

        options = webdriver.ChromeOptions()
        options.add_argument("disable-gpu")
        options.add_argument("headless")
        options.add_argument("no-default-browser-check")
        options.add_argument("no-first-run")
        options.add_argument("no-sandbox")

        browser = webdriver.Remote(
            getattr(settings, "WTM_CHROMEDRIVER_URL", "http://0.0.0.0:4444/wd/hub"),
            DesiredCapabilities.CHROME,
            options=options,
        )
        browser.implicitly_wait(30)
        browser.get(entry_url)

        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException as e:
            messages.error(request, e)

        browser.delete_all_cookies()

        browser.add_cookie(
            {
                "name": "wtm",
                "value": "|".join([f"{tag_type}:true" for tag_type in Tag.get_types()]),
                "path": "",
                "secure": False,
            }
        )

        browser.get(entry_url)
        now = datetime.utcnow()

        created = 0
        updated = 0

        for cookie in browser.get_cookies():
            expiry = datetime.fromtimestamp(cookie.get("expiry", now))

            obj, created = CookieDeclaration.objects.update_or_create(
                name=cookie.get("name"),
                domain=cookie.get("domain"),
                defaults={
                    "security": CookieDeclaration.INSECURE_COOKIE
                    if cookie.get("httpOnly")
                    else CookieDeclaration.SECURE_COOKIE,
                    "purpose": _("Unknown"),
                    "duration": chop_microseconds(expiry - now),
                },
            )

            print(obj)

            if created:
                created = created + 1
            else:
                updated = updated + 1

        browser.quit()

        messages.success(
            request, _("Created %d declaration(s) and updated %d." % (created, updated))
        )
    except Exception as e:
        messages.error(request, e)
