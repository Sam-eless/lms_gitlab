from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from lms.models import Course, Lesson, Subscription
# from lms.serrializers.lesson import LessonDetailSerializer
from lms.serrializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons_in_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    # lessons = LessonListSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        model = Course
        fields = '__all__'

    def get_number_of_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                subscription = Subscription.objects.get(user=request.user, course=course)
                return subscription.is_active
            except Subscription.DoesNotExist:
                return False
        else:
            return False

    # def get_lessons(self, instance):
    #     lessons = instance.lesson_set.all()
    #     if lessons:
    #         return [{lesson.title, lesson.description} for lesson in lessons]
    #         # return lessons
    #     return 0
