from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf
from accounts import serializers as acser

class StudentDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.STUDENT_DEBT)
        fields="__all__"

class StudentGetDebtSerializer(serializers.ModelSerializer):
    student=acser.StudentSerializer(read_only=True)
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
    user_dict=serializers.SerializerMethodField("user_serializer")
    class Meta:
        model=get_model(conf.EXPENSE)
        fields="__all__"
    
    def user_serializer(self,obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.user
        serializer = acser.UserSerializer(user, many=False, context=serializer_context)
        return serializer.data
