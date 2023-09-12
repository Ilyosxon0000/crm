from myconf import conf
from myconf.conf import get_model
from django_filters.rest_framework import filterset

class AttendanceFilter(filterset.FilterSet):
    class Meta:
        model = get_model(conf.ATTENDANCE)
        fields = ["user.type_user","davomat",'date']
