import factory

from wagtail_tag_manager.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    name = "necessary instant"
    content = '<script>console.log("necessary instant")</script>'

    class Meta:
        model = Tag


def tag_instant_necessary(**kwargs):
    return TagFactory(**kwargs)


def tag_instant_preferences(**kwarg):
    return TagFactory(
        name="preferences instant",
        tag_type="preferences",
        content='<script>console.log("preferences instant")</script>',
        **kwarg,
    )


def tag_instant_statistics(**kwarg):
    return TagFactory(
        name="statistics instant",
        tag_type="statistics",
        content='<script>console.log("statistics instant")</script>',
        **kwarg,
    )


def tag_instant_marketing(**kwarg):
    return TagFactory(
        name="marketing instant",
        tag_type="marketing",
        content='<script>console.log("marketing instant")</script>',
        **kwarg,
    )


def tag_lazy_necessary(**kwarg):
    return TagFactory(
        name="necessary lazy",
        tag_loading=Tag.LAZY_LOAD,
        content='<script>console.log("necessary lazy")</script>',
        **kwarg,
    )


def tag_lazy_preferences(**kwarg):
    return TagFactory(
        name="preferences lazy",
        tag_loading=Tag.LAZY_LOAD,
        tag_type="preferences",
        content='<script>console.log("preferences lazy")</script>',
        **kwarg,
    )


def tag_lazy_statistics(**kwarg):
    return TagFactory(
        name="statistics lazy",
        tag_loading=Tag.LAZY_LOAD,
        tag_type="statistics",
        content='<script>console.log("statistics lazy")</script>',
        **kwarg,
    )


def tag_lazy_marketing(**kwarg):
    return TagFactory(
        name="marketing lazy",
        tag_loading=Tag.LAZY_LOAD,
        tag_type="marketing",
        content='<script>console.log("marketing lazy")</script>',
        **kwarg,
    )
