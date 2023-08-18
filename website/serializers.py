from rest_framework import serializers
from .models import Type_of_Admin,Permission,Admin,Teacher,Employer,Student,Parent,Chat_room,Message,Davomat
from django.contrib.auth.models import User

def get_user(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.user
        serializer = UserSerializer(user, many=False, context=serializer_context)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id","username","email","first_name")

class SecondUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class Type_of_Admin_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Type_of_Admin
        fields="__all__"

class Permission_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields="__all__"

class AdminSerializer(serializers.ModelSerializer):
    type_dict=serializers.SerializerMethodField('get_type_dict')
    permissions_dict=serializers.SerializerMethodField('get_permissions_dict')
    user=SecondUserSerializer()
    # permission = Permission_Serializer(many=True, required=False)

    class Meta:
        model=Admin
        fields="__all__"

    def create(self, validated_data):
        permissions = validated_data.pop('permission', None)
        user_profile_data = validated_data.pop('user')
        user = User.objects.create(**user_profile_data)
        document = Admin.objects.create(user=user, **validated_data)
        if permissions:
            document.permissions.set(permissions)
        return document
      
    def get_type_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.types
        serializer = Type_of_Admin_Serializer(types, many=False, context=serializer_context)
        return serializer.data
    
    def get_permissions_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.permissions.all()
        if types:
            serializer = Permission_Serializer(types, many=True, context=serializer_context)
            return serializer.data
        else:
            return []

class AdminUpdateSerializer(serializers.ModelSerializer):
    type_dict=serializers.SerializerMethodField('get_type_dict')
    permissions_dict=serializers.SerializerMethodField('get_permissions_dict')

    class Meta:
        model=Admin
        fields="__all__"

    def get_type_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.types
        serializer = Type_of_Admin_Serializer(types, many=False, context=serializer_context)
        return serializer.data
    
    def get_permissions_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.permissions.all()
        if types:
            serializer = Permission_Serializer(types, many=True, context=serializer_context)
            return serializer.data
        else:
            return []

class TeacherSerializer(serializers.ModelSerializer):
    user=SecondUserSerializer()
    class Meta:
        model=Teacher
        fields="__all__"
    def create(self, validated_data):
        user_profile_data = validated_data.pop('user')
        user = User.objects.create(**user_profile_data)
        document = Teacher.objects.create(user=user, **validated_data)
        return document
    
class TeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields="__all__"

class EmployerSerializer(serializers.ModelSerializer):
    user=SecondUserSerializer()
    class Meta:
        model=Employer
        fields="__all__"

    def create(self, validated_data):
        user_profile_data = validated_data.pop('user')
        user = User.objects.create(**user_profile_data)
        document = Student.objects.create(user=user, **validated_data)
        return document
    
class EmployerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employer
        fields="__all__"
    
class StudentSerializer(serializers.ModelSerializer):
    user=SecondUserSerializer()
    class Meta:
        model=Student
        fields="__all__"
    
    def create(self, validated_data):
        user_profile_data = validated_data.pop('user')
        user = User.objects.create(**user_profile_data)
        document = Student.objects.create(user=user, **validated_data)
        return document
    
class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
    
class ParentSerializer(serializers.ModelSerializer):
    user=SecondUserSerializer()
    children_dict=serializers.SerializerMethodField('get_children_dict')

    class Meta:
        model=Parent
        fields="__all__"

    def create(self, validated_data):
        children = validated_data.pop('children', None)
        print(children)
        user_profile_data = validated_data.pop('user')
        user = User.objects.create(**user_profile_data)
        document = Parent.objects.create(user=user, **validated_data)
        if children:
            document.children.set(children)
        return document

    def get_children_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.children.all()
        serializer = StudentSerializer(types, many=True, context=serializer_context)
        return serializer.data
    
class ParentUpdateSerializer(serializers.ModelSerializer):
    children_dict=serializers.SerializerMethodField('get_children_dict')

    class Meta:
        model=Parent
        fields="__all__"

    def get_children_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.children.all()
        serializer = StudentSerializer(types, many=True, context=serializer_context)
        return serializer.data
    
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chat_room
        fields="__all__"

class MessageSerializer(serializers.ModelSerializer):
    from_user_dict=serializers.SerializerMethodField('get_from_user_dict')
    to_user_dict=serializers.SerializerMethodField('get_to_user_dict')
    chat_room_dict=serializers.SerializerMethodField('get_chat_room_dict')
    class Meta:
        model=Message
        fields=("id","chat_room","chat_room_dict","from_user_dict","to_user_dict","from_user","to_user","message","file_message","date","get_date","type_message")

    def get_from_user_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.from_user
        serializer = UserSerializer(user, many=False, context=serializer_context)
        return serializer.data
    
    def get_to_user_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        user = obj.to_user
        serializer = UserSerializer(user, many=False, context=serializer_context)
        return serializer.data
    
    def get_chat_room_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        chat_room = obj.chat_room
        serializer = ChatRoomSerializer(chat_room, many=False, context=serializer_context)
        return serializer.data
    
class DavomatSerializer(serializers.ModelSerializer):
    user_dict=serializers.SerializerMethodField('get_user_dict')
    class Meta:
        model=Davomat
        fields=("id","user","user_dict","davomat","date")
    
    def get_user_dict(self, obj):
        return get_user(self=self,obj=obj)
    