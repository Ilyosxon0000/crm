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
        serializer = TeacherSerializer(teacher, many=False, context=serializer_context)
        return serializer.data


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
    
    def get_from_user_dict(self, obj):
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
        print(objs['admin'])
        objs['type'] = "question"
        if objs['admin']:
            objs['type'] = "answer"
        return objs

class Teacher_LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.TEACHER_LESSON)
        fields="__all__"