from rest_framework import serializers
from myconf.conf import get_model
from myconf import conf
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, style={"input_type": "password"},write_only=True)
    type_user=serializers.ReadOnlyField()
    class Meta:
        model=get_user_model()
        fields=[
            "id",
            "username",
            "password",
            "image",
            "first_name",
            "last_name",
            "middle_name",
            "type_user"
            ]
        extra_kwargs = {'password': {'write_only': True}}
      
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

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

    class Meta:
        model=get_model(conf.ADMIN)
        fields="__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        permissions_data = validated_data.pop('permissions', [])  # Extract permissions data (if provided)
        
        user_instance = UserSerializer().create(user_data)  # Create user

        # Create admin
        admin = get_model(conf.ADMIN).objects.create(user=user_instance, **validated_data)

        # Set permissions using the .set() method
        admin.permissions.set(permissions_data)

        return admin
    
class TeacherSerializer(serializers.ModelSerializer):
    user=UserSerializer()

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

    class Meta:
        model=get_model(conf.STUDENT)
        fields="__all__"
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data
        user_instance = UserSerializer().create(user_data)  # Create user
        student = get_model(conf.STUDENT).objects.create(user=user_instance, **validated_data)
        return student

class ParentSerializer(serializers.ModelSerializer):
    user=UserSerializer()

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

