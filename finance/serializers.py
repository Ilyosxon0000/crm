from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.FINANCE)
        fields="__all__"

class Student_PaySerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.STUDENT_PAY)
        fields="__all__"