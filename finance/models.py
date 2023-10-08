from django.db import models
from django.contrib.auth import get_user_model
from myconf import conf
# Create your models here.

class Expense(models.Model):
    user=models.ForeignKey(get_user_model(),related_name="salaries",on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(default=0)
    comment=models.TextField(blank=True,null=True,default="oylik",verbose_name="Chiqim sababi:")
    date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        comment=f"ushbu xodimga {self.user.get_username()},{self.comment}" if self.user else self.comment  # noqa: E501
        return f"Chiqim sababi{comment}"

class Student_PayManager(models.Manager):
    def custom_create(self, *args,**kwargs):
        sum=0
        instance_tuple = self.get_or_create(*args,**kwargs,created_date__year=conf.get_date("year"),created_date__month=conf.get_date("month"))
        instance=instance_tuple[0]
        if instance_tuple[1]:
            instance.balance=instance.cost
            if instance.student.amount>0:
                sum+=instance.student.amount
                instance.balance=instance.cost+sum
                instance.student.amount=instance.balance
            else:
                instance.student.amount+=instance.balance
            instance.save()
            instance.student.save()
        return instance
    
    def custom_update(self,student,pay):
        costs=self.filter(student=student,status=Student_Pay.NO_PAID)
        student.amount+=pay
        student.save()
        for cost in costs:
            if pay>=abs(cost.balance):
                pay+=cost.balance
                cost.balance=0
                cost.save()
            elif pay>0:
                cost.balance+=pay
                cost.save()
                pay=0
        last_object = self.last()
        if last_object:
            last_object.balance+=pay
            last_object.save()

    def bug_fix(self,instance, new_value):
        sum=0
        instance.balance=instance.cost
        if instance.student.amount>0:
            sum+=instance.student.amount
        if instance.tolovlar.exists():
            all = instance.tolovlar.all()
            for i in all:
                sum += i.paid
        instance.balance=instance.cost+sum
        instance.student.amount=instance.balance
        instance.save()
        instance.student.save()
        return instance
    
class Student_Pay(models.Model):
    PAID="PAID" 
    NO_PAID="NO_PAID"#DID not paid
    STATUS=(
        (PAID,"to'lagan"),
        (NO_PAID,"to'lamagan")
    )
    student=models.ForeignKey(conf.STUDENT,related_name='pays',on_delete=models.CASCADE)
    status=models.CharField(max_length=255,choices=STATUS,verbose_name="holat:",default=NO_PAID)
    cost=models.IntegerField(default=0)
    balance=models.IntegerField(default=0)
    created_date=models.DateTimeField(blank=True,null=True)
    change_date=models.DateTimeField(auto_now=True)

    objects = Student_PayManager()

    def __str__(self):
        return f"username:{self.student.user.username};status:{self.status};summa:{self.balance};"#

    def save(self, *args, **kwargs):
        if self.balance>=0:
            self.status=self.PAID
        else:
            self.status=self.NO_PAID
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural="O'quvchi To'lovlari"

class Each_Pay(models.Model):
    student=models.ForeignKey(conf.STUDENT,related_name='each_pays',on_delete=models.CASCADE)
    paid = models.IntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    change_date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.student.user.username} - {self.paid} som'

    def save(self, *args, **kwargs):
        super(Each_Pay, self).save(*args, **kwargs)
        Student_Pay.objects.custom_update(self.student,self.paid)
