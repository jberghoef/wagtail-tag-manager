from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import View, TemplateView

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.utils import set_cookie
from wagtail_tag_manager.models import Constant, Variable, TagTypeSettings


class ManageView(TemplateView):
    template_name = "wagtail_tag_manager/manage.html"

    def get(self, request, *args, **kwargs):
        if getattr(settings, "WTM_MANAGE_VIEW", True):
            return super().get(request, *args, **kwargs)
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(request.get_full_path())

        form = ConsentForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                set_cookie(response, f"wtm_{key}", str(value).lower())

        return response


class StateView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(TagTypeSettings.all())


class VariableView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return JsonResponse(
                {
                    "constants": [
                        constant.as_dict() for constant in Constant.objects.all()
                    ],
                    "variables": [
                        variable.as_dict() for variable in Variable.objects.all()
                    ],
                }
            )
        return HttpResponseNotFound()
