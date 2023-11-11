from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register("sciences",views.ScienceView,basename="sciences")
router.register(r"classes",views.ClassView,basename="classes")
router.register("attendances",views.AttendanceView,basename="attendances")
router.register("rooms",views.RoomView,basename="rooms")
router.register("lesson_times",views.Lesson_TimeView,basename="lesson_times")
router.register("lessons",views.LessonView,basename="lessons")
router.register("grades",views.GradeView,basename="grades")
router.register("tasks",views.TaskView,basename="tasks")
router.register("tasks_for_class",views.TaskForClassView,basename="tasks_for_class")
router.register("parent_comments",views.Parent_CommentView,basename="parent_comments")
router.register("teacher_lessons",views.Teacher_LessonView,basename="teacher_lessons")
router.register("questions",views.QuestionsView,basename="questions")
router.register("company",views.CompanyView,basename="company")

# urlpatterns = []+router.urls