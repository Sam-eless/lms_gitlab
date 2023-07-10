from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from lms.models import Lesson
from lms.permissions import OwnerOrStuff
from lms.serrializers.lesson import LessonSerializer, LessonListSerializer


class LessonDetailView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]


class LessonListView(ListAPIView):
    serializer_class = LessonSerializer
    # serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]


class LessonUpdateView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]


class LessonDeleteView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerOrStuff]
