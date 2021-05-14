import pytest
from selenium import webdriver
from django.test.client import RequestFactory as BaseRequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.messages.storage.fallback import FallbackStorage
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from tests.factories.page import ContentPageFactory, TaggableContentPageFactory
from tests.factories.site import SiteFactory


@pytest.fixture(scope="function")
def site():
    try:
        from wagtail.core.models import Locale  # noqa

        from tests.factories.locale import LocaleFactory

        LocaleFactory()
    except:  # noqa: E722
        pass

    root_page = ContentPageFactory(parent=None, slug="")
    site = SiteFactory(is_default_site=True, root_page=root_page)

    page1 = ContentPageFactory(parent=root_page, slug="content-page")
    page2 = TaggableContentPageFactory(parent=root_page, slug="taggable-content-page")
    ContentPageFactory(parent=page1, slug="content-page-child")
    TaggableContentPageFactory(parent=page2, slug="taggable-content-page-child")

    return site


@pytest.fixture()
def rf():
    """RequestFactory instance"""
    return RequestFactory()


class RequestFactory(BaseRequestFactory):
    def request(self, **request):
        request["user"] = None
        request = super(RequestFactory, self).request(**request)
        request.user = AnonymousUser()
        request.session = SessionStore()
        request._messages = FallbackStorage(request)
        return request


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username="user")


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("headless")
    options.add_argument("no-default-browser-check")
    options.add_argument("no-first-run")
    options.add_argument("no-sandbox")

    d = DesiredCapabilities.CHROME
    d["loggingPrefs"] = {"browser": "ALL"}

    driver = webdriver.Chrome(options=options, desired_capabilities=d)
    driver.implicitly_wait(30)

    yield driver
    driver.quit()
