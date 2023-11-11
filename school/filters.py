from myconf import conf
from myconf.conf import get_model
from django_filters.rest_framework import filterset
import django_filters

class AttendanceFilter(filterset.FilterSet):
    class Meta:
        model = get_model(conf.ATTENDANCE)
        fields = ["user","user__username","user__type_user",'date',"attendance_type"]
