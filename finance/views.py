from myconf.conf import get_model
from myconf import conf
from rest_framework.viewsets import ModelViewSet
from . import serializers

# Create your views here.

class FinanceView(ModelViewSet):
    queryset=get_model(conf.FINANCE).objects.all()
    serializer_class=serializers.FinanceSerializer

class Student_PayView(ModelViewSet):
    queryset=get_model(conf.STUDENT_PAY).objects.all()
    serializer_class=serializers.Student_PaySerializer