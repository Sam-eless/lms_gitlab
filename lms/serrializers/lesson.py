from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('title', 'description', 'course',)


# class LessonDetailSerializer(serializers.ModelSerializer):
#     course = CourseDetailSerializer()
#
#     class Meta:
#         model = Lesson
#         fields = ('title', 'description', 'course', 'number_of_lessons_in_course')


