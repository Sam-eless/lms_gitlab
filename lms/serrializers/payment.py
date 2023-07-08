from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from lms.models import Payment, Lesson, Course


class PaymentSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'
