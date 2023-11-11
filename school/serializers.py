from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf


class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.SCIENCE)
        fields="__all__"

class ClassSerializer(serializers.ModelSerializer):
    teacher_object=serializers.SerializerMethodField('get_teacher_dict')
    room_name=serializers.SerializerMethodField('get_room_name')
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
    
    def get_room_name(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        room = obj.room
        if room:
            serializer = RoomSerializer(room, many=False, context=serializer_context)
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
    
class TaskForClassSerializer(serializers.ModelSerializer):
    from_teacher_object=serializers.SerializerMethodField('get_from_teacher_dict')
    to_class_object=serializers.SerializerMethodField('get_to_class_dict')
    class Meta:
        model=get_model(conf.TASK_FOR_CLASS)
        fields="__all__"
    
    def get_from_teacher_dict(self, obj):
        from accounts import serializers
        request = self.context.get('request')
        serializer_context = {'request': request }
        teacher = obj.from_teacher
        serializer = serializers.TeacherSerializer(teacher, many=False, context=serializer_context)
        return serializer.data
    
    def get_to_class_dict(self, obj):
        from accounts import serializers
        request = self.context.get('request')
        serializer_context = {'request': request }
        class_of_school = obj.to_class
        serializer = ClassSerializer(class_of_school, many=False, context=serializer_context)
        return serializer.data

class Parent_CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.PARENT_COMMENT)
        fields="__all__"
    
    def to_representation(self, instance):
        objs = super(Parent_CommentSerializer, self).to_representation(instance)
        objs['type'] = "question"
        if objs['admin']:
            objs['type'] = "answer"
        return objs

class Teacher_LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.TEACHER_LESSON)
        fields="__all__"

class QuestionSerializer(serializers.ModelSerializer):
    answer=serializers.Field(write_only=True)
    option1=serializers.Field(write_only=True)
    option2=serializers.Field(write_only=True)
    option3=serializers.Field(write_only=True)
    option4=serializers.Field(write_only=True)
    options=serializers.SerializerMethodField(method_name="get_extra_info")
    science_name=serializers.CharField(source="science.title")
    # science_name=serializers.CharField(source="science.title")
    class Meta:
        model=get_model(conf.QUESTION)
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        
        is_teacher = (
            self.context.get("request").user.type_user != "student" 
            if self.context.get("request").user.is_authenticated and hasattr(self.context.get("request").user, 'type_user') 
            else False
        )
        if is_teacher:
            self.fields['answer']=serializers.CharField()

    def get_extra_info(self, obj):
            import random
            options=[
                obj.option1,
                obj.option2,
                obj.option3,
                obj.option4,
                ]
            random.shuffle(options)
            return options

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.COMPANY)
        fields="__all__"

