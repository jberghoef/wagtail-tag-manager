from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse
from django.template.response import TemplateResponse
from django.templatetags.static import static

from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.strategy import TagStrategy


class TagManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request = request
        self.response = self.get_response(request)

        if (
            not hasattr(self.request, "wtm_injected")  # Only once per request
            and getattr(self.request, "method", None) == "GET"
            and getattr(self.response, "status_code", None) == 200
            and isinstance(self.response, TemplateResponse)
        ):
            self.strategy = TagStrategy(request)
            for cookie_name, value in self.strategy.cookies.items():
                set_cookie(self.response, cookie_name, value)

            self._add_instant_tags()
            self._add_lazy_manager()

            self.request.wtm_injected = True

        return self.response

    def _add_instant_tags(self):
        if hasattr(self.response, "content"):
            doc = BeautifulSoup(self.response.content, "html.parser")

            for tag in self.strategy.result:
                obj = tag.get("object")
                element = tag.get("element")

                if obj.tag_location == Tag.TOP_HEAD and doc.head:
                    doc.head.insert(1, element)
                elif obj.tag_location == Tag.BOTTOM_HEAD and doc.head:
                    doc.head.append(element)
                elif obj.tag_location == Tag.TOP_BODY and doc.body:
                    doc.body.insert(1, element)
                elif obj.tag_location == Tag.BOTTOM_BODY and doc.body:
                    doc.body.append(element)

            self.response.content = doc.decode()

    def _add_lazy_manager(self):
        if hasattr(self.response, "content"):
            doc = BeautifulSoup(self.response.content, "html.parser")

            if doc.body:
                doc.body["data-wtm-state"] = reverse("wtm:state")
                doc.body["data-wtm-lazy"] = reverse("wtm:lazy")

                if getattr(settings, "WTM_INCLUDE_STYLE", True):
                    link = doc.new_tag("link")
                    link["rel"] = "stylesheet"
                    link["type"] = "text/css"
                    link["href"] = static("wtm.bundle.css")
                    doc.body.append(link)

                if getattr(settings, "WTM_INCLUDE_SCRIPT", True):
                    script = doc.new_tag("script")
                    script["type"] = "text/javascript"
                    script["src"] = static("wtm.bundle.js")
                    doc.body.append(script)

            self.response.content = doc.decode()
