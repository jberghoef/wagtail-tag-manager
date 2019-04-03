import factory

from wagtail_tag_manager.models import Tag


class TagFactory(factory.DjangoModelFactory):
    name = "functional instant"
    content = '<script>console.log("functional instant")</script>'

    class Meta:
        model = Tag


def tag_instant_functional(**kwargs):
    return TagFactory(**kwargs)


def tag_instant_analytical(**kwarg):
    return TagFactory(
        name="analytical instant",
        tag_type="analytical",
        content='<script>console.log("analytical instant")</script>',
        **kwarg,
    )


def tag_instant_delayed(**kwarg):
    return TagFactory(
        name="delayed instant",
        tag_type="delayed",
        content='<script>console.log("delayed instant")</script>',
        **kwarg,
    )


def tag_instant_traceable(**kwarg):
    return TagFactory(
        name="traceable instant",
        tag_type="traceable",
        content='<script>console.log("traceable instant")</script>',
        **kwarg,
    )


def tag_lazy_functional(**kwarg):
    return TagFactory(
        name="functional lazy",
        tag_loading=Tag.LAZY_LOAD,
        content='<script>console.log("functional lazy")</script>',
        **kwarg,
    )


def tag_lazy_analytical(**kwarg):
    return TagFactory(
        name="analytical lazy",
        tag_loading=Tag.LAZY_LOAD,
        tag_type="analytical",
        content='<script>console.log("analytical lazy")</script>',
        **kwarg,
    )


def tag_lazy_delayed(**kwarg):
    return TagFactory(
        name="delayed lazy",
        tag_loading=Tag.LAZY_LOAD,
        tag_type="delayed",
        content='<script>console.log("delayed lazy")</script>',
        **kwarg,
    )


def tag_lazy_traceable(**kwarg):
    return TagFactory(
        name="traceable lazy",
        tag_loading=Tag.LAZY_LOAD,
        tag_type="traceable",
        content='<script>console.log("traceable lazy")</script>',
        **kwarg,
    )
