import re

from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.widgets import VariableSelect
from wagtail_tag_manager.widgets import (
    HorizontalCheckboxSelectMultiple as CheckboxSelectMultiple,
)
from wagtail_tag_manager.managers import TriggerQuerySet


class Trigger(ClusterableModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(
        default=True, help_text=_("Uncheck to disable this trigger from firing.")
    )

    TYPE_CLICK_ALL_ELEMENTS = "click_all_elements"
    TYPE_CLICK_SOME_ELEMENTS = "click_some_elements+"
    TYPE_VISIBILITY_ONCE_PER_PAGE = "visibility_once_per_page+"
    TYPE_VISIBILITY_ONCE_PER_ELEMENT = "visibility_once_per_element+"
    TYPE_VISIBILITY_RECURRING = "visibility_recurring+"
    TYPE_FORM_SUBMIT = "form_submit"
    TYPE_HISTORY_CHANGE = "history_change"
    TYPE_JAVASCRIPT_ERROR = "javascript_error"
    TYPE_SCROLL_VERTICAL = "scroll_vertical+"
    TYPE_SCROLL_HORIZONTAL = "scroll_horizontal+"
    TYPE_TIMER_TIMEOUT = "timer_timeout+"
    TYPE_TIMER_INTERVAL = "timer_interval+"
    TYPE_CHOICES = (
        (TYPE_FORM_SUBMIT, _("Form submit")),
        (TYPE_HISTORY_CHANGE, _("History change")),
        (TYPE_JAVASCRIPT_ERROR, _("JavaScript error")),
        (
            _("Click"),
            (
                (TYPE_CLICK_ALL_ELEMENTS, _("Click on all elements")),
                (TYPE_CLICK_SOME_ELEMENTS, _("Click on some elements")),
            ),
        ),
        (
            _("Visibility"),  # TODO: Advanced options...
            (
                (TYPE_VISIBILITY_ONCE_PER_PAGE, _("Monitor once per page")),
                (TYPE_VISIBILITY_ONCE_PER_ELEMENT, _("Monitor once per element")),
                (TYPE_VISIBILITY_RECURRING, _("Monitor recurringingly")),
            ),
        ),
        (
            _("Scroll"),
            (
                (TYPE_SCROLL_VERTICAL, _("Scroll vertical")),
                (TYPE_SCROLL_HORIZONTAL, _("Scroll horizontal")),
            ),
        ),
        (
            _("Timer"),
            (
                (TYPE_TIMER_TIMEOUT, _("Timer with timeout")),
                (TYPE_TIMER_INTERVAL, _("Timer with interval")),
            ),
        ),
    )

    trigger_type = models.CharField(
        max_length=255, choices=TYPE_CHOICES, default=TYPE_FORM_SUBMIT
    )
    value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=mark_safe(
            _(
                "<b>Click:</b> the query selector of the element(s).<br/>"
                "<b>Visibility:</b> the query selector of the element(s).<br/>"
                "<b>Scroll:</b> the distance after which to trigger as percentage.<br/>"
                "<b>Timer:</b> the time in milliseconds after which to trigger."
            )
        ),
    )

    tags = models.ManyToManyField(
        Tag, help_text=_("The tags to include when this trigger is fired.")
    )

    objects = TriggerQuerySet.as_manager()

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [FieldPanel("trigger_type"), FieldPanel("value"), FieldPanel("active")],
            heading=_("Configuration"),
        ),
        InlinePanel("conditions", label=_("Conditions")),
        FieldPanel("tags", widget=CheckboxSelectMultiple),
    ]

    def as_dict(self):
        return {
            "slug": self.slug,
            "type": re.sub(r"[+]", "", self.trigger_type),
            "value": self.get_value(),
        }

    def get_value(self):
        numbered = [
            self.TYPE_SCROLL_VERTICAL,
            self.TYPE_SCROLL_HORIZONTAL,
            self.TYPE_TIMER_TIMEOUT,
            self.TYPE_TIMER_INTERVAL,
        ]

        if self.trigger_type in numbered:
            return int(self.value)

        return self.value

    def validate(self, context) -> bool:
        if self.conditions.count() == 0:
            return True
        return all([condition.validate(context) for condition in self.conditions.all()])

    def clean(self):
        super().clean()
        self.slug = slugify(self.name)

        if self.trigger_type.endswith("+") and not self.value:
            raise ValidationError(_("A value is required for this trigger type."))
        elif self.value and not self.trigger_type.endswith("+"):
            raise ValidationError(_("A value is not allowed for this trigger type."))

    def __str__(self):
        return self.name


