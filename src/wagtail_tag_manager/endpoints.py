import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q

from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.strategy import define_tags


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

        tag_types, set_cookies = define_tags(request)

        if tag_types:
            context = Tag.create_context(request)

        for tag in Tag.objects.filter(*[
            Q(tag_loading=tag_type[0]) & Q(tag_type=tag_type[1])
            for tag_type in tag_types
        ]).active():
            process_tag(tag)

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
