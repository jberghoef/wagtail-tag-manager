from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WagtailTagManagerConfig(AppConfig):
    label = "wagtail_tag_manager"
    name = "wagtail_tag_manager"
    verbose_name = _("Wagtail Tag Manager")

    def ready(self):
        from wagtail_tag_manager.decorators import register_variable
        from wagtail_tag_manager.options import CustomVariable
        from wagtail_tag_manager.settings import TagTypeSettings
        from wagtail_tag_manager.utils import get_consent

        class TagConsentVariable(CustomVariable):
            def get_value(self, request):
                consent_state = get_consent(request)
                return consent_state.get(self.key)

        for tag_type, config in TagTypeSettings.all().items():
            instance = TagConsentVariable(
                name="%s consent" % config.get("verbose_name"),
                description=_(
                    "Retrieve consent state for %s tags." % config.get("verbose_name")
                ),
                key="consent_%s" % tag_type,
            )
            register_variable(instance)
