from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from lms.serrializers.course import CourseSerializer

from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@sky.pro", is_staff=True)
        self.user.set_password("123131")
        self.user.save()

        response = self.client.post(
            "/users/api/token/",
            {"email": "admin@sky.pro", "password": "123131"},
            format="json"
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(title="Java2")
        self.lesson = Lesson.objects.create(
            title="History",
            course=self.course
        )
        self.valid_data = {
            'title': 'Update Lesson',
            'description': 'Update Description',
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'owner': self.user.id,
            'course': self.course.title}

    def test_lesson_create(self):
        response = self.client.post(
            reverse("lesson_create"),
            {"course": self.course.title, "title": "English start"},
            format="json"
        )

        self.assertEqual(Lesson.objects.count(), 2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_list(self):
        response = self.client.get(reverse("lesson_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create_validation_error(self):
        response = self.client.post(
            reverse("lesson_create"),
            {"course": self.course.title, "title": "English start", "url": "sky.pro"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_detail(self):
        response = self.client.get(reverse('lesson_detail', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_valid_data(self):
        response = self.client.put(
            reverse('lesson_update', kwargs={'pk': self.lesson.id}),
            data=self.valid_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse('lesson_delete', kwargs={'pk': self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseSubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro", is_staff=True)
        self.user.set_password("123131")
        self.user.save()

        response = self.client.post(
            "/users/api/token/",
            {"email": "admin@sky.pro", "password": "123131"},
            format="json"
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(title="Java2")

    def test_1_subscribe_to_course(self):
        response = self.client.post(reverse('create_subscribe', kwargs={'pk': self.course.pk}), format='json')
        subscription = Subscription.objects.get(user=self.user, course=self.course)
        self.assertTrue(subscription.is_active)

    def test_2_unsubscribe_from_course(self):
        subscription_new = Subscription.objects.create(user=self.user, course=self.course, is_active=True)
        response = self.client.delete(reverse('delete_subscribe', kwargs={'pk': subscription_new.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription_new.refresh_from_db()
        self.assertFalse(subscription_new.is_active)

    def test_3_is_subscribed_to_course(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course, is_active=True)
        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])
        subscription.is_active = False
        subscription.save()
        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertFalse(response.data['is_subscribed'])

    def test_4_get_course_with_subscription(self):
        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CourseSerializer(instance=self.course, context={'request': response.wsgi_request})
        self.assertEqual(response.data, serializer.data)
