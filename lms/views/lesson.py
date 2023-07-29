from rest_framework import status
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, CreateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Lesson, Course, Subscription
from lms.pagination import CustomPagination
from lms.permissions import OwnerOrStuff
from lms.serrializers.lesson import LessonSerializer
from lms.services.mailing_subscription import mailing_by_subscriptions
from lms.tasks import mailing_by_update_course


class LessonDetailView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]


class LessonListView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]
    pagination_class = CustomPagination


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, OwnerOrStuff]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        lesson_title = self.request.data['title']
        lesson = get_object_or_404(Lesson, title=lesson_title)
        course = get_object_or_404(Course, id=lesson.course_id)

        subscriptions = Subscription.objects.filter(course=course)
        if lesson.is_active and course.is_active:
            for subscription in subscriptions:
                email = subscription.user.email
                mailing_by_update_course.delay(email, lesson=lesson.title, course=course.title)
        return Response(request.data, status=status.HTTP_201_CREATED)


class LessonUpdateView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]

    def partial_update(self, request, *args, **kwargs):

        lesson_id = self.kwargs['pk']
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course = get_object_or_404(Course, id=lesson.course_id)

        subscriptions = Subscription.objects.filter(course=course)
        if lesson.is_active and course.is_active:
            for subscription in subscriptions:
                email = subscription.user.email
                mailing_by_update_course.delay(email, lesson=lesson.title, course=course.title)
        return super().partial_update(request, *args, **kwargs)


class LessonDeleteView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]
