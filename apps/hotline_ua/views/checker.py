from django.views.generic import ListView

from apps.common.views import BaseCheckerListView
from apps.common.enums.checker_name import CheckerTypeName
from apps.hotline_ua.models import BaseSearchParameter


class CheckerListView(BaseCheckerListView, ListView):
    model_class = BaseSearchParameter
    template_name = 'hotline_ua/index.html'
    context_object_name = 'checkers'
    checker_type = CheckerTypeName.HOTLINE_UA
