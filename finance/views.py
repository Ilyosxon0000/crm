from myconf.conf import get_model
from myconf import conf
from rest_framework.viewsets import ModelViewSet
from . import serializers

class ExpenseView(ModelViewSet):
    queryset = get_model(conf.EXPENSE).objects.all()
    serializer_class = serializers.ExpenseSerializer

class Student_PayView(ModelViewSet):
    queryset=get_model(conf.STUDENT_PAY).objects.all()
    serializer_class=serializers.Student_PaySerializer

class Each_payView(ModelViewSet):
    queryset = get_model(conf.EACH_PAY).objects.all()
    serializer_class = serializers.Each_paySerializer
    filterset_fields="__all__"