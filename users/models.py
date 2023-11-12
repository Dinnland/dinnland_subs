from django.core.validators import MinValueValidator

from . import managers
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Пользователь сервиса"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', blank=True, default=None)
    phone = PhoneNumberField(unique=True, verbose_name='Номер телефона')
    patronymic = models.CharField(max_length=25, verbose_name='Отчество', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар - фото пользователя', **NULLABLE)
    country = models.CharField(max_length=30, verbose_name='Страна', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Верификация')
    subscription = models.BooleanField(default=False, verbose_name='Подписка на сервис')
    date_of_subscription = models.DateTimeField(verbose_name='Дата Подписки', **NULLABLE)
    access_code = models.CharField(max_length=10, verbose_name='Код доступа', **NULLABLE)
    payment_pk = models.CharField(max_length=10, verbose_name='id платежа', **NULLABLE)

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


class Payment(models.Model):
    """Платеж"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='the_user')
    date_of_payment = models.DateTimeField(default=now)
    payment_amount = models.IntegerField(validators=[MinValueValidator(100)], verbose_name='сумма оплаты')
    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')
    session = models.CharField(max_length=180, verbose_name='сессия для оплаты', **NULLABLE)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-date_of_payment',)
