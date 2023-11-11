import random
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from myconf import conf
from imagekit.models import ImageSpecField
from imagekit.processors import Transpose

class UserProfile(AbstractUser):
    def user_avatar_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/{instance.username}/avatar/{formatted_date}/{filename}"
    
    image=models.FileField(upload_to=user_avatar_path,verbose_name="Avatar uchun surat:",blank=True,null=True)
    image_thumbnail=ImageSpecField(
        source='image',
        processors=[Transpose(),],
        format='JPEG',
        options={'quality':60}
    )
    middle_name=models.CharField(max_length=255,verbose_name="Otasini ismi:",blank=True,null=True)
    type_user = models.CharField(max_length=255, blank=True, null=True,verbose_name="User turi:")
    unique_number = models.PositiveIntegerField(unique=True)
    # Other fields here

    def save(self, *args, **kwargs):
        if not self.unique_number:
            i=0
            while True:
                new_unique_number = random.randint(100000, 999999)  # Generate a random 6-digit number
                if not UserProfile.objects.filter(unique_number=new_unique_number).exists():
                    self.unique_number = new_unique_number
                    break
                i+=1
        return super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Foydalanuvchilar"

class Type_of_Admin(models.Model):
    title=models.CharField(max_length=255,verbose_name="nomi:")
    slug=models.SlugField(blank=True,null=True,editable=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Adminlar toifasi"

class Permission(models.Model):
    title=models.CharField(max_length=255,verbose_name="nomi:")
    slug=models.SlugField(blank=True,null=True,editable=False)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Adminlarga ruxsatnomalar"

class Admin(models.Model):
    user=models.OneToOneField(get_user_model(),related_name='admin',on_delete=models.CASCADE)
    salary = models.IntegerField(default=0,verbose_name="Oylik maosh:")
    types=models.ForeignKey(Type_of_Admin,related_name='admins',on_delete=models.CASCADE,verbose_name="Admin turi:")
    permissions=models.ManyToManyField(Permission,related_name='admins',blank=True,verbose_name="Ruxsatnomalar:")

    def __str__(self):
        return f"admin:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.user.type_user='admin'
        self.user.save()
        self.id=self.user.id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Adminlar"
# 
class Teacher(models.Model):
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
    
    def lessons_file_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/lessons_file/{formatted_date}/{filename}"

    MALE = "MALE"
    FEMALE = "FEMALE"
    GENDER = (
        (MALE, "Erkak"),
        (FEMALE, "Ayol")
    )

    HIGH_CATEGORY = "HIGH_CATEGORY"
    FIRST_CATEGORY = "FIRST_CATEGORY"
    SECOND_CATEGORY = "SECOND_CATEGORY"
    EXPERIENCE_TYPE = (
        (HIGH_CATEGORY, "Oliy toifa"),
        (FIRST_CATEGORY, "1-toifa"),
        (SECOND_CATEGORY, "2-toifa")
    )

    TESOL = "TESOL"
    CELTA = "CELTA"
    IELTS6 = "IELTS6"
    CEFRB2 = "CEFRB2"
    LANGUAGE_CERTIFICATE_TYPE = (
        (TESOL, "Tesol"),
        (CELTA, "Celta"),
        (IELTS6, "IELTS 6+"),
        (CEFRB2, "CEFR B2+")
    )
    user = models.OneToOneField(get_user_model(), related_name='teacher', on_delete=models.CASCADE)
    sciences = models.ManyToManyField('school.Science', related_name="teachers",blank=True,verbose_name="Fanlar:")
    id_card = models.CharField(max_length=50, blank=True, null=True,verbose_name="Pasport seriya raqami:")
    date_of_employment = models.DateField(blank=True, null=True,verbose_name="Ishga kirgan sanasi:")
    gender = models.CharField(max_length=255, choices=GENDER,verbose_name="Jinsi:")
    address = models.CharField(max_length=400, blank=True, null=True,verbose_name="Manzili:")
    experience = models.CharField(max_length=255,blank=True,null=True, choices=EXPERIENCE_TYPE,verbose_name="Tajriba:")
    language_certificate = models.CharField(max_length=255,blank=True,null=True, choices=LANGUAGE_CERTIFICATE_TYPE,verbose_name="Til sertifikati:")
    language_certificate_file = models.FileField(upload_to=teacher_language_certificate_path, blank=True, null=True,verbose_name="Til sertifikati fayl shakli:")
    lens = models.FileField(upload_to=teacher_lens_path, blank=True, null=True,verbose_name="Obyektivka:")
    id_card_photo = models.FileField(upload_to=teacher_id_card_photo_path, blank=True, null=True,verbose_name="Pasport nusxasi:")
    survey = models.FileField(upload_to=teacher_survey_path, blank=True, null=True,verbose_name="So'rovnoma:")
    biography = models.FileField(upload_to=teacher_biography_path, blank=True, null=True,verbose_name="Tarjimai xol:")
    medical_book = models.FileField(upload_to=teacher_medical_book_path, blank=True, null=True,verbose_name="Tibbiy Daftarcha (086):")
    picture_3x4 = models.FileField(upload_to=teacher_picture_3x4_path, null=True, blank=True,verbose_name="3x4 rasm:")
    completed_salary=models.BooleanField(default=False)
    lessons_file=models.FileField(upload_to=lessons_file_path, null=True, blank=True,verbose_name="dars jadvali:")

    def __str__(self):
        return f"teacher:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.user.type_user='teacher'
        self.user.save()
        self.id = self.user.id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="O'qituvchilar"

class Employer(models.Model):
    user=models.OneToOneField(get_user_model(),related_name='employer',on_delete=models.CASCADE)
    salary = models.IntegerField(default=0,verbose_name="Oylik maosh:")    
    position=models.CharField(max_length=255,verbose_name="Lavozim:")

    def __str__(self):
        return f"employer:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.user.type_user='employer'
        self.user.save()
        self.id=self.user.id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Xodimlar"

class StudentManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        data={
                "FAMILY_CHILDREN":{
                    'discount': 10,
                    'discount_month': 12,
                },
                "EMPLOYER_CHILDREN":{
                    'discount': 20,
                    'discount_month': 12,
                },
                "GRANT_FULL":{
                    'discount': 100,
                    'discount_month': 12,
                },
                "GRANT_MONTH":{
                    'discount': 100,
                    'discount_month': 2,
                },
            }
        discount=data[kwargs['discount_type']]
        kwargs['discount']=discount['discount']
        kwargs['discount_month']=discount['discount_month']
        return super().create(**kwargs)

class Student(models.Model):
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
    
    def student_medical_book_path(instance, filename):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        return f"uploads/teachers/{instance.user.username}/medical_book/{formatted_date}/{filename}"

    DISCOUNT_TYPE=(
        ("GRANT_FULL","GRANT_FULL"),
        ("GRANT_MONTH","GRANT_MONTH"),
        ("EMPLOYER_CHILDREN","EMPLOYER_CHILDREN"),
        ("FAMILY_CHILDREN","FAMILY_CHILDREN"),
    )

    user = models.OneToOneField(get_user_model(), related_name='student', on_delete=models.CASCADE)
    id_card = models.CharField(max_length=50)
    date_of_admission = models.DateField(blank=True, null=True)
    class_of_school = models.ForeignKey(conf.CLASS, related_name='students', on_delete=models.CASCADE, blank=True, null=True)
    id_card_parents = models.FileField(upload_to=student_id_card_parents_path, null=True, blank=True,verbose_name="Ota-ona pasporti nusxasi:")
    picture_3x4 = models.FileField(upload_to=student_picture_3x4_path, null=True, blank=True,verbose_name="3x4 rasm:")
    school_tab = models.FileField(upload_to=student_school_tab_path, null=True, blank=True,verbose_name="Maktabdan Tabel asli 2-11-sinflar uchun:")
    medical_book = models.FileField(upload_to=student_medical_book_path, blank=True, null=True,verbose_name="Tibbiy Daftarcha (086):")
    hostel=models.BooleanField(default=False)
    discount=models.IntegerField(default=0)
    discount_month=models.IntegerField(default=0)
    discount_type=models.CharField(max_length=20,choices=DISCOUNT_TYPE,blank=True,null=True)
    objects=StudentManager()
    
    def __str__(self):
        return f"student:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.user.type_user='student'
        self.user.save()
        self.id=self.user.id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="O'quvchilar"

class Parent(models.Model):
    user=models.OneToOneField(get_user_model(),related_name='parent',on_delete=models.CASCADE)
    children=models.ManyToManyField(Student,related_name="parents",blank=True)

    def __str__(self):
        return f"parent:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.user.type_user='parent'
        self.user.save()
        self.id=self.user.id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Ota ona"

    # user = models.OneToOneField(get_user_model(), related_name='teacher', on_delete=models.CASCADE)
    # sciences = models.ManyToManyField('school.Science', related_name="teachers",blank=True,verbose_name="Fanlar:")
    # id_card = models.CharField(max_length=50, blank=True, null=True,verbose_name="Pasport seriya raqami:")
    # salary_type = models.CharField(max_length=255, choices=SALARY_TYPE,verbose_name="Oylik turi(Fixed yoki Soatbay):")
    # salary = models.IntegerField(default=0,verbose_name="Oylik maosh(soatbay narx):")
    # date_of_employment = models.DateField(blank=True, null=True,verbose_name="Ishga kirgan sanasi:")
    # gender = models.CharField(max_length=255, choices=GENDER,verbose_name="Jinsi:")
    # address = models.CharField(max_length=400, blank=True, null=True,verbose_name="Manzili:")
    # experience = models.CharField(max_length=255,blank=True,null=True, choices=EXPERIENCE_TYPE,verbose_name="Tajriba:")
    # language_certificate_file = models.FileField(upload_to=teacher_language_certificate_path, blank=True, null=True,verbose_name="Til sertifikati fayl shakli:")
    # lens = models.FileField(upload_to=teacher_lens_path, blank=True, null=True,verbose_name="Obyektivka:")
    # id_card_photo = models.FileField(upload_to=teacher_id_card_photo_path, blank=True, null=True,verbose_name="Pasport nusxasi:")
    # survey = models.FileField(upload_to=teacher_survey_path, blank=True, null=True,verbose_name="So'rovnoma:")
    # biography = models.FileField(upload_to=teacher_biography_path, blank=True, null=True,verbose_name="Tarjimai xol:")
    # medical_book = models.FileField(upload_to=teacher_medical_book_path, blank=True, null=True,verbose_name="Tibbiy Daftarcha (086):")
    # picture_3x4 = models.FileField(upload_to=teacher_picture_3x4_path, null=True, blank=True,verbose_name="3x4 rasm:")
    # lessons_file=models.FileField(upload_to=lessons_file_path, null=True, blank=True,verbose_name="dars jadvali:")


"""

cron 1 oyda 
o'quvchi active bo'lsa
Grantlarni tekshirish
Yotoqxona

"""