import json

from django.http import JsonResponse, HttpResponseBadRequest

from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.models import Tag


def lazy_endpoint(request):
    data = {'tags': []}
    response = JsonResponse(data)

    def process_tag(tag):
        for element in tag.get_contents(request, context):
            data['tags'].append({
                'name': element.name,
                'string': element.string,
            })

    if request.method == 'POST' and request.body:
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest()

        cookies = request.COOKIES

        tag_types = [tag_type for tag_type in payload if payload[tag_type]]
        tag_loads = [Tag.LAZY_LOAD]

        if tag_types:
            context = Tag.create_context(request)

        for tag_type in payload:
            cookie_name = Tag.get_cookie_name(tag_type)
            cookie = cookies.get(cookie_name, None)
            value = str(payload[tag_type]).lower()

            if cookie != value:
                response = set_cookie(response, cookie_name, value)

            if payload[tag_type] and cookie != value:
                tag_loads.append(Tag.INSTANT_LOAD)

        for tag in Tag.objects.filter(
            tag_type__in=tag_types, tag_loading__in=tag_loads
        ).active():
            process_tag(tag)

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
