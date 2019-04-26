import re
import random
import operator

from bs4 import BeautifulSoup
from django.db import models
from django.conf import settings
from django.forms import widgets
from django.dispatch import receiver
from django.template import Context, Template
from django.core.cache import cache
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel

from wagtail_tag_manager.decorators import get_variables
from wagtail_tag_manager.managers import (
    TagQuerySet,
    TriggerQuerySet,
    CookieDeclarationQuerySet,
)
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
            request.wtm_constant_context = Constant.create_context()

        if (
            getattr(settings, "WTM_PRESERVE_VARIABLES", True)
            and not hasattr(request, "wtm_variable_context")
            or not getattr(settings, "WTM_PRESERVE_VARIABLES", True)
        ):
            request.wtm_variable_context = Variable.create_context(request)

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


class Constant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    key = models.SlugField(
        max_length=255,
        unique=True,
        help_text=mark_safe(
            _(
                "The key that can be used in tags to include the value.<br/>"
                "For example: <code>{{ ga_id }}</code>."
            )
        ),
    )
    value = models.CharField(
        max_length=255,
        help_text=_("The value to be rendered when this constant is included."),
    )

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("key"), FieldPanel("value")])], heading=_("Data")
        ),
    ]

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "key": self.key,
            "value": self.value,
        }

    def get_value(self):
        return self.value

    @classmethod
    def create_context(cls):
        context = cache.get("wtm_constant_cache", {})

        if not context:
            for constant in cls.objects.all():
                context[constant.key] = constant.get_value()

            timeout = getattr(settings, "WTM_CACHE_TIMEOUT", 60 * 30)
            cache.set("wtm_constant_cache", context, timeout)

        return context

    def clean(self):
        if Variable.objects.filter(key=self.key).exists():
            raise ValidationError(
                f"A variable with the key '{ self.key }' already exists."
            )
        else:
            super().clean()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Constant)
def handle_constant_save(sender, **kwargs):
    sender.create_context()  # Update the cache


class Variable(models.Model):
    TYPE_CHOICES = (
        (_("HTTP"), (("path", _("Path")), ("_repath+", _("Path with regex")))),
        (_("User"), (("user.pk", _("User")), ("session.session_key", _("Session")))),
        (_("Wagtail"), (("site", _("Site")),)),
        (_("Other"), (("_cookie+", _("Cookie")), ("_random", _("Random number")))),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    key = models.SlugField(
        max_length=255,
        unique=True,
        help_text=mark_safe(
            _(
                "The key that can be used in tags to include the value.<br/>"
                "For example: <code>{{ path }}</code>."
            )
        ),
    )
    variable_type = models.CharField(
        max_length=255,
        choices=TYPE_CHOICES,
        help_text=mark_safe(
            _(
                "<b>Path:</b> the path of the visited page.<br/>"
                "<b>Path with regex:</b> the path of the visited page after "
                "applying a regex search.<br/>"
                "<b>User:</b> the ID of a user, when available.<br/>"
                "<b>Session:</b> the session key.<br/>"
                "<b>Site:</b> the name of the site.<br/>"
                "<b>Cookie:</b> the value of a cookie, when available.<br/>"
                "<b>Random number:</b> a random number."
            )
        ),
    )
    value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=mark_safe(
            _(
                "<b>Path with regex:</b> the pattern to search the path with.<br/>"
                "<b>Cookie:</b> the name of the cookie."
            )
        ),
    )

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("key"), FieldPanel("variable_type")]),
                FieldPanel("value"),
            ],
            heading=_("Data"),
        ),
    ]

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "key": self.key,
            "variable_type": self.variable_type,
            "value": self.value,
        }

    def get_repath(self, request):
        path = getattr(request, "path", None)
        if path and self.value:
            regex = re.compile(self.value)
            match = regex.search(request.get_full_path())
            if match:
                return match.group()
            return ""
        return path

    def get_cookie(self, request):
        if request and hasattr(request, "COOKIES"):
            return request.COOKIES.get(self.value, "")
        return ""

    def get_random(self, request):
        return int(random.random() * 2_147_483_647)

    def get_value(self, request):
        variable_type = self.variable_type

        if variable_type.endswith("+"):
            variable_type = variable_type[:-1]

        if variable_type.startswith("_"):
            method = getattr(self, f"get{variable_type}")
            return method(request)

        if "." in self.variable_type:
            return operator.attrgetter(str(self.variable_type))(request)

        return getattr(request, str(self.variable_type))

    @classmethod
    def create_context(cls, request):
        context = {}

        for variable in [*get_variables(), *cls.objects.all()]:
            context[variable.key] = variable.get_value(request)

        return context

    def clean(self):
        if Constant.objects.filter(key=self.key).exists():
            raise ValidationError(
                f"A constant with the key '{ self.key }' already exists."
            )
        else:
            super().clean()

            if not self.variable_type.endswith("+"):
                self.value = ""

            return self

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


def searchable_regex_validator(value):
    try:
        re.search(value, "")
    except re.error:
        raise ValidationError(
            "The pattern {pattern} is not valid".format(pattern=value)
        )


class Trigger(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(
        default=True, help_text=_("Uncheck to disable this trigger from firing.")
    )
    pattern = models.CharField(
        max_length=255,
        help_text=_(
            "The regex pattern to match the full url path with. "
            "Groups will be added to the included tag's context."
        ),
        validators=[searchable_regex_validator],
    )
    tags = models.ManyToManyField(
        Tag, help_text=_("The tags to include when this trigger is fired.")
    )

    objects = TriggerQuerySet.as_manager()

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [FieldPanel("pattern"), FieldPanel("active")], heading=_("Configuration")
        ),
        FieldPanel("tags", widget=widgets.CheckboxSelectMultiple),
    ]

    def match(self, request):
        if request:
            return re.search(self.pattern, request.get_full_path())
        return False

    def __str__(self):
        return self.name


class CookieDeclaration(models.Model):
    INSECURE_COOKIE = "http"
    SECURE_COOKIE = "https"
    SECURITY_CHOICES = ((INSECURE_COOKIE, _("HTTP")), (SECURE_COOKIE, _("HTTPS")))

    cookie_type = models.CharField(
        max_length=10,
        choices=[
            (tag_type, config.get("verbose_name"))
            for tag_type, config in TagTypeSettings.all().items()
        ],
        help_text=_("The type of functionality this cookie supports."),
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, help_text=_("The name of this cookie."))
    domain = models.CharField(
        max_length=255,
        help_text=mark_safe(
            _(
                "The domain (including subdomain if applicable) of the cookie.<br/>"
                "For example: <code>.wagtail.io</code>."
            )
        ),
    )
    purpose = models.TextField(help_text=_("What this cookie is being used for."))
    duration = models.DurationField(null=True, blank=True)
    security = models.CharField(
        max_length=5,
        choices=SECURITY_CHOICES,
        default=INSECURE_COOKIE,
        help_text=_("Whether this cookie is secure or not."),
    )

    objects = CookieDeclarationQuerySet.as_manager()

    panels = [
        FieldPanel("name", classname="full title"),
        MultiFieldPanel(
            [
                FieldPanel("cookie_type"),
                FieldPanel("purpose"),
                FieldPanel("duration"),
                FieldRowPanel([FieldPanel("domain"), FieldPanel("security")]),
            ],
            heading=_("General"),
        ),
    ]

    class Meta:
        ordering = ["domain", "cookie_type", "name"]
        unique_together = ("name", "domain")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    @property
    def expiration(self):
        return self.duration

    def __str__(self):
        return self.name
