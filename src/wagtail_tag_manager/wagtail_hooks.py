from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from wagtail_tag_manager.models import Tag, Constant, Variable


class ConstantModelAdmin(ModelAdmin):
    model = Constant
    menu_icon = 'snippet'
    list_display = ('name', 'key', 'value',)
    search_fields = ('name', 'key', 'value', 'description',)


class VariableModelAdmin(ModelAdmin):
    model = Variable
    menu_icon = 'snippet'
    list_display = ('name', 'key', 'variable_type',)
    list_filter = ('variable_type',)
    search_fields = ('name', 'key', 'description',)
    form_view_extra_js = [static('variable_form_view.bundle.js')]


class TagModelAdmin(ModelAdmin):
    model = Tag
    menu_icon = 'code'
    list_display = ('name', 'tag_type', 'tag_location', 'tag_loading', 'active')
    list_filter = ('active', 'tag_type', 'tag_location', 'tag_loading')
    search_fields = ('name', 'description', 'content')
    form_view_extra_js = [static('tag_form_view.bundle.js')]


class TagManagerAdminGroup(ModelAdminGroup):
    menu_label = _("Tag Manager")
    menu_icon = 'code'
    menu_order = 1000
    items = (TagModelAdmin, ConstantModelAdmin, VariableModelAdmin)


modeladmin_register(TagManagerAdminGroup)
