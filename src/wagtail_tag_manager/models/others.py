from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel

from wagtail_tag_manager.managers import CookieDeclarationQuerySet
from wagtail_tag_manager.settings import TagTypeSettings


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
