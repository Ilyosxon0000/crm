from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf
from accounts import serializers as acser

class StudentDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.STUDENT_DEBT)
        fields="__all__"

class InComeSerializer(serializers.ModelSerializer):
    # student=acser.StudentSerializer(read_only=True)
    class Meta:
        model=get_model(conf.INCOME)
        fields="__all__"

class InComeGetSerializer(serializers.ModelSerializer):
    student=acser.StudentSerializer(read_only=True)
    class Meta:
        model=get_model(conf.INCOME)
        fields="__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.EXPENSE)
        fields="__all__"
