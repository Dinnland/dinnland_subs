from . import managers
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'null': True, 'blank': True}

# Create your models here.



class User(AbstractUser):
    """Пользователь сервиса"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = PhoneNumberField(unique=True, help_text='Номер телефона')
    # first_name = AbstractUser.first_name
    # last_name = AbstractUser.last_name
    # name = models.CharField(max_length=100, verbose_name='Имя', **NULLABLE)
    # surname = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)

    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар - фото пользователя', **NULLABLE)
    # city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='Страна', **NULLABLE)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()
