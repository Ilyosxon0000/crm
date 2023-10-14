from myconf import conf
from myconf.conf import get_model
from django_filters.rest_framework import filterset
from django_filters import rest_framework as rsfilter

class ExpenseFilter(filterset.FilterSet):
    class Meta:
        model = get_model(conf.EXPENSE)
        fields = ["user","user__username","user__type_user","type"]