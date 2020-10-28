from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse
from django.templatetags.static import static

from wagtail_tag_manager.utils import set_consent
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.strategy import TagStrategy


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


class CookieConsentMiddleware(BaseMiddleware):
    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        if (
            getattr(request, "method", None) == "GET"
            and getattr(response, "status_code", None) == 200
            and not getattr(response, "streaming", False)
        ):
            strategy = TagStrategy(request)
            set_consent(
                request,
                response,
                {key: value for key, value in strategy.consent.items()},
            )

        return response


class TagManagerMiddleware(BaseMiddleware):
    def __call__(self, request):
        response = self.get_response(request)
        if "Content-Length" in response and not getattr(response, "streaming", False):
            response["Content-Length"] = len(response.content)
        return response

    def process_template_response(self, request, response):
        response.render()
        response = self._add_instant_tags(request, response)
        response = self._add_lazy_manager(response)
        return response

    def _add_instant_tags(self, request, response):
        if hasattr(response, "content") and getattr(settings, "WTM_INJECT_TAGS", True):
            strategy = TagStrategy(request)
            content = response.content.decode(response.charset)
            doc = BeautifulSoup(content, "html.parser")
            head = getattr(doc, "head", [])
            body = getattr(doc, "body", [])

            for tag in strategy.result:
                obj = tag.get("object")
                element = tag.get("element")

                if head and obj.tag_location == Tag.TOP_HEAD:
                    head.insert(1, element)
                elif head and obj.tag_location == Tag.BOTTOM_HEAD:
                    head.append(element)
                elif body and obj.tag_location == Tag.TOP_BODY:
                    body.insert(1, element)
                elif body and obj.tag_location == Tag.BOTTOM_BODY:
                    body.append(element)

            doc.head = head
            doc.body = body
            response.content = doc.encode(formatter=None)

        return response

    def _add_lazy_manager(self, response):
        if hasattr(response, "content"):
            content = response.content.decode(response.charset)
            doc = BeautifulSoup(content, "html.parser")

            if doc.body:
                doc.body["data-wtm-config"] = reverse("wtm:config")
                doc.body["data-wtm-lazy"] = reverse("wtm:lazy")

                if getattr(settings, "WTM_INJECT_STYLE", True):
                    link = doc.new_tag("link")
                    link["rel"] = "stylesheet"
                    link["type"] = "text/css"
                    link["href"] = static("wagtail_tag_manager/wtm.bundle.css")
                    doc.body.append(link)

                if getattr(settings, "WTM_INJECT_SCRIPT", True):
                    script = doc.new_tag("script")
                    script["type"] = "text/javascript"
                    script["src"] = static("wagtail_tag_manager/wtm.bundle.js")
                    doc.body.append(script)

            response.content = doc.encode(formatter=None)

        return response
