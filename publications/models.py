from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Publication(models.Model):
    """
    Публикации
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор публикации')
    header = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    slug = models.CharField(max_length=150, verbose_name=' Человекопонятный URL', **NULLABLE)
    date_of_create = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    image = models.ImageField(upload_to='publications/img/', verbose_name='Изображение', **NULLABLE)
    video = models.FileField(upload_to='publications/video/', verbose_name='Видео', **NULLABLE,
                             validators=[
                                 FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    sign_of_publication = models.BooleanField(default=True, verbose_name='Признак публикации', **NULLABLE)
    quantity_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_paid = models.BooleanField(default=False, verbose_name='Признак платной публикации')

    # def __int__(self):
    #     return f'{self.header}'

    def __str__(self):
        return f'{self.header}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('header',)
