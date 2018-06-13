import json

from django.http import JsonResponse, HttpResponseBadRequest

from .utils import set_cookie
from .models import Tag


def lazy_endpoint(request):
    data = {'tags': []}
    response = JsonResponse(data)

    def process_payload(tag_type):
        cookie = cookies.get(f'wtm_{tag_type}', None)
        value = str(payload[tag_type]).lower()
        if cookie != value:
            set_cookie(response, f'wtm_{tag_type}', value)

        if payload[tag_type]:
            for tag in tags.filter(tag_type=tag_type).lazy():
                process_tag(tag)

            if cookie != value:
                for tag in tags.filter(tag_type=tag_type).instant():
                    process_tag(tag)

    def process_tag(tag):
        for element in tag.get_contents(request):
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
        tags = Tag.objects.active()

        for tag_type in Tag.get_types():
            if tag_type in payload:
                process_payload(tag_type)

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
