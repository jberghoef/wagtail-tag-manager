import json
from django.http import JsonResponse

from .models import Tag


def lazy_view(request):
    data = {'tags': []}
    response = JsonResponse(data)

    def process_tag(t):
        for element in t.get_contents(request):
            data['tags'].append({
                'name': element.name,
                'string': element.string,
            })

    if request.method == 'POST':
        if request.body:
            payload = json.loads(request.body)
            cookies = request.COOKIES

            tags = Tag.objects.active()

            if 'functional' in payload and payload['functional']:
                for tag in tags.functional().lazy():
                    process_tag(tag)

            if 'analytical' in payload and payload['analytical']:
                for tag in tags.analytical().lazy():
                    process_tag(tag)

                if 'wtm_analytical' not in cookies:
                    response.set_cookie('wtm_analytical', 'true')
                    for tag in tags.analytical().instant():
                        process_tag(tag)

            if 'traceable' in payload and payload['traceable']:
                for tag in tags.traceable().lazy():
                    process_tag(tag)

                if 'wtm_traceable' not in cookies:
                    response.set_cookie('wtm_traceable', 'true')
                    for tag in tags.traceable().instant():
                        process_tag(tag)

        response.content = json.dumps(data)
        return response
