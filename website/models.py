import json
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime

class Type_of_Admin(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
class Permission(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
class Admin(models.Model):
    def admin_avatar_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/admins/{instance.user.username}/avatar/{formatted_date}/{filename}"
    salary = models.IntegerField(default=0)
    image=models.ImageField(upload_to=admin_avatar_path,blank=True,null=True)
    user=models.OneToOneField(User,related_name='admin',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    types=models.ForeignKey(Type_of_Admin,related_name='admins',on_delete=models.CASCADE)
    permissions=models.ManyToManyField(Permission,related_name='admins',blank=True)

    def __str__(self):
        return f"admin:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id=self.user.id
        super().save(*args, **kwargs)

class Science(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)


class Teacher(models.Model):
    def teacher_avatar_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/avatar/{formatted_date}/{filename}"

    def teacher_language_certificate_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/l_sert/{formatted_date}{filename}"

    def teacher_lens_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/lens/{formatted_date}/{filename}"

    def teacher_id_card_photo_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/id_card_photo/{formatted_date}/{filename}"

    def teacher_survey_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/survey/{formatted_date}/{filename}"

    def teacher_biography_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/biography/{formatted_date}/{filename}"

    def teacher_medical_book_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/medical_book/{formatted_date}/{filename}"

    def teacher_picture_3x4_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/picture_3x4/{formatted_date}/{filename}"

    FIXED = "FIXED"
    PER_HOURS = "PER_HOURS"
    SALARY_TYPE = (
        (FIXED, "fixed"),
        (PER_HOURS, "soatbay")
    )

    MALE = "MALE"
    FEMALE = "FEMALE"
    GENDER = (
        (MALE, "Erkak"),
        (FEMALE, "Ayol")
    )
    # http://127.0.0.1:8000/media/uploads/teachers/first_teacher5/avatar/2023_09_01/Screenshot_from_2023-08-27_16-20-03_gYEAqW1.png

    user = models.OneToOneField(User, related_name='teacher', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=teacher_avatar_path, blank=True, null=True)
    science = models.ForeignKey(Science, related_name="teachers", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    id_card = models.CharField(max_length=50, blank=True, null=True)
    salary_type = models.CharField(max_length=255, choices=SALARY_TYPE)
    salary = models.IntegerField(default=0)
    date_of_employment = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, choices=GENDER)
    address = models.CharField(max_length=400, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    language_certificate = models.FileField(upload_to=teacher_language_certificate_path, blank=True, null=True)
    lens = models.FileField(upload_to=teacher_lens_path, blank=True, null=True)
    id_card_photo = models.FileField(upload_to=teacher_id_card_photo_path, blank=True, null=True)
    survey = models.FileField(upload_to=teacher_survey_path, blank=True, null=True)
    biography = models.FileField(upload_to=teacher_biography_path, blank=True, null=True)
    medical_book = models.FileField(upload_to=teacher_medical_book_path, blank=True, null=True)
    picture_3x4 = models.FileField(upload_to=teacher_picture_3x4_path, null=True, blank=True)

    def __str__(self):
        return f"teacher:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id = self.user.id
        super().save(*args, **kwargs)


class Sinf(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    teacher=models.ForeignKey(Teacher,related_name='sinflar',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"teacher:{self.user.username}"

class Employer(models.Model):
    def employer_avatar_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/employers/{instance.user.username}/avatar/{formatted_date}/{filename}"
    salary = models.IntegerField(default=0)    
    image=models.ImageField(upload_to=employer_avatar_path,blank=True,null=True)
    user=models.OneToOneField(User,related_name='employer',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    lavozim=models.CharField(max_length=255)

    def __str__(self):
        return f"employer:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id=self.user.id
        super().save(*args, **kwargs)

class Student(models.Model):
    def student_avatar_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/students/{instance.user.username}/avatar/{formatted_date}/{filename}"

    def student_id_card_parents_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/students/{instance.user.username}/id_card_parents/{formatted_date}/{filename}"

    def student_picture_3x4_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/students/{instance.user.username}/picture_3x4/{formatted_date}/{filename}"

    def student_school_tab_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/students/{instance.user.username}/school_tab/{formatted_date}/{filename}"


    user = models.OneToOneField(User, related_name='student', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=student_avatar_path, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    id_card = models.CharField(max_length=50)
    date_of_admission = models.DateField(blank=True, null=True)
    class_of_school = models.ForeignKey(Sinf, related_name='students', on_delete=models.CASCADE, blank=True, null=True)
    id_card_parents = models.FileField(upload_to=student_id_card_parents_path, null=True, blank=True)
    picture_3x4 = models.FileField(upload_to=student_picture_3x4_path, null=True, blank=True)
    school_tab = models.FileField(upload_to=student_school_tab_path, null=True, blank=True)

    def __str__(self):
        return f"student:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id = self.user.id
        super().save(*args, **kwargs)

    
class Parent(models.Model):
    def parent_avatar_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/parents/{instance.user.username}/avatar/{formatted_date}/{filename}"
    
    image=models.ImageField(upload_to=parent_avatar_path,blank=True,null=True)
    user=models.OneToOneField(User,related_name='parent',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    children=models.ManyToManyField(Student,related_name="parents",blank=True)

    def __str__(self):
        return f"parent:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id=self.user.id
        super().save(*args, **kwargs)

class Chat_room(models.Model):
    name=models.CharField(max_length=255,unique=True)
    users=models.ManyToManyField(User,related_name='chat_rooms',blank=True)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        super().save(*args, **kwargs)
    
class Message(models.Model):
    chat_room=models.ForeignKey(Chat_room,related_name='messages',on_delete=models.CASCADE)
    from_user=models.ForeignKey(User,related_name='from_messages',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='to_messages',on_delete=models.CASCADE)
    message=models.TextField(blank=True,null=True)
    file_message=models.FileField(upload_to="uploads/message/%Y_%m_%d",blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat_room.name}:{self.from_user.username} --> {self.to_user.username}"

    def get_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')
    
    def get_json_date(self):
        return json.dumps(self.date)
    
    def type_message(self):
        if self.file_message:
            return 'file_message'
        else:
            return 'word_message'
    
class Davomat(models.Model):
    user=models.ForeignKey(User,related_name='davomatlar',on_delete=models.CASCADE)
    SABABLI="SABABLI"
    SABABSIZ="SABABSIZ"
    KELGAN="KELGAN"
    CHOICES_DAVOMAT=(
        (SABABLI,'Sababli'),
        (SABABSIZ,'Sababsiz'),
        (KELGAN,'kelgan'),
    )
    davomat=models.CharField(choices=CHOICES_DAVOMAT,max_length=50)
    date=models.DateField(auto_now_add=True)
    sabab=models.TextField(blank=True,null=True)

    def get_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')
    
    def get_json_date(self):
        return json.dumps(self.date)
    
    def __str__(self) -> str:
        return f"{self.user}:{self.davomat};{self.date}"

    class Meta:
        verbose_name_plural="Davomatlar"

class Student_Pay(models.Model):
    PAID="PAID"
    NO_PAID="NO_PAID"#DID not paid
    STATUS=(
        (PAID,"to'lagan"),
        (NO_PAID,"to'lamagan")
    )
    student=models.ForeignKey(Student,related_name='pays',on_delete=models.CASCADE)
    status=models.CharField(max_length=255,choices=STATUS)
    summa=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"username:{self.student.user.username};status:{self.status};summa:{self.summa};date:{self.date.month};"

class Expense(models.Model):
    amount=models.IntegerField(default=0)
    comment=models.TextField(blank=True,null=True)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}.Chiqim sababi:{self.comment}"
    
    

