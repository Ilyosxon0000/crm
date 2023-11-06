from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf
from django.contrib.auth import get_user_model
import os
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, style={"input_type": "password"},write_only=True)
    type_user=serializers.ReadOnlyField()
    full_type=serializers.SerializerMethodField('get_type_dict')
    is_active=serializers.ReadOnlyField()
    image_thumbnail = serializers.ImageField(read_only=True)
    class Meta:
        model=get_user_model()
        fields=[
            "id",
            "username",
            "password",
            "image",
            "image_thumbnail",
            "first_name",
            "last_name",
            "middle_name",
            "type_user",
            "full_type",
            "is_active",
            ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_type_dict(self,obj):
        type=obj.type_user
        if obj.type_user=="admin":
            type=obj.admin.types.slug
        return type
      
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserForFaceIDSerializer(serializers.ModelSerializer):
    is_active=serializers.ReadOnlyField()
    class Meta:
        model=get_user_model()
        fields=[
            "id",
            "username",
            "image",
            "is_active",
            ]
    def to_representation(self, instance):
        data = super(UserForFaceIDSerializer, self).to_representation(instance)
        if instance.image and instance.is_active:
            full_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
            data['image_full_path'] = full_path
        return data
      

class Type_of_Admin_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.TYPE_OF_ADMIN)
        fields="__all__"

class Permission_Serializer(serializers.ModelSerializer):
    class Meta:
        model=get_model(conf.PERMISSION)
        fields="__all__"

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    type_dict=serializers.SerializerMethodField('get_type_dict')
    permissions_dict=serializers.SerializerMethodField('get_permissions_dict')

    class Meta:
        model=get_model(conf.ADMIN)
        fields="__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        permissions_data = validated_data.pop('permissions', [])
        user_instance = UserSerializer().create(user_data)
        admin = get_model(conf.ADMIN).objects.create(user=user_instance, **validated_data)
        admin.permissions.set(permissions_data)
        return admin

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
    user=UserSerializer()
    sciences_dict=serializers.SerializerMethodField('get_sciences_dict')

    class Meta:
        model=get_model(conf.TEACHER)
        fields="__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        sciences_data = validated_data.pop('sciences', []) 
        user_instance = UserSerializer().create(user_data)  # Create user
        teacher = get_model(conf.TEACHER).objects.create(user=user_instance, **validated_data)
        teacher.sciences.set(sciences_data)
        return teacher
    
    def get_sciences_dict(self, obj):
        from school.serializers import ScienceSerializer
        request = self.context.get('request')
        serializer_context = {'request': request }
        sciences = obj.sciences.all()
        if sciences:
            serializer = ScienceSerializer(sciences, many=True, context=serializer_context)
            return serializer.data
        else:
            return []

class EmployerSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    class Meta:
        model=get_model(conf.EMPLOYER)
        fields="__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        user_instance = UserSerializer().create(user_data)  # Create user
        employer = get_model(conf.EMPLOYER).objects.create(user=user_instance, **validated_data)
        return employer

class StudentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    sinf=serializers.SerializerMethodField("get_sinf_dict")

    class Meta:
        model=get_model(conf.STUDENT)
        fields="__all__"
    
    def get_sinf_dict(self, obj):
        sinf = obj.class_of_school
        if sinf:
            return {
                "name":sinf.title,
                "teacher":{
                    "username":sinf.teacher.user.username,
                    "first_name":sinf.teacher.user.first_name,
                    "last_name":sinf.teacher.user.last_name,
                } if sinf.teacher else None,
                "id":sinf.id,
                "xona":sinf.room.name if sinf.room else None
            }
        else:
            return {}
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        user_instance = UserSerializer().create(user_data)  # Create user
        student = get_model(conf.STUDENT).objects.create(user=user_instance, **validated_data)
        return student

class ParentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    children_dict=serializers.SerializerMethodField('get_children_dict')

    class Meta:
        model=get_model(conf.PARENT)
        fields="__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        children = validated_data.pop('children', []) 
        user_instance = UserSerializer().create(user_data)  # Create user
        parent = get_model(conf.PARENT).objects.create(user=user_instance, **validated_data)
        parent.children.set(children)
        return parent

    def get_children_dict(self, obj):
        request = self.context.get('request')
        serializer_context = {'request': request }
        types = obj.children.all()
        serializer = StudentSerializer(types, many=True, context=serializer_context)
        return serializer.data