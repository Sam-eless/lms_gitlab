from django.urls import path
from rest_framework import routers

from lms.views.course import *
from lms.views.lesson import *
from lms.views.payment import *
from lms.views.subscription import SubscriptionCreateView, SubscriptionDeleteView

urlpatterns = [
    # Lessons
    path('', LessonListView.as_view(), name="lesson_list"),
    path('<int:pk>/', LessonDetailView.as_view(), name="lesson_detail"),
    path('<int:pk>/update/', LessonUpdateView.as_view(), name="lesson_update"),
    path('create/', LessonCreateView.as_view(), name="lesson_create"),
    path('<int:pk>/delete/', LessonDeleteView.as_view(), name="lesson_delete"),

    # Payment
    path('payment/', PaymentListView.as_view()),
    path('payment/payment-intent-create/', PaymentIntentCreateView.as_view(), name='payment_intent_create'),
    path('payment/payment-method-create/', PaymentMethodCreateView.as_view(), name='payment_method_create'),
    path('payment/payment-confirm/', PaymentIntentConfirmView.as_view(), name='payment_confirm'),
    path('payment/payment-detail/', PaymentIntentDetailView.as_view(), name='payment_detail'),

    # Subscription
    path('course/<int:pk>/create/', SubscriptionCreateView.as_view(), name="create_subscribe"),
    path('course/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name="delete_subscribe"),

]

router = routers.SimpleRouter()
router.register('course', CourseViewSet)

urlpatterns += router.urls


