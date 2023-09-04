from django.urls import path
from .views import ExpenseView, ScienceView, TypeView,PermissionView,AdminView,TeacherView,\
    EmployerView,StudentView,ParentView,ChatRoomeView,MessageView,\
    DavomatView,Student_PayView,StudentxlsView,InComeView
from rest_framework.schemas import get_schema_view
from .router import MyRouter,Custom_List
from .token import TokenCreateView

Custom_List.append("token/login")
Custom_List.append("student/xlsx")

router=MyRouter()
router.register('type-admin',TypeView,basename='type-admin')
router.register('permission-admin',PermissionView,basename='permission')
router.register('custom-admin',AdminView,basename='admin')
router.register('science',ScienceView,basename='science')
router.register('teacher',TeacherView,basename='teacher')
router.register('employer',EmployerView,basename='employer')
router.register('student',StudentView,basename='student')
router.register('parent',ParentView,basename='parent')
router.register('chat-room',ChatRoomeView,basename='chat-room')
router.register('message',MessageView,basename='message')
router.register('davomat',DavomatView,basename='davomat')
router.register('student-pay',Student_PayView,basename='student-pay')
router.register('expense',ExpenseView,basename='expense')
router.register('incomde',InComeView,basename='income')


urlpatterns = [
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('token/login/',TokenCreateView.as_view()),
    path('student/xls/',StudentxlsView.as_view()),
]+router.urls
