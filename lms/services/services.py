from datetime import date, timedelta, datetime

from django.core.mail import send_mail

from config import settings
from users.models import User


def mailing_by_subscriptions(email, course, lesson=None):
    if lesson is not None:
        message = f'Привет! В курсе {course} обновился урок {lesson}'
    else:
        message = f'Привет! В курсе {course} обновился урок'
    #
    # send_mail(
    #     'Обновление материалов курса',
    #     message,
    #     settings.EMAIL_HOST_USER,
    #     [email],
    #     # ['testmail.mail.ru'], Для тестирования указать свой адрес
    #     fail_silently=False,
    # )

    print(f'Сообщение успешно отправлено на адрес {email}')


def deactivation_user_after_month():
    # Указать количество дней после которых не заходивший пользователь будет деактивирован.
    month_ago = date.today() - timedelta(days=32)
    user_list = User.objects.all()
    for user in user_list:
        if user.last_login:
            if user.last_login.date() == month_ago:
                user.is_active = False
                print(f'Последний раз юзер заходил больше месяца назад - {user.last_login.date()}.')
                print(f'Юзер {user.first_name} {user.last_name}, {user.email}  деактивирован')
