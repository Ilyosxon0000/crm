from django.db import models
from django.utils.text import slugify
from myconf import conf
from django.contrib.auth import get_user_model
import json

class Science(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural="Fanlar"

class Class(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    teacher=models.ForeignKey(conf.TEACHER,related_name='sinflar',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"teacher:{self.user.username}"

    class Meta:
        verbose_name_plural="Sinflar"

class Attendance(models.Model):
    user=models.ForeignKey(get_user_model(),related_name='davomatlar',on_delete=models.CASCADE)
    SABABLI="SABABLI"
    SABABSIZ="SABABSIZ"
    KELGAN="KELGAN"
    CHOICES_DAVOMAT=(
        (SABABLI,'Sababli'),
        (SABABSIZ,'Sababsiz'),
        (KELGAN,'kelgan'),
    )
    attendance_type=models.CharField(choices=CHOICES_DAVOMAT,max_length=50,verbose_name="davomat turi:")
    date=models.DateField(auto_now_add=True)
    reason=models.TextField(blank=True,null=True,verbose_name="sabab(Agar sababli turida bo'lsa):")

    def get_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')
    
    def get_json_date(self):
        return json.dumps(self.date)
    
    def __str__(self) -> str:
        return f"{self.user}:{self.davomat};{self.date}"

    class Meta:
        verbose_name_plural="Davomatlar"
