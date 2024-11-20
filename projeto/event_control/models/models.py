from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
import face_recognition as fr
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    def clean(self):
        super().clean()
        errors = {}
        try:
            img = fr.load_image_file(self.photo)
            faceloc = fr.face_locations(img)[0]
        except Exception as e:
            errors['photo'] = 'Essa foto não ta muito legal tente tirar outra mais adequada'
        finally:
            if errors:
                raise ValidationError(errors)



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
    end_date = models.DateTimeField(null=True, blank=False)

    def clean(self):
        super().clean()
        errors = {}
        if self.register_type == 'ee' and self.end_date == None:
            errors['end_date'] = 'A data fim não pode ser nula em eventos do tipo Entrada e saida'
        
        if self.end_date != None and self.end_date < self.start_date and self.register_type == 'ee':
            errors['start_date'] = 'A data inicial deve ser menor que a final'

        if self.start_date <= timezone.now():
            errors['start_date'] = 'A data inicial deve ser maior que a atual'

        origin = Event.objects.filter(pk=self.pk).first()
        if origin and origin.start_date <= timezone.now():
            errors['start_date'] = 'Não pode ter alterações depois da data de inicio do evento'
        
        if errors:
            raise ValidationError(errors)


class Register(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, models.DO_NOTHING, null=False, blank=False)
    student_id = models.ForeignKey(Student, models.DO_NOTHING, null=False, blank=False)
    check_in = models.DateTimeField(null=False, blank=False)
    check_out = models.DateTimeField(null=True, blank=False)
    computed = models.BooleanField(null=False, blank=False, default=False)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return self.name