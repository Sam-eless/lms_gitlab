import requests
from rest_framework import status, serializers
from rest_framework.response import Response

from config import settings
from lms.models import Course, Payment
from users.models import User


class StripeAPI:
    url = 'https://api.stripe.com/v1'
    api_key = settings.STRIPE_API_KEY
    headers = {'Authorization': f'Bearer {api_key}'}

    @classmethod
    def create_payment_intent(cls, course_id, user_id):
        course = Course.objects.get(id=course_id)
        amount = course.price + 100  # Для простоты отладки, т.к. цена по умолчанию 0.0
        user = User.objects.get(id=user_id)

        data = [
            ('amount', amount * 100),
            ('currency', 'rub'),
            ('metadata[course_id]', course.id),
            ('metadata[user_id]', user.id)
        ]
        response = requests.post(f'{cls.url}/payment_intents', headers=cls.headers, data=data)
        if response.status_code != 200:
            raise Exception(f'Намерение платежа не создано : {response.json()["error"]["message"]}')

        payment_intent = response.json()
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount,
            payment_intent_id=payment_intent['id'],
            status=payment_intent['status']
        )
        return payment_intent

    @classmethod
    def create_payment_method(cls, payment_token):
        data = {
            'type': 'card',
            'card[token]': payment_token,
        }
        response = requests.post(f'{cls.url}/payment_methods', headers=cls.headers, data=data)
        payment_method = response.json()

        if response.status_code != 200:
            raise Exception(f'Платеж не создан: {response.json()["error"]["message"]}')

        return payment_method

    @classmethod
    def update_payment_intent(cls, payment_intent_id, payment_token):
        payment_method = cls.create_payment_method(payment_token)
        print(payment_method['id'])
        data = {'payment_method': payment_method['id']}
        response = requests.post(f'{cls.url}/payment_intents/{payment_intent_id}', headers=cls.headers, data=data)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f'Метод оплаты не удалось привязать к платежу: {response.json()["error"]["message"]}')
            # Более полный текст ошибки, нужен для отладки
            # raise Exception(f'Метод оплаты не удалось привязать к платежу: {response.json()["error"]}')

        payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        payment.payment_method_id = payment_method['id']
        payment.status = response_data['status']
        payment.save()

        return payment_method

    @classmethod
    def confirm_payment_intent(cls, payment_intent_id):
        payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        url = f'{cls.url}/payment_intents/{payment_intent_id}/confirm'
        if payment.payment_method_id:
            data = {'payment_method': payment.payment_method_id}
            response = requests.post(url, headers=cls.headers, data=data)

        response_data = response.json()
        if response.status_code != 200:
            if payment.status == 'succeeded':
                payment.is_payment_confirmed = True
                payment.save()
                raise Exception(f"Платеж с id {payment_intent_id} уже подтвержден")
            else:
                raise Exception(f'{response.json()["error"]["message"]}')
                # Более полный текст ошибки для отладки
                # raise Exception(f'Платеж не подтвержден: {response.json()["error"]}')

        payment.status = response_data['status']
        payment.save()
        return response_data

    @classmethod
    def retrieve_payment_intent(cls, payment_intent_id):
        payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        url = f'{cls.url}/payment_intents/{payment_intent_id}'
        response = requests.get(url, headers=cls.headers)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f'{response_data["error"]["message"]}')
            # Более полный текст ошибки для отладки
            # raise Exception(f'{response.json()["error"]}')

        payment.status = response_data['status']
        payment.save()
        return response_data
