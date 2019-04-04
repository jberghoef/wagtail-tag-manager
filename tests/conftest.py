import pytest
from selenium import webdriver

pytest_plugins = ["tests.fixtures"]


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    from wagtail.core.models import Page, Site

    with django_db_blocker.unblock():
        # Remove some initial data that is brought by the tests.site module
        Site.objects.all().delete()
        Page.objects.all().exclude(depth=1).delete()


@pytest.fixture(scope="module")
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    browser_ = webdriver.Chrome(options=options)
    browser_.implicitly_wait(30)
    browser_.delete_all_cookies()

    yield browser_

    browser_.quit()
