from bs4 import BeautifulSoup
from django.conf import settings
from django.template import loader
from django.templatetags.static import static

from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.models import Tag


class TagManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request = request
        self.response = self.get_response(request)

        if self.request.method == 'GET' and self.response.status_code is 200:
            self.cookies = request.COOKIES
            cookie_name = Tag.get_cookie_name(Tag.FUNCTIONAL)

            # Functional cookies are always allowed.
            if (
                cookie_name not in self.cookies or
                self.cookies[cookie_name] == 'false'
            ):
                self.cookies[cookie_name] = 'true'
                set_cookie(self.response, cookie_name, 'true')

            self._add_instant_tags()
            self._add_lazy_manager()

        return self.response

    def _add_instant_tags(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')
        context = Tag.create_context(self.request)

        def handle_tag(tag):
            contents = tag.get_contents(self.request, context)
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

        enabled_tags = [
            tag_type for tag_type in Tag.get_types()
            if Tag.get_cookie_name(tag_type) in self.cookies and
            self.cookies[Tag.get_cookie_name(tag_type)] != 'false']

        for tag in tags.filter(tag_type__in=enabled_tags):
            handle_tag(tag)

        self.response.content = doc.prettify()

    def _add_lazy_manager(self):
        doc = BeautifulSoup(self.response.content, 'html.parser')

        if doc.head and doc.body:
            tags = Tag.objects.active()

            context = {
                tag_type: tags.filter(tag_type=tag_type).exists()
                for tag_type in Tag.get_types()
            }

            context['manage_view'] = getattr(settings, 'WTM_MANAGE_VIEW', True)

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
