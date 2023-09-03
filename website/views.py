from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import DavomatFilter
from .models import Expense, InCome, Science, Type_of_Admin,Permission,Admin,\
    Teacher,Employer,Student,Parent,Chat_room,Message,Davomat,\
    Student_Pay
from .serializers import AdminUpdateSerializer, EmployerUpdateSerializer, InCome_Serializer, \
    ParentUpdateSerializer, Scince_Serializer, StudentUpdateSerializer, TeacherUpdateSerializer, \
    Type_of_Admin_Serializer,Permission_Serializer,AdminSerializer,\
    TeacherSerializer,EmployerSerializer,StudentSerializer,ParentSerializer,\
    ChatRoomSerializer,MessageSerializer,DavomatSerializer,\
    Student_Pay_Serializer,Expense_Serializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models.signals import post_delete
from django.dispatch import receiver
import datetime

def get_date(types):
    current_date = datetime.datetime.now()
    # formatted_date = current_date.strftime("%Y_%m_%d")
    if types=="year":
        return current_date.year
    elif types=="month":
        return current_date.month
    elif types=="week":
        return current_date.isocalendar()[1]
    elif types=="day":
        return current_date.day


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        amount=int(request.data['summa'])
        income_general=InCome.objects.get_or_create(types="GENERAL")
        income_general[0].amount+=amount
        income_general[0].save()
        income_yearly=InCome.objects.get_or_create(types="YEARLY",date__year=get_date("year"))
        income_yearly[0].amount+=amount
        income_yearly[0].save()
        income_monthly=InCome.objects.get_or_create(types="MONTHLY",date__month=get_date("month"))
        income_monthly[0].amount+=amount
        income_monthly[0].save()
        income_weekly=InCome.objects.get_or_create(types="WEEKLY",date__week=get_date("week"))
        income_weekly[0].amount+=amount
        income_weekly[0].save()
        income_daily=InCome.objects.get_or_create(types="DAILY",date__day=get_date("day"))
        income_daily[0].amount+=amount
        income_daily[0].save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # print(request.data)
        amount=int(request.data['summa'])
        income_general=InCome.objects.get_or_create(types="GENERAL")
        income_general[0].amount+=amount
        income_general[0].save()
        income_yearly=InCome.objects.get_or_create(types="YEARLY",date__year=get_date("year"))
        income_yearly[0].amount+=amount
        income_yearly[0].save()
        income_monthly=InCome.objects.get_or_create(types="MONTHLY",date__month=get_date("month"))
        income_monthly[0].amount+=amount
        income_monthly[0].save()
        income_weekly=InCome.objects.get_or_create(types="WEEKLY",date__week=get_date("week"))
        income_weekly[0].amount+=amount
        income_weekly[0].save()
        income_daily=InCome.objects.get_or_create(types="DAILY",date__day=get_date("day"))
        income_daily[0].amount+=amount
        income_daily[0].save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class InComeView(ModelViewSet):
    queryset=InCome.objects.all()
    serializer_class=InCome_Serializer
    filterset_fields=["types"]

    def list(self, request, *args, **kwargs):
        # print(Student_Pay.objects.latest('date').date)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # filterset_fields=["id","title","slug"]
    # ["tasischi","manager","finance","admin","teacher","employer","student","parent"]

class ExpenseView(ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class=Expense_Serializer
    filterset_fields=["types"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        amount=int(request.data['amount'])
        income_general=InCome.objects.get_or_create(types="GENERAL")
        if income_general[0].amount>amount:
            income_general[0].amount-=amount
            income_general[0].save()
            exponse_yearly=InCome.objects.get_or_create(types="YEARLY",date__year=get_date("year"))
            exponse_yearly[0].amount-=amount
            exponse_yearly[0].save()
            exponse_monthly=InCome.objects.get_or_create(types="MONTHLY",date__month=get_date("month"))
            exponse_monthly[0].amount-=amount
            exponse_monthly[0].save()
            exponse_weekly=InCome.objects.get_or_create(types="WEEKLY",date__week=get_date("week"))
            exponse_weekly[0].amount-=amount
            exponse_weekly[0].save()
            exponse_daily=InCome.objects.get_or_create(types="DAILY",date__day=get_date("day"))
            exponse_daily[0].amount-=amount
            exponse_daily[0].save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # print(request.data)
        amount=int(request.data['amount'])
        income_general=InCome.objects.get_or_create(types="GENERAL")
        if income_general[0].amount>amount:
            income_general[0].amount-=amount
            income_general[0].save()
            exponse_yearly=InCome.objects.get_or_create(types="YEARLY",date__year=get_date("year"))
            exponse_yearly[0].amount-=amount
            exponse_yearly[0].save()
            exponse_monthly=InCome.objects.get_or_create(types="MONTHLY",date__month=get_date("month"))
            exponse_monthly[0].amount-=amount
            exponse_monthly[0].save()
            exponse_weekly=InCome.objects.get_or_create(types="WEEKLY",date__week=get_date("week"))
            exponse_weekly[0].amount-=amount
            exponse_weekly[0].save()
            exponse_daily=InCome.objects.get_or_create(types="DAILY",date__day=get_date("day"))
            exponse_daily[0].amount-=amount
            exponse_daily[0].save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
