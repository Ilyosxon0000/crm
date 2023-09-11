from rest_framework.decorators import api_view
from rest_framework.response import Response
from myconf import conf
from django.contrib.auth import get_user_model
from myconf.conf import get_model

@api_view(['GET'])
def davomat_users(request):
    if request.method == 'GET':
        users=get_user_model().objects.all()
        for user in users:
            davomat=get_model(conf.ATTENDANCE).objects.create(user=user)
        return Response({"message": "succesfully"})
    
@api_view(['GET'])
def students_pays(request):
    money=-1000_000
    if request.method == 'GET':
        students=get_model(conf.STUDENT).objects.all()
        for student in students:
            student_pay=get_model(conf.STUDENT_PAY).objects.create(student=student,amount_2=money)
            print(student_pay.status)
        return Response({"message": "succesfully"})