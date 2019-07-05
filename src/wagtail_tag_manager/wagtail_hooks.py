from django.conf import settings
from django.urls import reverse
from wagtail.core import hooks
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from wagtail.admin.site_summary import SummaryItem
from django.template.defaultfilters import truncatechars
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from wagtail_tag_manager.views import WTMIndexView, CookieDeclarationIndexView
from wagtail_tag_manager.models import (
    Tag,
    Trigger,
    Constant,
    Variable,
    CookieDeclaration,
)
from wagtail_tag_manager.settings import TagTypeSettings


class ConstantModelAdmin(ModelAdmin):
    model = Constant
    menu_icon = "snippet"
    list_display = ("name_display", "key", "value")
    search_fields = ("name", "key", "value", "description")
    index_view_class = WTMIndexView
    index_template_name = "wagtail_tag_manager/admin/constant_index.html"
    help_text = _(
        "Constants allow you to store reusable information for usage in 1 or multiple tags. "
        "This is often used for account ID's."
    )

    @staticmethod
    def name_display(obj):
        if obj.description:
            description = truncatechars(obj.description, 64)
            return mark_safe(f"{obj.name}<br/><small>{description}</small>")
        return obj.name

    name_display.short_description = _("Name")


class VariableModelAdmin(ModelAdmin):
    model = Variable
    menu_icon = "snippet"
    list_display = ("name_display", "key", "variable_type")
    list_filter = ("variable_type",)
    search_fields = ("name", "key", "description")
    form_view_extra_js = [static("variable_form_view.bundle.js")]
    index_view_class = WTMIndexView
    index_template_name = "wagtail_tag_manager/admin/variable_index.html"
    help_text = _(
        "Variables allow you to retrieve information corresponding to a request and add that to 1 or multiple tags."
    )

    @staticmethod
    def name_display(obj):
        if obj.description:
            description = truncatechars(obj.description, 64)
            return mark_safe(f"{obj.name}<br/><small>{description}</small>")
        return obj.name

    name_display.short_description = _("Name")


class TagModelAdmin(ModelAdmin):
    model = Tag
    menu_icon = "code"
    list_display = (
        "name_display",
        "tag_type_display",
        "tag_loading",
        "tag_location",
        "priority",
        "auto_load",
    )
    list_filter = ("auto_load", "tag_type", "tag_location", "tag_loading")
    search_fields = ("name", "description", "content")
    form_view_extra_js = [static("tag_form_view.bundle.js")]
    index_view_class = WTMIndexView
    index_template_name = "wagtail_tag_manager/admin/tag_index.html"
    help_text = _(
        "A tag is a little code snippet (HTML containing CSS, JavaScript or both) that can be added to your page. "
        "You can choose where and when this tag should load, "
        "allowing you to control the order in which the tags will be loaded."
    )

    @staticmethod
    def name_display(obj):
        if obj.description:
            description = truncatechars(obj.description, 64)
            return mark_safe(f"{obj.name}<br/><small>{description}</small>")
        return obj.name

    name_display.short_description = _("Name")

    @staticmethod
    def tag_type_display(obj):
        config = TagTypeSettings().get(obj.tag_type)
        return config.get("verbose_name")

    tag_type_display.short_description = _("Tag type")


class TriggerModelAdmin(ModelAdmin):
    model = Trigger
    menu_icon = "media"
    list_display = ("name_display", "tags_count", "active")
    list_filter = ("active",)
    search_fields = ("name", "description")
    form_view_extra_js = [static("trigger_form_view.bundle.js")]
    index_view_class = WTMIndexView
    index_template_name = "wagtail_tag_manager/admin/trigger_index.html"
    help_text = _(
        "Triggers monitor the behaviour of a visitor on a page and can load tags whenever a certain event takes place. "
        "For example, when a form is submitted or a user scrolls past a certain point on the page."
    )

    @staticmethod
    def name_display(obj):
        if obj.description:
            description = truncatechars(obj.description, 64)
            return mark_safe(f"{obj.name}<br/><small>{description}</small>")
        return obj.name

    name_display.short_description = _("Name")

    @staticmethod
    def tags_count(obj):
        return f"{obj.tags.count()} tag(s)"

    tags_count.short_description = _("Tags")


class CookieDeclarationModelAdmin(ModelAdmin):
    model = CookieDeclaration
    menu_icon = "tick"
    list_display = ("cookie_type", "name", "domain", "duration", "security")
    list_filter = ("cookie_type", "domain", "security")
    search_fields = ("name", "purpose", "domain")
    index_view_class = CookieDeclarationIndexView
    index_template_name = "wagtail_tag_manager/admin/cookie_declaration_index.html"
    help_text = _(
        "Cookie declarations provide visitors of your website with insight into the data that is "
        "stored on their computer by your site. These declarations will be visible in the "
        'cookie bar. Use the "Scan for cookies" button to automatically detect cookies. '
        "Note that it is unlikely the scanner will find everything."
    )


class TagManagerAdminGroup(ModelAdminGroup):
    menu_label = _("Tag Manager")
    menu_icon = "code"
    menu_order = 640
    items = (
        TagModelAdmin,
        ConstantModelAdmin,
        VariableModelAdmin,
        TriggerModelAdmin,
        CookieDeclarationModelAdmin,
    )


modeladmin_register(TagManagerAdminGroup)


# Summary panels
class ModelCountSummaryItem(SummaryItem):
    order = 0
    model = None
    reverse = ""
    title = "Placeholder"
    icon = "placeholder"

    def render(self):
        count = self.model.objects.count()
        target_url = reverse(self.reverse)
        return mark_safe(
            f"""
            <li class="icon icon-{self.icon}">
                <a href="{target_url}"><span>{count}</span>{self.title}</a>
            </li>"""
        )


class TagSummaryPanel(ModelCountSummaryItem):
    order = 3000
    model = Tag
    reverse = "wagtail_tag_manager_tag_modeladmin_index"
    title = _("Tags")
    icon = "code"


class ConstantSummaryPanel(ModelCountSummaryItem):
    order = 3100
    model = Constant
    reverse = "wagtail_tag_manager_constant_modeladmin_index"
    title = _("Constants")
    icon = "snippet"


class VariableSummaryPanel(ModelCountSummaryItem):
    order = 3200
    model = Variable
    reverse = "wagtail_tag_manager_variable_modeladmin_index"
    title = _("Variables")
    icon = "snippet"


class TriggerSummaryPanel(ModelCountSummaryItem):
    order = 3300
    model = Trigger
    reverse = "wagtail_tag_manager_trigger_modeladmin_index"
    title = _("Triggers")
    icon = "media"


class CookieDeclarationSummaryPanel(ModelCountSummaryItem):
    order = 3400
    model = CookieDeclaration
    reverse = "wagtail_tag_manager_cookiedeclaration_modeladmin_index"
    title = _("Cookie declarations")
    icon = "tick"


@hooks.register("construct_homepage_summary_items")
def add_personalisation_summary_panels(request, items):
    if getattr(settings, "WTM_SUMMARY_PANELS", False):
        items.append(TagSummaryPanel(request))
        items.append(ConstantSummaryPanel(request))
        items.append(VariableSummaryPanel(request))
        items.append(TriggerSummaryPanel(request))
        items.append(CookieDeclarationSummaryPanel(request))
