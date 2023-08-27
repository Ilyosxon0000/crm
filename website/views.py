from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import DavomatFilter
from .models import Science, Type_of_Admin,Permission,Admin,\
    Teacher,Employer,Student,Parent,Chat_room,Message,Davomat,\
    Student_Pay
from .serializers import AdminUpdateSerializer, EmployerUpdateSerializer, \
    ParentUpdateSerializer, Scince_Serializer, StudentUpdateSerializer, TeacherUpdateSerializer, \
    Type_of_Admin_Serializer,Permission_Serializer,AdminSerializer,\
    TeacherSerializer,EmployerSerializer,StudentSerializer,ParentSerializer,\
    ChatRoomSerializer,MessageSerializer,UserSerializer,DavomatSerializer,\
    Student_Pay_Serializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.settings import api_settings


class Users(APIView):
    serializer_class=UserSerializer
    filterset_fields=["first_name"]
    permission_classes=[AllowAny]
    def get(self,request,*args,**kwargs):
        mydict={
        "example":
        {
            "admin":{
                "user": {
                    "username": "username //required",
                    "password": "password //required"
                },
                "type": "admin //required",
                "model": {
                    "first_name": "ism //required",
                    "last_name": "familiya //required",
                    "admin_type": "id //required",
                    'permission':"[1,2,3] //optional"
                }
            },
            "teacher":{
                "user": {
                    "username": "username //required",
                    "password": "password //required"
                },
                "type": "teacher //required",
                "model": {
                    "first_name": "ism //required",
                    "last_name": "familiya //required",
                    "lavozim": "lavozim //required",
                }
            },
            "employer":{
                "user": {
                    "username": "username //required",
                    "password": "password //required"
                },
                "type": "employer //required",
                "model": {
                    "first_name": "ism //required",
                    "last_name": "familiya //required",
                    "lavozim": "lavozim //required",
                }
            },
            "student":{
                "user": {
                    "username": "username //required",
                    "password": "password //required"
                },
                "type": "student //required",
                "model": {
                    "first_name": "ism //required",
                    "last_name": "familiya //required",
                }
            },
            "parent":{
                "user": {
                    "username": "username //required",
                    "password": "password //required"
                },
                "type": "parent //required",
                "model": {
                    "first_name": "ism //required",
                    "last_name": "familiya //required",
                    "children":"[1,2,3] //optional"
                }
            },
        }
    }
        return Response(mydict,status=200)
    def post(self,request,*args,**kwargs):
        user=request.data["user"]
        user_type=request.data['type']
        data=dict(request.data)['model']
        try:
            
            match user_type:
                case 'admin':
                    myuser=User.objects.create_user(username=user['username'],password=user['password'],first_name=Type_of_Admin.objects.get(id=data['admin_type']))#user_type
                    admin=Admin.objects.create(user=myuser,first_name=data['first_name'],last_name=data['last_name'],types=Type_of_Admin.objects.get(id=data['admin_type']))
                    if data.get("permission"):
                        for i in data.get("permission"):
                            admin.permissions.add(Permission.objects.get(id=i))
                    serializer=AdminSerializer(admin,many=False)
                    return Response({"teacher":serializer.data})
                case 'teacher':
                    myuser=User.objects.create_user(username=user['username'],password=user['password'],first_name=user_type)
                    teacher=Teacher.objects.create(user=myuser,first_name=data['first_name'],last_name=data['last_name'],lavozim=data['lavozim'])
                    serializer=TeacherSerializer(teacher,many=False)
                    return Response({"teacher":serializer.data})
                case 'employer':
                    myuser=User.objects.create_user(username=user['username'],password=user['password'],first_name=user_type)
                    teacher=Employer.objects.create(user=myuser,first_name=data['first_name'],last_name=data['last_name'],lavozim=data['lavozim'])
                    serializer=EmployerSerializer(teacher,many=False)
                    return Response({"employer":serializer.data})
                case 'student':
                    myuser=User.objects.create_user(username=user['username'],password=user['password'],first_name=user_type)
                    student=Student.objects.create(user=myuser,first_name=data['first_name'],last_name=data['last_name'])
                    serializer=StudentSerializer(student,many=False)
                    return Response({"student":serializer.data})
                case 'parent':
                    myuser=User.objects.create_user(username=user['username'],password=user['password'],first_name=user_type)
                    parent=Parent.objects.create(user=myuser,first_name=data['first_name'],last_name=data['last_name'])
                    if data.get("children"):
                        for i in data.get("children"):
                            parent.children.add(Student.objects.get(id=i))
                    serializer=ParentSerializer(parent,many=False)
                    return Response({"parent":serializer.data})
        except:
            myuser.delete()
            return Response({"result":"nimadir xato ketdi!!!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(request.data,status=200)

class StudentxlsView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,*args,**kwargs):

        return Response(request.data,status=200)

class TypeView(ModelViewSet):
    queryset=Type_of_Admin.objects.all()
    serializer_class=Type_of_Admin_Serializer
    filterset_fields=["id","title","slug"]

class PermissionView(ModelViewSet):
    queryset=Permission.objects.all()
    serializer_class=Permission_Serializer
    

class AdminView(ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Admin.objects.all()
    serializer_class=AdminSerializer

    def create(self, request, *args, **kwargs):
        print("ishladi create")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data,"success":"true"}, status=status.HTTP_201_CREATED, headers=headers)


    def get_serializer_class(self):
        if self.action == 'update':
            return AdminUpdateSerializer
        return AdminSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class ScienceView(ModelViewSet):
    queryset=Science.objects.all()
    serializer_class=Scince_Serializer
    filterset_fields=["id","title","slug"]

class TeacherView(ModelViewSet):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer

    def create(self, request, *args, **kwargs):
        print("Function is working")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data,"success":"true"}, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == 'update':
            return TeacherUpdateSerializer
        return TeacherSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class EmployerView(ModelViewSet):
    queryset=Employer.objects.all()
    serializer_class=EmployerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data,"success":"true"}, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == 'update':
            return EmployerUpdateSerializer
        return EmployerSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class StudentView(ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data,"success":"true"}, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == 'update':
            return StudentUpdateSerializer
        return StudentSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class ParentView(ModelViewSet):
    queryset=Parent.objects.all()
    serializer_class=ParentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data,"success":"true"}, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == 'update':
            return ParentUpdateSerializer
        return ParentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)

class ChatRoomeView(ModelViewSet):
    queryset=Chat_room.objects.all()
    serializer_class=ChatRoomSerializer

class MessageView(ModelViewSet):
    queryset=Message.objects.all()
    serializer_class=MessageSerializer
    filterset_fields=["chat_room","from_user","to_user","message",'date']

class DavomatView(ModelViewSet):
    queryset=Davomat.objects.all()
    serializer_class=DavomatSerializer
    
    filterset_class=DavomatFilter

    def get_queryset(self):
        if self.request.GET.get('type'):
            type_user=self.request.GET.get('type')
            data=self.queryset.filter(user__first_name=type_user)
            return data
        return self.queryset
        
    # def list(self, request, *args, **kwargs):
    #     print(request.method)
    #     queryset = self.filter_queryset(self.get_queryset())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)  
    # filterset_fields=["user","davomat",'date']

class Student_PayView(ModelViewSet):
    queryset=Student_Pay.objects.all()
    serializer_class=Student_Pay_Serializer
    # filterset_fields=["id","title","slug"]