from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.EXPENSE)
        fields="__all__"

class Student_PaySerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.STUDENT_PAY)
        fields="__all__"

class Each_paySerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.EACH_PAY)
        fields="__all__"