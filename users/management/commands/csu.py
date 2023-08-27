from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.get(email="admin@sky.pro"):
            user = User.objects.create(
                email='admin@sky.pro',
                first_name='admin',
                last_name='admin',
                is_staff=True,
                is_superuser=True
            )

            user.set_password('123131')
            user.save()
