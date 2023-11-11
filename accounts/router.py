from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register("users",views.UserView,basename="user")
router.register("types-admin",views.Type_of_Admin_View,basename="types")
router.register("permissions-admin",views.Permission_View,basename="permissions")
router.register("admins",views.Admin_View,basename="admins")
router.register("teachers",views.Teacher_View,basename="teachers")
router.register("employers",views.Employer_View,basename="employers")
router.register("students",views.Student_View,basename="students")
router.register("parents",views.Parent_View,basename="parents")