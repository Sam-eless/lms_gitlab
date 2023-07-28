from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Subscription
from lms.permissions import OwnerOrStuff
from lms.serrializers.course import CourseSerializer
from lms.services.mailing_subscription import mailing_by_subscriptions
from lms.tasks import mailing_by_update_course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, OwnerOrStuff]

    def update(self, request, *args, **kwargs):
        course_id = self.kwargs['pk']
        course = get_object_or_404(Course, id=course_id)
        subscriptions = Subscription.objects.filter(course=course)
        if course.is_active:
            for subscription in subscriptions:
                email = subscription.user.email
                mailing_by_update_course.delay(email, course=course.title)
        return super().update(request, *args, **kwargs)
