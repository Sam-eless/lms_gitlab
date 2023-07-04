from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='Изображение', default="course/nophoto.png")
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кем создана', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активен')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', **NULLABLE)
    preview = models.ImageField(upload_to='lesson/', verbose_name='Изображение', default="lesson/nophoto.png")
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активен')
    url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кем создана', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
