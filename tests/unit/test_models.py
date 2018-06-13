import pytest

from wagtail_tag_manager.models import Tag, Constant, Variable


@pytest.mark.django_db
def test_tag_create():
    tag = Tag.objects.create(
        name='functional instant',
        content='<script>console.log("functional instant")</script>')
    assert tag in Tag.objects.all()


@pytest.mark.django_db
def test_constant_create():
    constant = Constant.objects.create(
        name='Constant', key='key', value='value')
    assert constant in Constant.objects.all()


@pytest.mark.django_db
def test_variable_create():
    variable = Variable.objects.create(
        name='Variable', key='key', variable_type='path')
    assert variable in Variable.objects.all()
