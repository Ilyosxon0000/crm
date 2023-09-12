from django.contrib.auth import get_user_model
from myconf.conf import get_model,get_type_name_field
from myconf import conf
from rest_framework.viewsets import ModelViewSet
from . import serializers
from rest_framework.response import Response
from django.db import models
from rest_framework import status
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
def global_update(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    instance = self.get_object()
    data = request.data
    if data.get('user.username',False):
        queryset = queryset.filter(user__username=data['user.username'])
        if len(queryset)!=True:
            instance.user.username=data['user.username']
            instance.user.save()
    if type(data.get('user.image'))!=str:
        user_data = {
            'first_name': data.get('user.first_name'),
            'last_name': data.get('user.last_name'),
            'middle_name': data.get('user.middle_name'),
            'type_user': data.get('user.type_user'),
            'image': data.get('user.image'),
        }
    else:
        user_data = {
            'first_name': data.get('user.first_name'),
            'last_name': data.get('user.last_name'),
            'middle_name': data.get('user.middle_name'),
            'type_user': data.get('user.type_user'),
        }
    user_serializer = serializers.UserSerializer(instance=instance.user, data=user_data, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()

    model=kwargs['model']
    types=kwargs['types']
    file_fields = get_type_name_field(model,types)
    del_key=[]
    my_dict=data.dict()
    for key in my_dict.keys():
        if key in file_fields:
            if type(data[key])==str:
                del_key.append(key)
    for item in del_key:
        my_dict.pop(item)
    serializer = self.get_serializer(instance, data=my_dict, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    return serializer

class UserView(ModelViewSet):
    queryset=get_user_model().objects.all()
    serializer_class=serializers.UserSerializer


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username',  # parameter name
                openapi.IN_QUERY,
                description="Username to check",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    @action(detail=False, methods=['GET'])
    def check_username_exists(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({"error": "Username parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username already exists in the database
        user_exists = get_user_model().objects.filter(username=username).exists()

        if user_exists:
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class Type_of_Admin_View(ModelViewSet):
    queryset=get_model(conf.TYPE_OF_ADMIN).objects.all()
    serializer_class=serializers.Type_of_Admin_Serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class Permission_View(ModelViewSet):
    queryset=get_model(conf.PERMISSION).objects.all()
    serializer_class=serializers.Permission_Serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

@receiver(post_delete)
def delete_user(sender, instance, **kwargs):
    if hasattr(instance, 'user'):
        instance.user.delete()

class Admin_View(ModelViewSet):
    queryset=get_model(conf.ADMIN).objects.all()
    serializer_class=serializers.AdminSerializer

    def update(self, request, *args, **kwargs):
        serializer=global_update(self, request, *args, **kwargs,model=conf.ADMIN,types=models.FileField)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class Teacher_View(ModelViewSet):
    queryset=get_model(conf.TEACHER).objects.all()
    serializer_class=serializers.TeacherSerializer

    def update(self, request, *args, **kwargs):
        serializer=global_update(self, request, *args, **kwargs,model=conf.TEACHER,types=models.FileField)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class Employer_View(ModelViewSet):
    queryset=get_model(conf.EMPLOYER).objects.all()
    serializer_class=serializers.EmployerSerializer

    def update(self, request, *args, **kwargs):
        serializer=global_update(self, request, *args, **kwargs,model=conf.EMPLOYER,types=models.FileField)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class Student_View(ModelViewSet):
    queryset=get_model(conf.STUDENT).objects.all()
    serializer_class=serializers.StudentSerializer

    def update(self, request, *args, **kwargs):
        serializer=global_update(self, request, *args, **kwargs,model=conf.STUDENT,types=models.FileField)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class Parent_View(ModelViewSet):
    queryset=get_model(conf.PARENT).objects.all()
    serializer_class=serializers.ParentSerializer

    def update(self, request, *args, **kwargs):
        serializer=global_update(self, request, *args, **kwargs,model=conf.PARENT,types=models.FileField)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)