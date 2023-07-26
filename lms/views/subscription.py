from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Subscription
from lms.serrializers.subscription import SubscriptionSerializer


class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: SubscriptionSerializer()})
    def post(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
        if created:
            message = f'Вы подписались на обновления курса "{course.title}"'
        else:
            if subscription.is_active:
                message = f'Вы уже подписаны на обновления курса "{course.title}"'
            else:
                subscription.is_active = True
                subscription.save()
                message = f'Вы успешно подписались на обновления курса "{course.title}"'
        return Response({'message': message}, status=status.HTTP_200_OK)


class SubscriptionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        subscription = get_object_or_404(Subscription, user=request.user, course=course)
        if not subscription.is_active:
            message = f'Вы уже отписались от обновлений курса "{course.title}"'
        else:
            subscription.is_active = False
            subscription.save()
            message = f'Вы успешно отписались от обновлений курса "{course.title}"'
        return Response({'message': message}, status=status.HTTP_200_OK)
