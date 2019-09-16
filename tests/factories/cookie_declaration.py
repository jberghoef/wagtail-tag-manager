import factory

from wagtail_tag_manager.models import CookieDeclaration


class CookieDeclarationFactory(factory.DjangoModelFactory):
    cookie_type = "necessary"
    name = "Necessary cookie"
    domain = "localhost"
    purpose = "Lorem ipsum"
    duration = 1
    security = CookieDeclaration.SECURE_COOKIE

    class Meta:
        model = CookieDeclaration
