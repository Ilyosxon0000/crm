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
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models import Count

# Create your views here.
def global_update(self, request, *args, **kwargs):
    # print(request.data)
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
    user_serializer.update(instance.user,user_data)

    model=kwargs['model']
    types=kwargs['types']
    file_fields = get_type_name_field(model,types)
    del_key=['user.username',"permissions"]
    my_dict=request.data.dict()
    for key in my_dict.keys():
        if key in file_fields:
            if type(data[key])==str:
                del_key.append(key)
    for item in del_key:
        my_dict.pop(item)

    myDict = {}
    for key in request.data.keys():
        myDict[key] = request.data.getlist(key)

    # print(dict(request.data).get("permissions",[]))
    # print(request.data["permissions"])
    print(myDict)
    
    # print(dict(request.data).get("permissions",False))

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
    @action(detail=False, methods=['GET'])
    def teachers_for_class(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        teachers_with_classes = queryset.annotate(num_classes=Count('sinflar'))
        for teacher in teachers_with_classes:
            if teacher.num_classes == 0:
                serializer = self.get_serializer(teacher, many=False)
                return Response(serializer.data)
        return Response({"message":"We haven't teachers"})

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
    @swagger_auto_schema(
        operation_summary="Upload a single file.",
        operation_description="Upload a single file using multipart/form-data.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['students_table'],
            properties={
                'students_table': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    format=openapi.FORMAT_BINARY,  # Specify binary format
                    description="The allowed extensions excel(xls,xlsx)."
                )
            }
        ),
        consumes=["multipart/form-data"],  # Set the content type
        responses={
            status.HTTP_201_CREATED: "File uploaded successfully.",
            status.HTTP_400_BAD_REQUEST: "Bad request.",
        }
    )
    @action(detail=False, methods=['POST'])
    def add_student_with_excel(self, request):
        uploaded_file = request.data.get('students_table')
        print(uploaded_file)

        if not uploaded_file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        allowed_extensions = ['xls', 'xlsx']
        file_name = uploaded_file.name
        file_extension = file_name.split('.')[-1].lower()

        if not any(file_extension == ext for ext in allowed_extensions):
            return Response({"error": "Invalid file extension."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    
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


class StudentxlsView(APIView):
    def get(self,request,*args,**kwargs):
        return Response({"message":"FormData","student_table":"student_table.xls"},status=200)
    
    def post(self,request,*args,**kwargs):
        return Response(request.data,status=200)


class General_Statistics(APIView):
    def get(self,request,*args,**kwargs):
        data={
            "admins":len(get_model(conf.ADMIN).objects.all()),
            "teachers":len(get_model(conf.TEACHER).objects.all()),
            "employers":len(get_model(conf.EMPLOYER).objects.all()),
            "students":len(get_model(conf.STUDENT).objects.all()),
        }
        return Response([data],status=200)
    