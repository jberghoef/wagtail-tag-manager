import datetime

from selenium import webdriver
from django.conf import settings
from django.contrib import messages
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from wagtail_tag_manager.models import Tag, CookieDeclaration


def set_cookie(response, key, value, days_expire=None):
    if days_expire is None:
        expires = getattr(settings, "WTM_COOKIE_EXPIRE", 365)
        max_age = expires * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60

    delta = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    expires = datetime.datetime.strftime(delta, "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )

    return response


def scan_cookies(request):  # pragma: no cover
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(30)
        browser.get(request.site.root_page.full_url)
        browser.delete_all_cookies()
        for tag in Tag.get_types():
            browser.add_cookie(
                {
                    "name": Tag.get_cookie_name(tag),
                    "value": "true",
                    "path": "",
                    "secure": False,
                }
            )
        browser.get(request.site.root_page.full_url)

        created = 0
        updated = 0

        for cookie in browser.get_cookies():
            obj, created = CookieDeclaration.objects.update_or_create(
                name=cookie.get("name"),
                domain=cookie.get("domain"),
                defaults={
                    "security": CookieDeclaration.INSECURE_COOKIE
                    if cookie.get("httpOnly")
                    else CookieDeclaration.SECURE_COOKIE,
                    "purpose": _("Unknown"),
                },
            )

            if created:
                created = created + 1
            else:
                updated = updated + 1

        browser.quit()

        messages.success(
            request, _("Created %d declaration(s) and updated %d." % (created, updated))
        )
    except NotADirectoryError:
        messages.warning(
            request,
            mark_safe(
                _(
                    "Could not instantiate WebDriver session. Please ensure "
                    "<a href='http://chromedriver.chromium.org/' target='_blank' rel='noopener'>ChromeDriver</a> "
                    "is installed and available in your path."
                )
            ),
        )
    except Exception as e:
        messages.error(request, e)
