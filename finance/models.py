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
    amount=models.IntegerField(default=0,verbose_name="pul miqdori:")
    amount_2 = models.IntegerField(default=0)
    amount_3 = models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)


    def __str__(self):
        return f"username:{self.student.user.username};status:{self.status};summa:{self.amount};date:{self.date.month};"

    def save(self, *args, **kwargs):
        print(self.amount)
        if self.amount>0:
            Finance.objects.create(
                student=self.student,
                amount=self.amount,
                types_finance=Finance.INCOME,
                types=Finance.STUDENT_PAY
            )

        if self.student.amount>0:
            self.amount+=self.student.amount
        if self.amount>0:
            self.amount_2+=self.amount_2
            self.student.amount+=self.amount_2

        if self.amount>=0 and self.amount_2>=0:
            self.amount_status=self.PAID
        elif self.amount>=0 and self.amount_2<0:
            if self.amount + self.amount_2 >= 0:
                self.amount_status=self.PAID
            else:
                self.amount_status=self.NO_PAID
            self.amount_2 = self.amount + self.amount_2
            self.student.amount+=self.amount_2
            self.student.save()
        else:
            pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="O'quvchi To'lovlari"