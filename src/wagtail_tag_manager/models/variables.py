import re
import operator

from django.db import models
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel

from wagtail_tag_manager.decorators import get_variables


class Variable(models.Model):
    TYPE_CHOICES = (
        (_("HTTP"), (("_repath+", _("Path with regex")),)),
        (_("Other"), (("_cookie+", _("Cookie")),)),
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
                "<b>Path with regex:</b> the path of the visited page after "
                "applying a regex search.<br/>"
                "<b>Cookie:</b> the value of a cookie, when available."
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
        from wagtail_tag_manager.models.constants import Constant

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
