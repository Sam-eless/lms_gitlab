# Generated by Django 4.2.3 on 2023-07-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Стоимость курса'),
        ),
    ]