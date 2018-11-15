import pytest

from wagtail_tag_manager.utils import scan_cookies


@pytest.mark.django_db
def test_scan_cookies(rf, site):
    request = rf.get(site.root_page.url)
    scan_cookies(request)
