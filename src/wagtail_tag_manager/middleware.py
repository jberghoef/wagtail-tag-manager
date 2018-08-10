import json

from bs4 import BeautifulSoup
from django.conf import settings
from django.template import loader
from django.templatetags.static import static

from wagtail_tag_manager.models import Tag, TagTypeSettings
from wagtail_tag_manager.strategy import TagStrategy
from wagtail_tag_manager.utils import set_cookie


class TagManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request = request
        self.response = self.get_response(request)

        if self.request.method == 'GET' and self.response.status_code is 200:
            self.strategy = TagStrategy(request)
            for cookie_name in self.strategy.include_cookies:
                set_cookie(self.response, cookie_name, 'true')
            for cookie_name in self.strategy.exclude_cookies:
                set_cookie(self.response, cookie_name, 'false')

            self._add_instant_tags()
            self._add_lazy_manager()

        return self.response

    def _add_instant_tags(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')
        context = Tag.create_context(self.request)

        def process_tag(tag_instance):
            contents = tag_instance.get_contents(self.request, context)
            for element in contents:
                if tag_instance.tag_location == Tag.TOP_HEAD and doc.head:
                    doc.head.insert(1, element)
                elif tag_instance.tag_location == Tag.BOTTOM_HEAD and doc.head:
                    doc.head.append(element)
                elif tag_instance.tag_location == Tag.TOP_BODY and doc.body:
                    doc.body.insert(1, element)
                elif tag_instance.tag_location == Tag.BOTTOM_BODY and doc.body:
                    doc.body.append(element)

        for tag in Tag.objects.active().filter(self.strategy.queryset):
            process_tag(tag)

        self.response.content = doc.prettify()

    def _add_lazy_manager(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')

        if doc.head and doc.body:
            context = {
                'config': json.dumps({
                    tag_type: config
                    for tag_type, config in TagTypeSettings.all().items()
                }),
                'manage_view': getattr(settings, 'WTM_MANAGE_VIEW', True)
            }

            template = loader.get_template('wagtail_tag_manager/state.html')
            element = BeautifulSoup(
                template.render(context, self.request), 'html.parser')
            doc.head.append(element)

            template = loader.get_template('wagtail_tag_manager/cookie_bar.html')
            element = BeautifulSoup(
                template.render(context, self.request), 'html.parser')
            doc.head.append(element)

            element = doc.new_tag('script')
            element['src'] = static('wtm.bundle.js')
            doc.head.append(element)

        self.response.content = doc.prettify()
