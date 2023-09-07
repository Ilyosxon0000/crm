from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf

class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.SCIENCE)
        fields="__all__"

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.CLASS)
        fields="__all__"

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.ATTENDANCE)
        fields="__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.ROOM)
        fields="__all__"

class Lesson_Time_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.LESSON_TIME)
        fields="__all__"

class Lesson_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.LESSON)
        fields="__all__"

class Grade_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.GRADE)
        fields="__all__"