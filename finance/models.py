from collections.abc import Iterable
from django.db import models
from myconf.conf import get_user_model
from myconf import conf
from .validation import EmployerTypeError
# Create your models here.

# This class is cron debt for student
class Student_Debt(models.Model):
    student=models.ForeignKey(conf.STUDENT,related_name="debts",on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    balance=models.IntegerField(default=0)
    paid=models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)

    def save(self,*args,**kwargs):
        self.paid=True if self.balance>=0 else False
        return super().save(*args,**kwargs)

# This class is in come
class InCome(models.Model):
    EACH_PAY="EACH_PAY"
    OTHER="OTHER"
    TYPE=(
        (EACH_PAY,"each_pay"),
        (OTHER,"other")
    )
    student=models.ForeignKey(conf.STUDENT,related_name="each_pays",on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(default=0)
    comment=models.TextField(blank=True,null=True)
    # this type var is extra
    type=models.CharField(max_length=50,choices=TYPE,blank=True,null=True)
    # created_date=models.DateField(blank=True,null=True)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)

# This class is in come
class Expense(models.Model):
    SALARY="SALARY"
    OTHER="OTHER"
    TYPE=(
        (SALARY,"salary"),
        (OTHER,"other")
    )
    user=models.ForeignKey(get_user_model(),related_name="salaries",on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(default=0)
    comment=models.TextField(blank=True,null=True)
    # this type var is extra
    type=models.CharField(max_length=50,choices=TYPE,blank=True,null=True)
    # created_date=models.DateField(blank=True,null=True)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.type_user in ["student","parent"]:
                return EmployerTypeError()
        super().save(*args, **kwargs)
