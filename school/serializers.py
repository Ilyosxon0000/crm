from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf


class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.SCIENCE)
        fields="__all__"

class ClassSerializer(serializers.ModelSerializer):
    teacher_object=serializers.SerializerMethodField('get_teacher_dict')
    class Meta:
        model=get_model(conf.CLASS)
        fields="__all__"
    
    def get_teacher_dict(self, obj):
        from accounts.serializers import TeacherSerializer
        request = self.context.get('request')
        serializer_context = {'request': request }
        teacher = obj.teacher
        if teacher:
            serializer = TeacherSerializer(teacher, many=False, context=serializer_context)
            return serializer.data
        return None

class ClassForTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.CLASS)
        fields="__all__"

class AttendanceSerializer(serializers.ModelSerializer):
    user_object=serializers.SerializerMethodField('get_user_dict')
    class Meta:
        model=get_model(conf.ATTENDANCE)
        fields="__all__"
    def get_user_dict(self, obj):
        from accounts import serializers
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.user
        serializer = serializers.UserSerializer(user, many=False, context=serializer_context)
        return serializer.data

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
    lesson_time=serializers.SerializerMethodField('get_time_dict')
    fan=serializers.SerializerMethodField('get_fan_dict')


    class Meta:
        model=get_model(conf.LESSON)
        fields="__all__"
    
    def get_std_dict(self, obj):
        from school.serializers import ScienceSerializer
        request = self.context.get('request')
        serializer_context = {'request': request}
        # print(obj)
        student_class = obj.student_class
        if student_class:
            dic={
                "id":student_class.id,
                "title":student_class.title
            }
            return dic
        else:
            return {}
    def get_fan_dict(self, obj):
        from school.serializers import ScienceSerializer
        request = self.context.get('request')
        serializer_context = {'request': request}
        science = obj.science
        if science:
            return science.title
        else:
            return None
    def get_time_dict(self, obj):
        from school.serializers import ScienceSerializer
        request = self.context.get('request')
        serializer_context = {'request': request}
        lesson_time = obj.lesson_time
        if lesson_time:
            dic={
                "id":lesson_time.id,
                "begin_time":lesson_time.begin_time,
                "end_time":lesson_time.end_time
            }
            return dic
        else:
            return {}

class TableLessonSerializer(serializers.Serializer):
    # current_date = serializers.CharField() 

    class Meta:
        model = get_model(conf.LESSON)
        fields = ('id', 'lesson_date', 'teacher', 'science', 'student_class', 'room', 'lesson_time')

    
class Grade_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.GRADE)
        fields="__all__"

class TaskSerializer(serializers.ModelSerializer):
    from_user_object=serializers.SerializerMethodField('get_from_user_dict')
    to_user_object=serializers.SerializerMethodField('get_to_user_dict')
    class Meta:
        model=get_model(conf.TASK)
        fields="__all__"
    
    def get_from_user_dict(self, obj):
        from accounts import serializers
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.from_user
        serializer = serializers.UserSerializer(user, many=False, context=serializer_context)
        return serializer.data
    
    def get_to_user_dict(self, obj):
        from accounts import serializers
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.to_user
        serializer = serializers.UserSerializer(user, many=False, context=serializer_context)
        return serializer.data

class Parent_CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.PARENT_COMMENT)
        fields="__all__"
    
    def to_representation(self, instance):
        objs = super(Parent_CommentSerializer, self).to_representation(instance)
        # print(objs['admin'])
        objs['type'] = "question"
        if objs['admin']:
            objs['type'] = "answer"
        return objs

class Teacher_LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.TEACHER_LESSON)
        fields="__all__"

from django.conf import settings

class Teacher_LessonThemeSerializer(serializers.ModelSerializer):
    file_message = serializers.SerializerMethodField()

    class Meta:
        model = get_model(conf.TEACHER_LESSON)
        fields = ('id', 'message', 'file_message', 'date', 'teacher')

    def get_file_message(self, obj):
        base_url = settings.BASE_URL
        full_url = f"{base_url}{obj.file_message.url}"
        return full_url