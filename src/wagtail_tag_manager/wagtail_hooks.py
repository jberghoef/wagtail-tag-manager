from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from .models import Constant, Tag


class ConstantModelAdmin(ModelAdmin):
    model = Constant
    menu_icon = 'snippet'
    menu_order = 200
    list_display = ('name', 'key', 'value',)
    search_fields = ('name', 'key', 'value', 'description',)


class TagModelAdmin(ModelAdmin):
    model = Tag
    menu_icon = 'code'
    menu_order = 100
    list_display = ('name', 'tag_type', 'tag_location', 'tag_loading', 'active')
    list_filter = ('active', 'tag_type', 'tag_location', 'tag_loading')
    search_fields = ('name', 'description', 'content')
    form_view_extra_js = [static('tag_form_view.bundle.js')]


class TagManagerAdminGroup(ModelAdminGroup):
    menu_label = _("Tag Manager")
    menu_icon = 'code'
    menu_order = 1000
    items = (ConstantModelAdmin, TagModelAdmin)


modeladmin_register(TagManagerAdminGroup)