class TriggerCondition(Orderable):
    trigger = ParentalKey(Trigger, on_delete=models.CASCADE, related_name="conditions")

    variable = models.CharField(max_length=255, null=True, blank=False)

    CONDITION_EXACT_MATCH = "exact_match"
    CONDITION_NOT_EXACT_MATCH = "not_exact_match"
    CONDITION_CONTAINS = "contains"
    CONDITION_NOT_CONTAINS = "not_contains"
    CONDITION_STARTS_WITH = "starts_with"
    CONDITION_NOT_STARTS_WITH = "not_starts_with"
    CONDITION_ENDS_WITH = "ends_with"
    CONDITION_NOT_ENDS_WITH = "not_ends_with"

    CONDITION_REGEX_MATCH = "regex_match"
    CONDITION_NOT_REGEX_MATCH = "not_regex_match"
    CONDITION_REGEX_IMATCH = "regex_imatch"
    CONDITION_NOT_REGEX_IMATCH = "not_regex_imatch"

    CONDITION_LT = "lower_than"
    CONDITION_LTE = "lower_than_equal"
    CONDITION_GT = "greater_than"
    CONDITION_GTE = "greater_than_equal"

    CONDITION_CHOICES = (
        (
            _("Text"),
            (
                (CONDITION_EXACT_MATCH, _("exact match")),
                (CONDITION_NOT_EXACT_MATCH, _("not exact match")),
                (CONDITION_CONTAINS, _("contains")),
                (CONDITION_NOT_CONTAINS, _("does not contain")),
                (CONDITION_STARTS_WITH, _("starts with")),
                (CONDITION_NOT_STARTS_WITH, _("does not start with")),
                (CONDITION_ENDS_WITH, _("ends with")),
                (CONDITION_NOT_ENDS_WITH, _("does not end with")),
            ),
        ),
        (
            _("Regex"),
            (
                (CONDITION_REGEX_MATCH, _("matches regex")),
                (CONDITION_NOT_REGEX_MATCH, _("does not match regex")),
                (CONDITION_REGEX_IMATCH, _("matches regex (case insensitive)")),
                (
                    CONDITION_NOT_REGEX_IMATCH,
                    _("does not match regex (case insensitive)"),
                ),
            ),
        ),
        (
            _("Numbers"),
            (
                (CONDITION_LT, _("is lower than")),
                (CONDITION_LTE, _("is lower than or equal to")),
                (CONDITION_GT, _("is greater than")),
                (CONDITION_GTE, _("is greater than or equal to")),
            ),
        ),
    )

    condition_type = models.CharField(
        max_length=255, choices=CONDITION_CHOICES, default=CONDITION_CONTAINS
    )

    value = models.CharField(max_length=255)

    panels = [
        FieldPanel("variable", widget=VariableSelect),
        FieldPanel("condition_type"),
        FieldPanel("value"),
    ]

    def validate(self, context) -> bool:
        if self.variable in context:
            variable = context.get(self.variable, None)
            validator = getattr(self, self.condition_type)
            return validator(variable, self.value)
        return False

    # Text
    @staticmethod
    def exact_match(variable, value):
        return str(value) == str(variable)

    def not_exact_match(self, *args, **kwargs):
        return not self.exact_match(*args, **kwargs)

    @staticmethod
    def contains(variable, value):
        return str(value) in str(variable)

    def not_contains(self, *args, **kwargs):
        return not self.contains(*args, **kwargs)

    @staticmethod
    def starts_with(variable, value):
        return str(variable).startswith(str(value))

    def not_starts_with(self, *args, **kwargs):
        return not self.starts_with(*args, **kwargs)

    @staticmethod
    def ends_with(variable, value):
        return str(variable).endswith(str(value))

    def not_ends_with(self, *args, **kwargs):
        return not self.ends_with(*args, **kwargs)

    # Regex
    @staticmethod
    def regex_match(variable, value):
        return re.match(value, str(variable)) is not None

    def not_regex_match(self, *args, **kwargs):
        return not self.regex_match(*args, **kwargs)

    @staticmethod
    def regex_imatch(variable, value):
        return re.match(value, str(variable), re.IGNORECASE) is not None

    def not_regex_imatch(self, *args, **kwargs):
        return not self.regex_imatch(*args, **kwargs)

    # Numbers
    @staticmethod
    def lower_than(variable, value):
        return float(variable) < float(value)

    @staticmethod
    def lower_than_equal(variable, value):
        return float(variable) <= float(value)

    @staticmethod
    def greater_than(variable, value):
        return float(variable) > float(value)

    @staticmethod
    def greater_than_equal(variable, value):
        return float(variable) >= float(value)
