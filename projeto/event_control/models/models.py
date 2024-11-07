from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O campo Email deve ser definido')
        if not password:
            raise ValueError('o campo Senha deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    student_id = models.CharField(max_length=10, null=False, blank=False, unique=True)
    course = models.CharField(max_length=255, null=False, blank=False)
    photo = models.ImageField(upload_to='photos')
    user_id = models.OneToOneField(User, models.DO_NOTHING, null=False)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Student.objects.get(pk=self.pk)
            if original.photo != self.photo and original.photo:
                if os.path.isfile(original.photo.path):
                    os.remove(original.photo.path)
        super().save(*args, **kwargs)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    user_id = models.OneToOneField(User, models.DO_NOTHING, null=False, blank=False)

REGISTER_TYPE_CHOICES = [
    ('eo', 'Somente entrada'),
    ('ee', 'Entrada e saida')
]

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    register_type = models.CharField(max_length=2, choices=REGISTER_TYPE_CHOICES, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    organizer = models.ForeignKey(Teacher, models.DO_NOTHING, null=False, blank=False)

class Register(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, models.DO_NOTHING, null=False, blank=False)
    student_id = models.ForeignKey(Student, models.DO_NOTHING, null=False, blank=False)
    date = models.DateField(auto_now_add=True, null=False, blank=False)
    check_in = models.TimeField(auto_now_add=True, null=False, blank=False)
    check_out = models.TimeField(auto_now_add=True, null=True, blank=False)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return self.name