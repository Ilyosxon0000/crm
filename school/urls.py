from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register("sciences",views.ScienceView,basename="sciences")
router.register("classes",views.ClassView,basename="classes")
router.register("attendances",views.AttendanceView,basename="attendances")
router.register("lesson_times",views.Lesson_TimeView,basename="lesson_times")
router.register("lessons",views.LessonView,basename="lessons")
router.register("grades",views.GradeView,basename="grades")

urlpatterns = []+router.urls