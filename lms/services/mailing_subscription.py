from django.core.mail import send_mail

from config import settings


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
