from rest_framework.routers import DefaultRouter
from . import views
from school import urls as school_urls
from finance import urls as finance_urls
from djoser.urls import authtoken
from django.urls import path
from finance.models import Student_Pay
from myconf.conf import get_model
from myconf import conf
from django.http.response import JsonResponse
from finance.views import FinanceView


router=DefaultRouter()
router.register("users",views.UserView,basename="user")
router.register("types-admin",views.Type_of_Admin_View,basename="types")
router.register("permissions-admin",views.Permission_View,basename="permissions")
router.register("admins",views.Admin_View,basename="admins")
router.register("teachers",views.Teacher_View,basename="teachers")
router.register("employers",views.Employer_View,basename="employers")
router.register("students",views.Student_View,basename="students")
router.register("parents",views.Parent_View,basename="parents")
def salom(req):
    students=get_model(conf.STUDENT).objects.all()
    for student in students:
        Student_Pay.objects.custom_create(student=student,cost=-100)
    return JsonResponse({"salom":"salom"})
urlpatterns = [
    path("salom/",salom),
    # path("finances/",FinanceView.as_view()),
    path("general_statistics/",views.General_Statistics.as_view())
]
urlpatterns+=router.urls
urlpatterns += school_urls.router.urls
urlpatterns += finance_urls.router.urls
urlpatterns += authtoken.urlpatterns

