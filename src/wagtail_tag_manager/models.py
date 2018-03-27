import random
import operator

from bs4 import BeautifulSoup
from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, FieldRowPanel)


class TagQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def functional(self, include=True):
        if include:
            return self.filter(tag_type=Tag.FUNCTIONAL)
        else:
            return self.exclude(tag_type=Tag.FUNCTIONAL)

    def analytical(self, include=True):
        if include:
            return self.filter(tag_type=Tag.ANALYTICAL)
        else:
            return self.exclude(tag_type=Tag.ANALYTICAL)

    def traceable(self, include=True):
        if include:
            return self.filter(tag_type=Tag.TRACEABLE)
        else:
            return self.exclude(tag_type=Tag.TRACEABLE)

    def instant(self):
        return self.filter(tag_loading=Tag.INSTANT_LOAD)

    def lazy(self):
        return self.filter(tag_loading=Tag.LAZY_LOAD)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def functional(self):
        return self.get_queryset().functional()

    def analytical(self):
        return self.get_queryset().analytical()

    def traceable(self):
        return self.get_queryset().traceable()

    def instant(self):
        return self.get_queryset().instant()

    def lazy(self):
        return self.get_queryset().lazy()


class Tag(models.Model):
    FUNCTIONAL = 'functional'
    ANALYTICAL = 'analytical'
    TRACEABLE = 'traceable'
    TYPE_CHOICES = [
        (FUNCTIONAL, _("Functional")),
        (ANALYTICAL, _("Analytical")),
        (TRACEABLE, _("Traceable")),
    ]

    TOP_HEAD = 'top_head'
    BOTTOM_HEAD = 'bottom_head'
    TOP_BODY = 'top_body'
    BOTTOM_BODY = 'bottom_body'
    LOCATION_CHOICES = [
        (TOP_HEAD, _("Top of head tag")),
        (BOTTOM_HEAD, _("Bottom of head tag")),
        (TOP_BODY, _("Top of body tag")),
        (BOTTOM_BODY, _("Bottom of body tag")),
    ]

    INSTANT_LOAD = 'instant_load'
    LAZY_LOAD = 'lazy_load'
    LOAD_CHOICES = [
        (INSTANT_LOAD, _("Instant")),
        (LAZY_LOAD, _("Lazy")),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    tag_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=FUNCTIONAL)
    tag_location = models.CharField(max_length=12, choices=LOCATION_CHOICES, default=TOP_HEAD)
    tag_loading = models.CharField(max_length=12, choices=LOAD_CHOICES, default=INSTANT_LOAD)

    content = models.TextField()

    objects = TagManager()

    panels = [
        FieldPanel('name', classname='full title'),
        FieldPanel('description', classname='full'),
        MultiFieldPanel([
            FieldPanel('tag_type'),
            FieldRowPanel([
                FieldPanel('tag_loading'),
                FieldPanel('tag_location'),
            ]),
            FieldPanel('active'),
        ], heading="Meta", classname="collapsible"),
        FieldPanel('content', classname='full'),
    ]

    def clean(self):
        self.content = str(self.get_doc())

    def get_doc(self, context=None):
        content = self.content

        if context:
            template = Template(content)
            context = Context(context)
            content = template.render(context)

        doc = BeautifulSoup(content, 'html.parser')

        for tag in doc.contents:
            if len(tag.string) > 1 and not tag.name:
                tag.string.wrap(doc.new_tag("script"))

        return doc

    def get_contents(self, request):
        context = {
            **Constant.create_context(),
            **Variable.create_context(request),
        }
        doc = self.get_doc(context)
        return doc.contents

    def __str__(self):
        return self.name


class Constant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    panels = [
        FieldPanel('name', classname='full title'),
        FieldPanel('description', classname='full'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('key'),
                FieldPanel('value'),
            ])
        ], heading="Data"),
    ]

    @classmethod
    def create_context(cls):
        context = {}

        for constant in cls.objects.all():
            context[constant.key] = constant.value

        return context

    def __str__(self):
        return self.name


class Variable(models.Model):
    TYPE_CHOICES = (
        (_("HTTP"), (
            ('path', _('Path')),
        )),
        (_("User"), (
            ('user.pk', _("User")),
            ('session.session_key', _("Session")),
        )),
        (_("Wagtail"), (
            ('site', _("Site")),
        )),
        (_("Other"), (
            ('_cookie+', _("Cookie")),
            ('_random', _("Random number")),
        )),
    )

    # TODO: Create edited edit/create view for values, based on '+' symbol.

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    key = models.CharField(max_length=255, unique=True)
    variable_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    value = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('name', classname='full title'),
        FieldPanel('description', classname='full'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('key'),
                FieldPanel('variable_type')
            ]),
            FieldPanel('value'),
        ], heading="Data"),
    ]

    def get_cookie(self, request):
        return request.COOKIES[self.value]

    def get_random(self, request):
        return int(random.random() * 2147483647)

    def get_value(self, request):
        variable_type = self.variable_type

        if variable_type.endswith('+'):
            variable_type = variable_type[:-1]

        if variable_type.startswith('_'):
            method = getattr(self, f'get{variable_type}')
            return method(request)

        if '.' in self.variable_type:
            return operator.attrgetter(str(self.variable_type))(request)

        return getattr(request, str(self.variable_type))

    @classmethod
    def create_context(cls, request):
        context = {}

        for variable in cls.objects.all():
            context[variable.key] = variable.get_value(request)

        return context

    def __str__(self):
        return self.name
