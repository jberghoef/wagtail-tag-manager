import json
import base64
import binascii
from urllib.parse import quote, unquote

from django.http import HttpRequest


def get_page_for_request(request: HttpRequest):
    site = get_site_for_request(request)
    if site:
        path = request.path
        path_components = [component for component in path.split("/") if component]
        page, args, kwargs = site.root_page.specific.route(request, path_components)
        return page

    return None


def get_site_for_request(request: HttpRequest):
    try:
        from wagtail.models import Site

        return Site.find_for_request(request)
    except:  # noqa: E722
        return getattr(request, "site")


def dict_to_base64(input: dict) -> str:
    content = json.dumps(input, separators=(",", ":"), sort_keys=True)
    encoded_bytes = base64.b64encode(content.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return quote(encoded_string)


def base64_to_dict(input: str) -> dict:
    try:
        original_string = unquote(input)
        encoded_bytes = original_string.encode("utf-8")
        decoded_bytes = base64.b64decode(encoded_bytes)
        decoded_string = decoded_bytes.decode("utf-8")
        return json.loads(decoded_string)
    except binascii.Error:
        return {}
