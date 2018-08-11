import json

from django.http import JsonResponse, HttpResponseBadRequest

from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.strategy import TagStrategy
from wagtail_tag_manager.utils import set_cookie


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

        consent = None
        if 'consent' in payload:
            consent = payload['consent']

        strategy = TagStrategy(request, consent)

        for cookie_name in strategy.include_cookies:
            set_cookie(response, cookie_name, 'true')
        for cookie_name in strategy.exclude_cookies:
            set_cookie(response, cookie_name, 'false')

        if strategy.include_tags:
            context = Tag.create_context(request)

        for tag in Tag.objects.active().filter(strategy.queryset):
            process_tag(tag)

        response.content = json.dumps(data)
        return response

    return HttpResponseBadRequest()
