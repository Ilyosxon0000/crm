from django.db import models
from myconf import conf
from django.db.models import F,ExpressionWrapper

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
        print(pay)
        print(self.last().created_date)
        self.last().balance+=pay
        print(self.last().balance)
        self.last().save()
        # print(self.latest(field_name="created_date"))

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
        return f"username:{self.student.user.username};status:{self.status};summa:{self.balance};date:{self.created_date.month};"

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
        Finance.objects.create(
            student=self.student,
            each_pay=self,
            amount=self.paid,
            types_finance=Finance.INCOME,
            types=Finance.STUDENT_PAY
        )
        Student_Pay.objects.custom_update(self.student,self.paid)

class Finance(models.Model):
    EXPONSE="EXPONSE"
    INCOME="INCOME"
    STATUS_FINANCE=(
        (EXPONSE,"Chiqim"),
        (INCOME,"Kirim"),
    )
    SALARY="SALARY"
    STUDENT_PAY="STUDENT_PAY"
    OTHER="OTHER"
    STATUS=(
        (SALARY,"oylik maosh"),
        (STUDENT_PAY,"o'quvchilar to'lovi"),
        (OTHER,"boshqa"),
    )
    student=models.ForeignKey(conf.STUDENT,related_name='finance_pays',on_delete=models.CASCADE,blank=True,null=True)
    each_pay=models.ForeignKey(Each_Pay,related_name='finance_pays',on_delete=models.CASCADE)
    teacher=models.ForeignKey(conf.TEACHER,related_name='salaries',on_delete=models.CASCADE,blank=True,null=True)
    employer=models.ForeignKey(conf.EMPLOYER,related_name='salaries',on_delete=models.CASCADE,blank=True,null=True)
    admin=models.ForeignKey(conf.ADMIN,related_name='salaries',on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(default=0,verbose_name="pul miqdori:")
    types_finance=models.CharField(max_length=60,choices=STATUS,verbose_name="Chiqim yoki Kirim turi:")
    types=models.CharField(max_length=60,choices=STATUS_FINANCE,blank=True,null=True,verbose_name="(Chiqim,Kirim) turi:")
    comment=models.TextField(blank=True,null=True,verbose_name="Chiqim sababi:")
    date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.types==self.INCOME and self.types_finance==self.STUDENT_PAY:
            self.amount=self.each_pay.paid
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.types}:{self.amount}."
    
    def get_date(self,types):
        if types=="year":
            return self.date.year
        elif types=="month":
            return self.date.month
        elif types=="week":
            return self.date.isocalendar()[1]
        elif types=="week_day":
            return self.date.weekday
        elif types=="day":
            return self.date.day
    
    
    class Meta:
        verbose_name_plural="Finance"
