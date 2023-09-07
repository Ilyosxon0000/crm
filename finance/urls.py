from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register("finances",views.FinanceView,basename="finances")
router.register("student_pay",views.Student_PayView,basename="student_pay")

urlpatterns = []+router.urls