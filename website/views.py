from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import DavomatFilter
from .models import Expense, Science, Type_of_Admin,Permission,Admin,\
    Teacher,Employer,Student,Parent,Chat_room,Message,Davomat,\
    Student_Pay
from .serializers import AdminUpdateSerializer, EmployerUpdateSerializer, \
    ParentUpdateSerializer, Scince_Serializer, StudentUpdateSerializer, TeacherUpdateSerializer, \
    Type_of_Admin_Serializer,Permission_Serializer,AdminSerializer,\
    TeacherSerializer,EmployerSerializer,StudentSerializer,ParentSerializer,\
    ChatRoomSerializer,MessageSerializer,UserSerializer,DavomatSerializer,\
    Student_Pay_Serializer,Expense_Serializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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

@receiver(post_delete, sender=Admin)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()

class AdminView(ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Admin.objects.all()
    serializer_class=AdminSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return AdminUpdateSerializer
        return AdminSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success":"true"},status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        # Handling GET requests with query parameters
        queryset = self.filter_queryset(self.get_queryset())
        
        # Extract query parameters
        username = self.request.GET.get('username')

        if username:
            queryset = queryset.filter(user__username=username)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ScienceView(ModelViewSet):
    queryset=Science.objects.all()
    serializer_class=Scince_Serializer
    filterset_fields=["id","title","slug"]

class TeacherView(ModelViewSet):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer

    def update(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data=request.data

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if data.get('user.username',False):
            queryset = queryset.filter(user__username=data['user.username'])
            if len(queryset)!=True:
                instance.user.username=data['user.username']
                instance.user.save()
        
        file_field=[
            'image','language_certificate','lens','id_card_photo',
            'survey','biography','medical_book','picture_3x4',"my_image"
        ]
        del_key=[]

        my_dict=data.dict()
        
        for key in my_dict.keys():
            if key in file_field:
                if type(data[key])==str:
                    del_key.append(key)
        for item in del_key:
            my_dict.pop(item)
        # Bu Comment
        serializer = self.get_serializer(instance, data=my_dict, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
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

from django.db.models import Q

class DavomatView(ModelViewSet):
    queryset = Davomat.objects.all()
    serializer_class = DavomatSerializer
    filterset_class = DavomatFilter

    def get_queryset(self):
        queryset = self.queryset
        type_user = self.request.GET.get('type')
        type_list = ["tasischi", "manager", "finance", "admin", "employer"]

        if type_user and type_user in type_list:
            # Create a list of Q objects
            q_objects = [Q(user__first_name=i) for i in type_list]
            # Combine the Q objects using the OR operator
            combined_q_object = q_objects.pop()
            for q_obj in q_objects:
                combined_q_object |= q_obj
            # Apply the combined Q object to the queryset
            queryset = queryset.filter(combined_q_object)
        elif type_user:
            queryset = queryset.filter(user__first_name=type_user)
        return queryset
    
    def update(self, request, *args, **kwargs):
        return Response({"message":"Ushbu amal bloklangan!"},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"message":"Ushbu amal bloklangan!"},status=status.HTTP_400_BAD_REQUEST)


class Student_PayView(ModelViewSet):
    queryset=Student_Pay.objects.all()
    serializer_class=Student_Pay_Serializer

class ExpenseView(ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class=Expense_Serializer
    # filterset_fields=["id","title","slug"]
    # ["tasischi","manager","finance","admin","teacher","employer","student","parent"]
