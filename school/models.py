from django.db import models
from django.utils.text import slugify
from myconf import conf
from django.contrib.auth import get_user_model
import json
from django.core.exceptions import ValidationError
from myconf.conf import get_model
from typing import Any

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
    slug=models.SlugField(blank=True,null=True)
    teacher=models.OneToOneField(conf.TEACHER,related_name='sinf',on_delete=models.CASCADE,blank=True,null=True)
    room=models.ForeignKey(conf.ROOM,related_name='sinflar',blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"class:{self.title}"

    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)

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
    attendance_type=models.CharField(choices=CHOICES_DAVOMAT,max_length=50,verbose_name="davomat turi:",default=SABABSIZ)
    date=models.DateField(auto_now_add=True)
    date_enter = models.DateTimeField(blank=True,null=True)
    date_leave = models.DateTimeField(blank=True,null=True)
    reason=models.TextField(blank=True,null=True,verbose_name="sabab(Agar sababli turida bo'lsa):")

    def save(self, *args, **kwargs):
        if self.attendance_type==self.KELGAN:
            self.date=conf.get_date('current_date')
        super().save(*args, **kwargs)

    def get_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')
    
    def get_json_date(self):
        return json.dumps(self.date)
    
    def __str__(self) -> str:
        return f"{self.user.username}:{self.attendance_type};{self.date}"

    class Meta:
        verbose_name_plural="Davomatlar"

class Room(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Xonalar"

class Lesson_Time(models.Model):
    begin_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.begin_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

    class Meta:
        verbose_name_plural="Dars soatlari"

class Lesson(models.Model):
    MONDAY="MONDAY"
    TUESDAY="TUESDAY"
    WEDNESDAY="WEDNESDAY"
    THURSDAY="THURSDAY"
    FRIDAY="FRIDAY"
    SATURDAY="SATURDAY"
    DAY_CHOICES=(
        (MONDAY,"Dushanba"),
        (TUESDAY,"Seshanba"),
        (WEDNESDAY,"Chorshanba"),
        (THURSDAY,"Payshanba"),
        (FRIDAY,"Juma"),
        (SATURDAY,"Shanba"),
    )
    # teacher=models.ForeignKey(conf.TEACHER,related_name='lessons',on_delete=models.CASCADE)
    teacher=models.TextField(blank=True,null=True)
    science=models.ForeignKey(conf.SCIENCE,related_name="lessons",blank=True,null=True,on_delete=models.CASCADE)
    student_class=models.ForeignKey(conf.CLASS,related_name='lessons',on_delete=models.CASCADE)
    room=models.ForeignKey(conf.ROOM,related_name='lessons',blank=True,null=True,on_delete=models.CASCADE)
    lesson_date=models.CharField(
        max_length=10,
        choices=DAY_CHOICES,
        default='Dushanba'
    )
    lesson_time=models.ForeignKey(Lesson_Time,related_name="lessons",on_delete=models.CASCADE)

    def __str__(self):
        return f"fan:{self.science};O'qituvchi:{self.teacher};Xona:{self.room};Hafta kuni:{self.lesson_date}"

    class Meta:
        verbose_name_plural="Darslar"
        ordering = ['lesson_time']

class Grade(models.Model):
    GRADE_CHOICES = (
        (1, "Bir"),
        (2, "Ikki"),
        (3, "Uch"),
        (4, "To'rt"),
        (5, "Besh"),
    )

    grade = models.IntegerField(
        choices=GRADE_CHOICES,
        default=1
    )
    teacher=models.ForeignKey(conf.TEACHER,related_name="grades",on_delete=models.CASCADE)
    student=models.ForeignKey(conf.STUDENT,related_name="grades",on_delete=models.CASCADE)
    lesson=models.ForeignKey(conf.LESSON,related_name='grades',on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Baholar"

class Task(models.Model):
    from_user=models.ForeignKey(get_user_model(),related_name='from_tasks',on_delete=models.CASCADE)
    to_user=models.ForeignKey(get_user_model(),related_name='to_tasks',on_delete=models.CASCADE)
    task_title=models.CharField(max_length=255)
    task_message=models.TextField()
    complete_to_user=models.BooleanField(default=False)
    complete_from_user=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    change_date=models.DateTimeField(auto_now=True)
    begin_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValidationError("from_user and to_user cannot be the same.")
        super().save(*args, **kwargs)

class TaskForClass(models.Model):
    from_teacher=models.ForeignKey(get_model(conf.TEACHER),related_name='tasksforclass',on_delete=models.CASCADE)
    to_class=models.ForeignKey(get_model(conf.CLASS),related_name='tasks',on_delete=models.CASCADE)
    task_title=models.CharField(max_length=255)
    task_message=models.TextField()
    complete_to_user=models.BooleanField(default=False)
    complete_from_user=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    change_date=models.DateTimeField(auto_now=True)
    begin_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)

class Parent_Comment(models.Model):
    parent=models.ForeignKey(get_model(conf.PARENT),related_name='parent_comments',on_delete=models.CASCADE)
    admin=models.ForeignKey(get_model(conf.ADMIN),blank=True,null=True,related_name='admin_answers',on_delete=models.CASCADE)
    message=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    change_date=models.DateTimeField(auto_now=True)

class Teacher_Lesson(models.Model):
    teacher=models.ForeignKey(get_model(conf.TEACHER),related_name='teacher_lessons',on_delete=models.CASCADE)
    message=models.TextField()
    file_message=models.FileField(upload_to="uploads/message/%Y_%m_%d",blank=True,null=True)
    date=models.DateTimeField(blank=True,null=True)


class Question(models.Model):
    teacher=models.ForeignKey(get_model(conf.TEACHER),related_name="questions",on_delete=models.CASCADE)
    #TODO
    science=models.ForeignKey(get_model(conf.SCIENCE),related_name="questions",on_delete=models.CASCADE)
    question=models.TextField()
    option1=models.CharField(max_length=255)
    option2=models.CharField(max_length=255)
    option3=models.CharField(max_length=255)
    option4=models.CharField(max_length=255)
    answer=models.CharField(max_length=255)

class Company(models.Model):
    logo=models.FileField(upload_to="uploads/company_logo/%Y_%m_%d",blank=True,null=True)
    # name=models.CharField(max_length=255,blank=True,null=True)
    begin_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    study_price=models.IntegerField(default=0)
    hostel_price=models.IntegerField(default=0)
    camera_entrance=models.URLField(blank=True,null=True)
    camera_exit=models.URLField(blank=True,null=True)
