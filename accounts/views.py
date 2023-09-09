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

    # Update the user model with the extracted user_data
    user_serializer = serializers.UserSerializer(instance=instance.user, data=user_data, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()

    model=kwargs['model']
    types=kwargs['types']
    file_fields = get_type_name_field(model,types)
    print(file_fields)
    # data = {key: value for key, value in data.items() if key not in file_fields}
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

@receiver(post_delete, sender=conf.ADMIN)
def delete_user(sender, instance, **kwargs):
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

@receiver(post_delete, sender=conf.TEACHER)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
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

@receiver(post_delete, sender=conf.EMPLOYER)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
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

@receiver(post_delete, sender=conf.STUDENT)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
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

@receiver(post_delete, sender=conf.PARENT)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
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