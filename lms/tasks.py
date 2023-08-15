from celery import shared_task

from lms.services.services import mailing_by_subscriptions, deactivation_user_after_month, check_status_payment
from users.models import User


@shared_task
def mailing_by_update_course(email, course, lesson=None):
    mailing_by_subscriptions(email, course, lesson)


@shared_task
def check_last_login_user():
    deactivation_user_after_month()


@shared_task
def scheduled_check_status_payment():
    check_status_payment()
