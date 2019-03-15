from django.db import models


class TagQuerySet(models.QuerySet):
    def auto_load(self):
        return self.filter(auto_load=True)

    def passive(self):
        return self.filter(auto_load=False)

    def instant(self):
        from wagtail_tag_manager.models import Tag

        return self.filter(tag_loading=Tag.INSTANT_LOAD)

    def lazy(self):
        from wagtail_tag_manager.models import Tag

        return self.filter(tag_loading=Tag.LAZY_LOAD)

    def sorted(self):
        from wagtail_tag_manager.models import Tag

        order = [*Tag.get_types(), None]
        return sorted(self, key=lambda x: order.index(x.tag_type))


class TriggerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


class CookieDeclarationQuerySet(models.QuerySet):
    def sorted(self):
        from wagtail_tag_manager.models import Tag

        order = [*Tag.get_types(), None]
        return sorted(self, key=lambda x: order.index(x.cookie_type))
