from django.db import models

from config import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='Изображение', default="course/nophoto.png")
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кем создана', **NULLABLE)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кем создана', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.title}'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user}: {self.amount} ({self.payment_method})'
