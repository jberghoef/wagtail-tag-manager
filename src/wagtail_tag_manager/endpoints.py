import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q

from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.strategy import TagStrategy


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

        strategy = TagStrategy(request)

        if strategy.include_tags:
            context = Tag.create_context(request)

        for tag in Tag.objects.active().filter(strategy.queryset):
            process_tag(tag)

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
