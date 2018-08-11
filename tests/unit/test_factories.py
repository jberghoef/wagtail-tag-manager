import pytest

from tests.factories.tag import (
    TagFactory, tag_lazy_traceable, tag_lazy_analytical, tag_lazy_functional,
    tag_instant_traceable, tag_instant_analytical, tag_instant_functional)
from tests.factories.constant import ConstantFactory
from tests.factories.variable import VariableFactory
from wagtail_tag_manager.models import Tag, Constant, Variable


@pytest.mark.django_db
def test_tag_create():
    produced_tag = TagFactory()
    tag = Tag(
        name='functional instant',
        content='<script>console.log("functional instant")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_tag_instant_functional():
    produced_tag = tag_instant_functional()
    tag = Tag(
        name='functional instant',
        content='<script>console.log("functional instant")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_tag_instant_analytical():
    produced_tag = tag_instant_analytical()
    tag = Tag(
        name='analytical instant',
        tag_type='analytical',
        content='<script>console.log("analytical instant")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_tag_instant_traceable():
    produced_tag = tag_instant_traceable()
    tag = Tag(
        name='traceable instant',
        tag_type='traceable',
        content='<script>console.log("traceable instant")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_tag_lazy_functional():
    produced_tag = tag_lazy_functional()
    tag = Tag(
        name='functional lazy',
        content='<script>console.log("functional lazy")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_tag_lazy_analytical():
    produced_tag = tag_lazy_analytical()
    tag = Tag(
        name='analytical lazy',
        tag_type='analytical',
        content='<script>console.log("analytical lazy")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_tag_lazy_traceable():
    produced_tag = tag_lazy_traceable()
    tag = Tag(
        name='traceable lazy',
        tag_type='traceable',
        content='<script>console.log("traceable lazy")</script>')

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == tag.content


@pytest.mark.django_db
def test_constant_create():
    produced_constant = ConstantFactory()
    constant = Constant(name='Constant', key='key', value='value')

    assert produced_constant.name == constant.name
    assert produced_constant.key == constant.key
    assert produced_constant.value == constant.value


@pytest.mark.django_db
def test_variable_create():
    produced_variable = VariableFactory()
    variable = Variable(
        name='Variable', key='key', variable_type='path', value='value')

    assert produced_variable.name == variable.name
    assert produced_variable.key == variable.key
    assert produced_variable.variable_type == variable.variable_type
    assert produced_variable.value == variable.value
