from celery import shared_task

from lms.services.mailing_subscription import mailing_by_subscriptions


@shared_task
def mailing_by_update_course(email, course, lesson=None):
    mailing_by_subscriptions(email, course, lesson)
