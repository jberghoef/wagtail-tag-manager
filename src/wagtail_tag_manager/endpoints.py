import json

from django.http import JsonResponse, HttpResponseBadRequest

from wagtail_tag_manager.utils import set_consent
from wagtail_tag_manager.strategy import TagStrategy


def lazy_endpoint(request):
    data = {"tags": []}
    response = JsonResponse(data)

    if getattr(request, "method", None) == "POST" and hasattr(request, "body"):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()

        request.path = payload.get("pathname", request.path)
        request.META["QUERY_STRING"] = payload.get("search", "")

        strategy = TagStrategy(request, payload)

        set_consent(response, {key: value for key, value in strategy.consent.items()})

        for tag in strategy.result:
            element = tag.get("element")

            for content in element.contents:
                if content.name:
                    data["tags"].append(
                        {
                            "name": content.name,
                            "attributes": getattr(content, "attrs", {}),
                            "string": content.string,
                        }
                    )

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
