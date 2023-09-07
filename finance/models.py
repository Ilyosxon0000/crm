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
    student=models.ForeignKey(conf.STUDENT,related_name='finance_pays',on_delete=models.CASCADE)
    teacher=models.ForeignKey(conf.TEACHER,related_name='salaries',on_delete=models.CASCADE)
    amount=models.IntegerField(default=0,verbose_name="pul miqdori:")
    types_finance=models.CharField(max_length=60,choices=STATUS,verbose_name="Chiqim yoki Kirim turi:")
    types=models.CharField(max_length=60,choices=STATUS,blank=True,null=True,verbose_name="(Chiqim,Kirim) turi:")
    comment=models.TextField(blank=True,null=True,verbose_name="Chiqim sababi:")
    date=models.DateField(auto_now_add=True)

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
    status=models.CharField(max_length=255,choices=STATUS,verbose_name="holat:")
    amount=models.IntegerField(default=0,verbose_name="pul miqdori:")
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"username:{self.student.user.username};status:{self.status};summa:{self.summa};date:{self.date.month};"

    def save(self, *args, **kwargs):
        if self.amount>=0:
            self.amount_status=self.PAID
        else:
            self.amount_status=self.NO_PAID
        self.student.amount-=self.amount
        self.student.save()
        # if self.status==self.PAID and self.amount>=0:
        #     print(conf.get_date("year"))
        #     print(conf.get_date("month"))
        #     print(conf.get_date("week"))
        #     print(conf.get_date("week_day"))
        #     print(conf.get_date("day"))
        #     income_general=InCome.objects.get_or_create(types="GENERAL")
        #     income_general[0].amount+=self.amount
        #     income_general[0].save()
        #     income_yearly=InCome.objects.get_or_create(types="YEARLY",date__year=conf.get_date("year"))
        #     income_yearly[0].amount+=self.amount
        #     income_yearly[0].save()
        #     income_monthly=InCome.objects.get_or_create(types="MONTHLY",date__month=conf.get_date("month"))
        #     income_monthly[0].amount+=self.amount
        #     income_monthly[0].save()
        #     income_weekly=InCome.objects.get_or_create(types="WEEKLY",date__week=conf.get_date("week"))
        #     income_weekly[0].amount+=self.amount
        #     income_weekly[0].save()
        #     income_daily=InCome.objects.get_or_create(types="DAILY",date__day=conf.get_date("day"))
        #     income_daily[0].amount+=self.amount
        #     income_daily[0].save()
        #     # TODO for InCome
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="O'quvchi To'lovlari"