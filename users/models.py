from . import managers
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'null': True, 'blank': True}

# Create your models here.


class User(AbstractUser):
    """Пользователь сервиса"""
    # ROLE_CHOICES = (
    #     ('sub', 'Подписчик'),
    #     ('author', 'Автор'),
    # )
    # role = models.CharField(max_length=50, default='sub', choices=ROLE_CHOICES, verbose_name='Роль пользователя')
    # name = models.CharField(max_length=100, verbose_name='Имя', **NULLABLE)
    # surname = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', blank=True, default=None)
    phone = PhoneNumberField(unique=True, verbose_name='Номер телефона')
    # nickname = models.CharField(unique=True, max_length=15, verbose_name='nickname', **NULLABLE)
    patronymic = models.CharField(max_length=25, verbose_name='Отчество', **NULLABLE)

    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар - фото пользователя', **NULLABLE)
    country = models.CharField(max_length=30, verbose_name='Страна', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Верификация')
    subscription = models.BooleanField(default=False, verbose_name='Подписка на сервис')
    date_of_subscription = models.DateTimeField(verbose_name='Дата Подписки', **NULLABLE)
    access_code = models.CharField(max_length=10, verbose_name='Код доступа', **NULLABLE)

    # if phone is not None:
    #     USERNAME_FIELD = 'phone'
    # elif email is not None:
    #     USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()

    def __str__(self):
        return f"{self.phone}"

    def save(self, *args, **kwargs):
        """
        Метод, делающий пропущенные поля email = null,
        для исключения ошибок Уникальности, из-за записи пустых строк
        """
        # Empty strings are not unique, but we can save multiple NULLs
        if not self.email:
            self.email = None

        super().save(*args, **kwargs)  # Python3-style super()