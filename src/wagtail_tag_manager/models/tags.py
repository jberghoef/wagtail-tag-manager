import re

from bs4 import BeautifulSoup
from django.db import models
from django.conf import settings
from django.template import Context, Template
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel

from wagtail_tag_manager.models import constants, variables
from wagtail_tag_manager.managers import TagQuerySet
from wagtail_tag_manager.settings import TagTypeSettings


class Tag(models.Model):
    TOP_HEAD = "0_top_head"
    BOTTOM_HEAD = "1_bottom_head"
    TOP_BODY = "2_top_body"
    BOTTOM_BODY = "3_bottom_body"
    LOCATION_CHOICES = [
        (TOP_HEAD, _("Top of head tag")),
        (BOTTOM_HEAD, _("Bottom of head tag")),
        (TOP_BODY, _("Top of body tag")),
        (BOTTOM_BODY, _("Bottom of body tag")),
    ]

    INSTANT_LOAD = "instant_load"
    LAZY_LOAD = "lazy_load"
    LOAD_CHOICES = [(INSTANT_LOAD, _("Instant")), (LAZY_LOAD, _("Lazy"))]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    auto_load = models.BooleanField(
        default=True,
        help_text=_(
            "Uncheck to disable this tag from being included automatically, "
            "or when using a trigger to include this tag."
        ),
    )
    priority = models.SmallIntegerField(
        default=0,
        help_text=mark_safe(
            _(
                "Define how early on this tag should load as compared to other tags. "
                "A higher number will load sooner. For example:<br/>"
                " - A tag with a priority of 3 will load before a tag with priority 1.<br/>"
                " - A tag with a priority 0 will load before a tag with priority -1.<br/>"
                "<em>Please note that with instanly loading tags, the priority is only "
                "compared to tags that load in the same document location.</em>"
            )
        ),
    )

    tag_type = models.CharField(
        max_length=100,
        choices=[
            (tag_type, config.get("verbose_name"))
            for tag_type, config in TagTypeSettings.all().items()
        ],
        default=list(TagTypeSettings.all())[0],
        help_text=_(
            "The purpose of this tag. Will decide if and when this tag is "
            "loaded on a per-user basis."
        ),
    )
    tag_location = models.CharField(
        max_length=14,
        choices=LOCATION_CHOICES,
        default=TOP_HEAD,
        help_text=_(
            "Where in the document this tag will be inserted. Only applicable "
            "for tags that load instantly."
        ),
    )
    tag_loading = models.CharField(
        max_length=12,
        choices=LOAD_CHOICES,
        default=INSTANT_LOAD,
        help_text=mark_safe(
            _(
                "<b>Instant:</b> include this tag in the document when the initial "
                "request is made.<br/>"
                "<b>Lazy:</b> include this tag after the page has finished loading."
            )
        ),
    )

    content = models.TextField(
        help_text=_(
            "The tag to be added or script to be executed."
            "Will assume the content is a script if no explicit tag has been added."
        )
    )

    objects = TagQuerySet.as_manager()

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("tag_type"),
                FieldRowPanel([FieldPanel("tag_loading"), FieldPanel("tag_location")]),
                FieldPanel("priority"),
                FieldPanel("auto_load"),
            ],
            heading=_("Meta"),
            classname="collapsible",
        ),
        FieldPanel("content", classname="full code"),
    ]

    class Meta:
        ordering = ["tag_loading", "-auto_load", "tag_location", "-priority"]

    def clean(self):
        if not re.match(r"\<.+\/?\>", self.content):
            self.content = f"<script>{self.content}</script>"

        self.content = BeautifulSoup(self.content, "html.parser").prettify()

        try:
            template = Template(self.content)
            template.render(Context())
        except Exception as error:
            raise ValidationError({"content": error})

        return self

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def get_doc(self, request=None, context=None):
        content = self.content

        if request:
            template = Template(content)
            context = Context(Tag.create_context(request, context))
            content = template.render(context)

        return BeautifulSoup(content, "html.parser")

    @classmethod
    def create_context(cls, request, context=None):
        context = context or {}
        if hasattr(context, "flatten"):
            context = context.flatten()

        if not hasattr(request, "wtm_constant_context"):
            request.wtm_constant_context = constants.Constant.create_context()

        if (
            getattr(settings, "WTM_PRESERVE_VARIABLES", True)
            and not hasattr(request, "wtm_variable_context")
            or not getattr(settings, "WTM_PRESERVE_VARIABLES", True)
        ):
            request.wtm_variable_context = variables.Variable.create_context(request)

        return {
            **request.wtm_constant_context,
            **request.wtm_variable_context,
            **context,
        }

    @classmethod
    def get_types(cls):
        return list(TagTypeSettings.all())

    def __str__(self):
        return self.name
