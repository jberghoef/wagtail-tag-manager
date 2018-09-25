import json

from django.http import JsonResponse, HttpResponseBadRequest

from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.strategy import TagStrategy


def lazy_endpoint(request):
    data = {"tags": []}
    response = JsonResponse(data)

    if request.method == "POST" and request.body:
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()

        consent = payload.get("consent", None)

        request.path = payload.get("pathname", request.path)
        request.META["QUERY_STRING"] = payload.get("search", "")

        strategy = TagStrategy(request, consent)

        for cookie_name, value in strategy.cookies.items():
            set_cookie(response, cookie_name, value)

        for item in strategy.result:
            content = item.get("content", [])

            for element in content:
                data["tags"].append({"name": element.name, "string": element.string})

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
