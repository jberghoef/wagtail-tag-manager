import random

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WagtailTagManagerConfig(AppConfig):
    label = "wagtail_tag_manager"
    name = "wagtail_tag_manager"
    verbose_name = _("Wagtail Tag Manager")

    def ready(self):
        self.register_variables()

    @staticmethod
    def register_variables():
        from wagtail_tag_manager.decorators import register_variable
        from wagtail_tag_manager.options import CustomVariable
        from wagtail_tag_manager.settings import TagTypeSettings
        from wagtail_tag_manager.utils import get_consent

        class TagConsentVariable(CustomVariable):
            group = _("Consent")

            def get_value(self, request):
                consent_state = get_consent(request)
                return consent_state.get(self.key[8:])

        for tag_type, config in TagTypeSettings.all().items():
            instance = TagConsentVariable(
                name=config.get("verbose_name"),
                description=_(
                    "Retrieve consent state for %s tags." % config.get("verbose_name")
                ),
                key="consent_%s" % tag_type,
            )
            register_variable(instance)

        @register_variable
        class ReferrerVariable(CustomVariable):
            name = _("Referrer")
            description = _("The url of the previously visited page.")
            key = "navigation_referrer"
            group = _("Navigation")

            def get_value(self, request):
                if hasattr(request, "META"):
                    return request.META.get("HTTP_REFERER", "")
                return super().get_value(request)

        @register_variable
        class HostVariable(CustomVariable):
            name = _("Host")
            description = _("The hostname of the visited page.")
            key = "navigation_host"
            group = _("Navigation")

            def get_value(self, request):
                if hasattr(request, "get_host"):
                    return request.get_host()
                return super().get_value(request)

        @register_variable
        class URLVariable(CustomVariable):
            name = _("URL")
            description = _("The url of the visited page.")
            key = "navigation_url"
            group = _("Navigation")

            def get_value(self, request):
                if hasattr(request, "build_absolute_uri"):
                    return request.build_absolute_uri()
                return super().get_value(request)

        @register_variable
        class PathVariable(CustomVariable):
            name = _("Path")
            description = _("The path of the visited page.")
            key = "navigation_path"
            group = _("Navigation")

            def get_value(self, request):
                return getattr(request, "path", "")

        @register_variable
        class FullPathVariable(CustomVariable):
            name = _("Full path")
            description = _("The path of the visited page including query string.")
            key = "navigation_full_path"
            group = _("Navigation")

            def get_value(self, request):
                if hasattr(request, "get_full_path"):
                    return request.get_full_path()
                return super().get_value(request)

        @register_variable
        class UserVariable(CustomVariable):
            name = _("User")
            description = _("The ID of the logged in user.")
            key = "user_id"
            group = _("User")

            def get_value(self, request):
                if hasattr(request, "user"):
                    return getattr(request.user, "pk", "")
                return super().get_value(request)

        @register_variable
        class SessionVariable(CustomVariable):
            name = _("Session")
            description = _("The session ID of the visitor.")
            key = "user_session"
            group = _("User")

            def get_value(self, request):
                if hasattr(request, "session"):
                    return getattr(request.session, "session_key", "")
                return super().get_value(request)

        @register_variable
        class SiteVariable(CustomVariable):
            name = _("Site")
            description = _("The ID of the active site.")
            key = "wagtail_site"
            group = _("Wagtail")

            def get_value(self, request):
                if hasattr(request, "site"):
                    return getattr(request.site, "pk", "")
                return super().get_value(request)

        @register_variable
        class RandomVariable(CustomVariable):
            name = _("Random")
            description = _("A (pseudo) random number.")
            key = "rand"

            def get_value(self, request):
                return int(random.random() * 2_147_483_647)

        @register_variable
        class TriggerNameVariable(CustomVariable):
            name = _("Name")
            description = _("The name of a trigger event.")
            key = "trigger_name"
            group = _("Trigger")

        @register_variable
        class TriggerTypeVariable(CustomVariable):
            name = _("Type")
            description = _("The type of a trigger event.")
            key = "trigger_type"
            group = _("Trigger")

        @register_variable
        class TriggerValueVariable(CustomVariable):
            name = _("Value")
            description = _("The value retrieved from a trigger event.")
            key = "trigger_value"
            group = _("Trigger")
