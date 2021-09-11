from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


GENDER_CHOICES = (
    ('Erkak', 'Erkak'),
    ('Ayol', 'Ayol')
)

STEP_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),

)

class Course(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
                

class Group(models.Model):
    course_title = models.ForeignKey(Course, related_name= "groups", on_delete=models.PROTECT)
    name = models.CharField(max_length=70, verbose_name="guruh nomi")
    mentor = models.CharField(max_length=40)
    time = models.DateTimeField() 
    weekdays = models.CharField(max_length=200, verbose_name="hafta kunlari")
    price = models.IntegerField()
    technologies = models.CharField(max_length=200,verbose_name="texnologiyalar")

    def __str__(self):
        return str(self.name)


class User(models.Model):
    user_id = models.IntegerField()
    tg_username = models.CharField('Username',
                                max_length=20, unique=False) 

    def __str__(self):
        return self.tg_username      

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Student(models.Model):
    user = models.OneToOneField(User, related_name='students', on_delete=models.PROTECT)                              
    name = models.CharField(max_length=20, verbose_name="Familya Ism")
    age = models.IntegerField(verbose_name="yoshi")
    phone = models.CharField(max_length=12, unique=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    group = models.ForeignKey(Group, related_name="users", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        

    def __str__(self):
        return self.name      

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"

class UserStep(models.Model):
    user = models.OneToOneField(User, related_name="step", on_delete=models.PROTECT)
    step = models.CharField(max_length=2, choices=STEP_CHOICES)

    def __str__(self):
        return self.step        