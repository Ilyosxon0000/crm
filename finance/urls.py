from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register('student_debts',views.StudentDebtView,basename="student_debts")
router.register('incomes',views.InComeView,basename="incomes")
router.register('expenses',views.ExpenseView,basename="expenses")