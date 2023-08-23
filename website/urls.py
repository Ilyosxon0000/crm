from django.urls import path
from .views import ScienceView, TypeView,PermissionView,AdminView,TeacherView,\
    EmployerView,StudentView,ParentView,ChatRoomeView,MessageView,Users,\
    DavomatView
from rest_framework.schemas import get_schema_view
from .router import MyRouter,Custom_List
from .token import TokenCreateView

Custom_List.append("users")
Custom_List.append("token/login")

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


urlpatterns = [
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('users/',Users.as_view()),
    path('token/login/',TokenCreateView.as_view()),
]+router.urls
