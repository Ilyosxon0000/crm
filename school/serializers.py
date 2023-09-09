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
    begin_time=serializers.TimeField(format='%H:%M')
    end_time=serializers.TimeField(format='%H:%M')
    class Meta:
        model=get_model(conf.LESSON_TIME)
        fields="__all__"

class Lesson_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.LESSON)
        fields="__all__"

class TableLessonSerializer(serializers.Serializer):
    # current_date = serializers.CharField() 

    class Meta:
        model = get_model(conf.LESSON)
        fields = ('id', 'lesson_date', 'teacher', 'science', 'student_class', 'room', 'lesson_time')

    
class Grade_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.GRADE)
        fields="__all__"