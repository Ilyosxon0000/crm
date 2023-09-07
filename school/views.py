from myconf.conf import get_model
from myconf import conf
from rest_framework.viewsets import ModelViewSet
from . import serializers

# Create your views here.

class ScienceView(ModelViewSet):
    queryset=get_model(conf.SCIENCE).objects.all()
    serializer_class=serializers.ScienceSerializer

class ClassView(ModelViewSet):
    queryset=get_model(conf.CLASS).objects.all()
    serializer_class=serializers.ClassSerializer

class AttendanceView(ModelViewSet):
    queryset=get_model(conf.ATTENDANCE).objects.all()
    serializer_class=serializers.AttendanceSerializer

class RoomView(ModelViewSet):
    queryset=get_model(conf.ROOM).objects.all()
    serializer_class=serializers.RoomSerializer

class Lesson_TimeView(ModelViewSet):
    queryset=get_model(conf.LESSON_TIME).objects.all()
    serializer_class=serializers.Lesson_Time_Serializer

class LessonView(ModelViewSet):
    queryset=get_model(conf.LESSON).objects.all()
    serializer_class=serializers.Lesson_Serializer

class GradeView(ModelViewSet):
    queryset=get_model(conf.GRADE).objects.all()
    serializer_class=serializers.Grade_Serializer
