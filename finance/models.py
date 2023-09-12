from django.db import models
from myconf import conf

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
    teacher=models.ForeignKey(conf.TEACHER,related_name='salaries',on_delete=models.CASCADE,blank=True,null=True)
    employer=models.ForeignKey(conf.EMPLOYER,related_name='salaries',on_delete=models.CASCADE,blank=True,null=True)
    admin=models.ForeignKey(conf.ADMIN,related_name='salaries',on_delete=models.CASCADE,blank=True,null=True)
    amount=models.IntegerField(default=0,verbose_name="pul miqdori:")
    types_finance=models.CharField(max_length=60,choices=STATUS,verbose_name="Chiqim yoki Kirim turi:")
    types=models.CharField(max_length=60,choices=STATUS_FINANCE,blank=True,null=True,verbose_name="(Chiqim,Kirim) turi:")
    comment=models.TextField(blank=True,null=True,verbose_name="Chiqim sababi:")
    date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

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
    created_date=models.DateTimeField(auto_now_add=True)
    change_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"username:{self.student.user.username};status:{self.status};summa:{self.balance};date:{self.change_date.month};"

    def save(self, *args, **kwargs):
        # self.balance=self.cost
        super().save(*args, **kwargs)
        sum = 0
        if self.student.amount>0:
            sum+=0
        if self.tolovlar.exists():
            all = self.tolovlar.all()
            for i in all:
                sum += i.paid
        self.balance=sum + self.cost
        if self.balance>=0:
            self.status=self.PAID
        if self.student.amount>0:
            self.student.amount = self.balance
        if self.student.amount<0 and self.student.latest_amount_date.year==conf.get_date('year') and self.student.latest_amount_date.month==conf.get_date('month'):
            self.student.amount += self.balance
            self.student.latest_amount_date=conf.get_date('current')
        self.student.save()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural="O'quvchi To'lovlari"

class Each_Pay(models.Model):
    std_pay = models.ForeignKey(Student_Pay, related_name='tolovlar', on_delete=models.CASCADE)
    paid = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.std_pay.student.user.username} - {self.paid} som'
    
    # def save(self, *args, **kwargs):
    #     super(Each_Pay, self).save(*args, **kwargs)
    #     Finance.objects.create(
    #         student=self.std_pay.student,
    #         amount=self.paid,
    #         types_finance=Finance.INCOME,
    #         types=Finance.STUDENT_PAY
    #     )
    #     self.std_pay.save()
    def save(self, *args, **kwargs):
        super(Each_Pay, self).save(*args, **kwargs)  # Save the instance to get a primary key

        # Now that the instance is saved, you can create the related Finance object.
        Finance.objects.create(
            student=self.std_pay.student,
            amount=self.paid,
            types_finance=Finance.INCOME,
            types=Finance.STUDENT_PAY
        )

        # Update the related Student_Pay instance and save it.
        self.std_pay.save()