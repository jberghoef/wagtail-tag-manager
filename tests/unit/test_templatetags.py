import pytest

from tests.factories.tag import (
    tag_instant_functional, tag_instant_analytical, tag_instant_traceable)

from wagtail_tag_manager.models import TagTypeSettings
from wagtail_tag_manager.templatetags.wtm_tags import (
    wtm_instant_tags, wtm_lazy_manager, wtm_cookie_bar)


@pytest.mark.django_db
def test_wtm_instant_tags(rf):
    tag_instant_functional()
    tag_instant_analytical()
    tag_instant_traceable()

    request = rf.get('/')

    context = wtm_instant_tags({'request': request})
    assert 'tags' in context
    assert len(context.get('tags')) == 1

    request.COOKIES = {
        'wtm_functional': 'true',
        'wtm_analytical': 'true'}
    context = wtm_instant_tags({'request': request})
    assert 'tags' in context
    assert len(context.get('tags')) == 2

    request.COOKIES = {
        'wtm_functional': 'true',
        'wtm_analytical': 'true',
        'wtm_traceable': 'true'}
    context = wtm_instant_tags({'request': request})
    assert 'tags' in context
    assert len(context.get('tags')) == 3


@pytest.mark.django_db
def test_wtm_lazy_manager():
    context = wtm_lazy_manager()

    assert 'config' in context
    print(context.get('config'))
    assert context.get('config') == TagTypeSettings.all()


@pytest.mark.django_db
def test_wtm_cookie_bar():
    context = wtm_cookie_bar()

    assert 'manage_view' in context
    assert context.get('manage_view') is True
