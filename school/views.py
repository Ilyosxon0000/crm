from myconf.conf import get_model
from myconf import conf
from rest_framework.viewsets import ModelViewSet
from . import serializers
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.
import datetime

def get_all_weeks_of_current_year():
    current_year = datetime.datetime.now().year
    all_weeks = set()

    for day in range(1, 366):  # Iterate through all days of the year
        current_date = datetime.date(current_year, 1, 1) + datetime.timedelta(days=day - 1)
        iso_week = current_date.isocalendar()[1]
        all_weeks.add(iso_week)

    return sorted(list(all_weeks))

class ScienceView(ModelViewSet):
    queryset=get_model(conf.SCIENCE).objects.all()
    serializer_class=serializers.ScienceSerializer

class ClassView(ModelViewSet):
    queryset=get_model(conf.CLASS).objects.all()
    serializer_class=serializers.ClassSerializer

class AttendanceView(ModelViewSet):
    queryset=get_model(conf.ATTENDANCE).objects.all()
    serializer_class=serializers.AttendanceSerializer
    def get_queryset(self):
        queryset = self.queryset
        type_user = self.request.GET.get('type')
        type_list = ["tasischi", "manager", "finance", "admin", "employer"]
        if type_user and type_user in type_list:
            q_objects = [Q(user__type_user=i) for i in type_list]
            combined_q_object = q_objects.pop()
            for q_obj in q_objects:
                combined_q_object |= q_obj
            queryset = queryset.filter(combined_q_object)
        elif type_user:
            queryset = queryset.filter(user__type_user=type_user)
        return queryset

class RoomView(ModelViewSet):
    queryset=get_model(conf.ROOM).objects.all()
    serializer_class=serializers.RoomSerializer

class Lesson_TimeView(ModelViewSet):
    queryset=get_model(conf.LESSON_TIME).objects.all()
    serializer_class=serializers.Lesson_Time_Serializer

def weekday_by_day(desired_weekday):
    current_date = datetime.date.today()
    weekday_number = current_date.weekday()
    days_until_desired_weekday = (desired_weekday - weekday_number) % 7
    desired_date = current_date + datetime.timedelta(days=days_until_desired_weekday)
    return desired_date

def weekday_by_week(desired_weekday):
    current_date = datetime.date.today()
    difference = current_date.weekday() - desired_weekday
    desired_date = current_date - datetime.timedelta(days=difference)
    return desired_date

class LessonView(ModelViewSet):
    queryset=get_model(conf.LESSON).objects.all()
    serializer_class=serializers.Lesson_Serializer
    week_days=[
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY"
        ]
    day_name_to_id = {
        "MONDAY": 0,
        "TUESDAY": 1,
        "WEDNESDAY": 2,
        "THURSDAY": 3,
        "FRIDAY": 4,
        "SATURDAY": 5,
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        week = self.request.GET.get("week")
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        elif week is not None and week in ["weekday_by_week","weekday_by_day"]:
            return self.week_list(self, request,week=week, *args, **kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def week_list(self, request, *args, **kwargs):
        data = []
        queryset = self.filter_queryset(self.get_queryset())
        lessons_by_day = {day: [] for day in self.week_days}
        for lesson in queryset.filter(lesson_date__in=self.week_days):
            lessons_by_day[lesson.lesson_date].append(lesson)
        for week_day, day_lessons in lessons_by_day.items():
            day_id = self.day_name_to_id.get(week_day, -1)
            day_items = self.get_serializer(day_lessons, many=True).data
            day_date=0
            week=kwargs['week']
            if week=="weekday_by_week":
                day_date=weekday_by_week(day_id)
            elif week=="weekday_by_day":
                day_date=weekday_by_day(day_id)
            data.append({
                "day_name": week_day,
                "date": day_date,
                "lessons": day_items
            })
        return Response(data)   

class GradeView(ModelViewSet):
    queryset=get_model(conf.GRADE).objects.all()
    serializer_class=serializers.Grade_Serializer

class TaskView(ModelViewSet):
    queryset=get_model(conf.TASK).objects.all()
    serializer_class=serializers.TaskSerializer
    filterset_fields="__all__"

class Parent_CommentView(ModelViewSet):
    queryset=get_model(conf.PARENT_COMMENT).objects.all()
    serializer_class=serializers.Parent_CommentSerializer
    filterset_fields="__all__"

class Teacher_LessonView(ModelViewSet):
    queryset=get_model(conf.TEACHER_LESSON).objects.all()
    serializer_class=serializers.Teacher_LessonSerializer

