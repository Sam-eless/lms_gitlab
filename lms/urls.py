from django.urls import path
from rest_framework import routers

from lms.views.course import *
from lms.views.lesson import *
from lms.views.payment import *

urlpatterns = [
    # Lessons
    path('', LessonListView.as_view()),
    path('<int:pk>/', LessonDetailView.as_view()),
    path('<int:pk>/update/', LessonUpdateView.as_view()),
    path('create/', LessonCreateView.as_view()),
    path('<int:pk>/delete/', LessonDeleteView.as_view()),

    # Payment
    path('payment/', PaymentListView.as_view()),

]

router = routers.SimpleRouter()
router.register('course', CourseViewSet)

urlpatterns += router.urls


