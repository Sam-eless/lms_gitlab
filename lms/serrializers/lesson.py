from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from lms.models import Lesson, Course
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    validators = [UrlValidator(field="url")]

    class Meta:
        model = Lesson
        fields = '__all__'

# class LessonListSerializer(serializers.ModelSerializer):
#     course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
#
#     class Meta:
#         model = Lesson
#         fields = ('title', 'description', 'course',)
# validators = [UrlValidator(field="url")]
