import json
from django.db import models
from django.contrib.auth.models import User,AbstractUser,Group,Permission
from django.utils.text import slugify
from django.conf import settings

class Type_of_Admin(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # self.slug=self.title.lower().replace(" ","-")
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
class Permission(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        # self.slug=self.title.lower().replace(" ","-")
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
class Admin(models.Model):
    image=models.ImageField(upload_to="uploads/avatar/%Y_%m_%d",blank=True,null=True)
    user=models.OneToOneField(User,related_name='admins',on_delete=models.CASCADE)
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
    FIXED="FIXED"
    PER_HOURS="PER_HOURS"
    SALLERY_TYPE=(
        (FIXED,"fixed"),
        (PER_HOURS,"soatbay")
    )
    
    MALE="MALE"
    FEMALE="FEMALE"
    GENDER=(
        (MALE,"Erkak"),
        (FEMALE,"Ayol")
    )
    user=models.OneToOneField(User,related_name='teachers',on_delete=models.CASCADE)
    image=models.ImageField(upload_to=f"uploads/teachers/{user}/avatar/%Y_%m_%d",blank=True,null=True)
    science=models.ForeignKey(Science,related_name="teachers",on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    middle_name=models.CharField(max_length=255)
    id_card=models.CharField(max_length=50,blank=True,null=True)
    sallery_type=models.CharField(max_length=255,choices=SALLERY_TYPE)
    sallery=models.IntegerField(default=0)
    date_of_employment=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=255,choices=GENDER)
    address=models.CharField(max_length=400,blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    experience=models.CharField(max_length=255,blank=True,null=True)
    language_certificate=models.FileField(upload_to=f"uploads/teachers/{user}/l_sert/%Y_%m_%d",blank=True,null=True)
    lens=models.FileField(upload_to=f"uploads/teachers/{user}/lens/%Y_%m_%d",blank=True,null=True)
    id_card_photo=models.FileField(upload_to=f"uploads/teachers/{user}/id_card_photo/%Y_%m_%d",blank=True,null=True)
    survey=models.FileField(upload_to=f"uploads/teachers/{user}/survey/%Y_%m_%d",blank=True,null=True)
    biography=models.FileField(upload_to=f"uploads/teachers/{user}/biography/%Y_%m_%d",blank=True,null=True)
    medical_book=models.FileField(upload_to=f"uploads/teachers/{user}/biography/%Y_%m_%d",blank=True,null=True)
    picture_3x4=models.FileField(upload_to=f"uploads/teachers/{user}/picture_3x4/%Y_%m_%d",null=True,blank=True)

    def __str__(self):
        return f"teacher:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id=self.user.id
        super().save(*args, **kwargs)

class Sinf(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    teacher=models.ForeignKey(Teacher,related_name='sinflar',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"teacher:{self.user.username}"

class Employer(models.Model):
    image=models.ImageField(upload_to="uploads/avatar/%Y_%m_%d",blank=True,null=True)
    user=models.OneToOneField(User,related_name='employers',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    lavozim=models.CharField(max_length=255)

    def __str__(self):
        return f"employer:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id=self.user.id
        super().save(*args, **kwargs)

class Student(models.Model):
    user=models.OneToOneField(User,related_name='students',on_delete=models.CASCADE)
    image=models.ImageField(upload_to=f"uploads/students/{user}/avatar/%Y_%m_%d",blank=True,null=True)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    middle_name=models.CharField(max_length=255)
    id_card=models.CharField(max_length=50)
    date_of_admission=models.DateField(blank=True,null=True)
    class_of_school=models.ForeignKey(Sinf,related_name='students',on_delete=models.CASCADE,blank=True,null=True)
    id_card_parents=models.FileField(upload_to=f"uploads/students/{user}/id_card_parents/%Y_%m_%d",null=True,blank=True)
    picture_3x4=models.FileField(upload_to=f"uploads/students/{user}/picture_3x4/%Y_%m_%d",null=True,blank=True)
    school_tab=models.FileField(upload_to=f"uploads/students/{user}/picture_3x4/%Y_%m_%d",null=True,blank=True)

    def __str__(self):
        return f"student:{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.id=self.user.id
        super().save(*args, **kwargs)
    
class Parent(models.Model):
    image=models.ImageField(upload_to="uploads/avatar/%Y_%m_%d",blank=True,null=True)
    user=models.OneToOneField(User,related_name='parents',on_delete=models.CASCADE)
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
        # self.slug=self.title.lower().replace(" ","-")
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

    def get_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')
    
    def get_json_date(self):
        return json.dumps(self.date)
    
    def __str__(self) -> str:
        return f"{self.user}:{self.davomat};{self.date}"

    class Meta:
        verbose_name_plural="Davomatlar"

