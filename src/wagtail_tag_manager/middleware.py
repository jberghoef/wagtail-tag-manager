from bs4 import BeautifulSoup
from django.template import loader
from django.templatetags.static import static

from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.models import Tag, TagTypeSettings
from wagtail_tag_manager.strategy import TagStrategy


class TagManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request = request
        self.response = self.get_response(request)

        if self.request.method == 'GET' and self.response.status_code is 200:
            self.strategy = TagStrategy(request)
            for cookie_name, value in self.strategy.cookies.items():
                set_cookie(self.response, cookie_name, value)

            self._add_instant_tags()
            self._add_lazy_manager()

        return self.response

    def _add_instant_tags(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')

        for item in self.strategy.result:
            tag = item.get('tag', None)
            content = item.get('content', [])

            for element in content:
                if tag.tag_location == Tag.TOP_HEAD and doc.head:
                    doc.head.insert(1, element)
                elif tag.tag_location == Tag.BOTTOM_HEAD and doc.head:
                    doc.head.append(element)
                elif tag.tag_location == Tag.TOP_BODY and doc.body:
                    doc.body.insert(1, element)
                elif tag.tag_location == Tag.BOTTOM_BODY and doc.body:
                    doc.body.append(element)

        self.response.content = doc.prettify()

    def _add_lazy_manager(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')

        if doc.head and doc.body:
            template = loader.get_template('wagtail_tag_manager/state.html')
            element = BeautifulSoup(template.render({
                'config': TagTypeSettings.all(),
            }, self.request), 'html.parser')
            doc.head.append(element)

            element = doc.new_tag('script')
            element['src'] = static('wtm.bundle.js')
            doc.head.append(element)

        self.response.content = doc.prettify()
