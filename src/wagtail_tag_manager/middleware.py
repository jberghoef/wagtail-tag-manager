from bs4 import BeautifulSoup
from django.template import loader
from django.templatetags.static import static

from .models import Constant, Tag


class TagManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request = request
        self.response = self.get_response(request)
        self.cookies = request.COOKIES
        self.context = Constant.create_context()

        if self.response.status_code is 200:
            self._add_instant_tags()
            self._add_lazy_tags()

        return self.response

    def _add_instant_tags(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')

        def handle_tag(tag):
            contents = tag.get_contents(self.context)
            for element in contents:
                if tag.tag_location == Tag.TOP_HEAD and doc.head:
                    doc.head.insert(1, element)
                elif tag.tag_location == Tag.BOTTOM_HEAD and doc.head:
                    doc.head.append(element)
                elif tag.tag_location == Tag.TOP_BODY and doc.body:
                    doc.body.insert(1, element)
                elif tag.tag_location == Tag.BOTTOM_BODY and doc.body:
                    doc.body.append(element)

        tags = Tag.objects.active().instant()
        for tag in tags.functional():
            handle_tag(tag)

        if 'wtm_analytical' in self.cookies and self.cookies['wtm_analytical'] != 'false':
            for tag in tags.analytical():
                handle_tag(tag)

        if 'wtm_traceable' in self.cookies and self.cookies['wtm_traceable'] != 'false':
            for tag in tags.traceable():
                handle_tag(tag)

        self.response.content = doc.prettify()

    def _add_lazy_tags(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')

        if doc.head:
            context = {
                'functional': Tag.objects.active().functional().exists(),
                'analytical': Tag.objects.active().analytical().exists(),
                'traceable': Tag.objects.active().traceable().exists(),
            }

            template = loader.get_template('pre_manager.html')
            element = BeautifulSoup(
                template.render(context, self.request), 'html.parser')
            doc.head.append(element)

            template = loader.get_template('cookie_bar.html')
            element = BeautifulSoup(
                template.render(context, self.request), 'html.parser')
            doc.head.append(element)

            element = doc.new_tag('script')
            element['src'] = static('wtm.bundle.js')
            doc.head.append(element)

        self.response.content = doc.prettify()

