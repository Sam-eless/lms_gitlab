from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response

from lms.models import Payment, Lesson, Course


class PaymentSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentIntentCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate(self, value):
        course_id = value['course_id']
        try:
            Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Курс c id {course_id} не найден")
        return value


class PaymentMethodCreateSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=255)
    payment_token = serializers.CharField(max_length=255)

    def validate(self, value):
        payment_intent_id = value['payment_intent_id']
        try:
            payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"платеж с id - {payment_intent_id} не найден")
        if payment.is_payment_confirmed:
            raise serializers.ValidationError(f"Платеж с id {payment_intent_id} уже подтвержден (is_confirmed)")
        return value


class PaymentIntentConfirmSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=255)

    def validate(self, value):
        payment_intent_id = value['payment_intent_id']
        try:
            payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"платеж с id - {payment_intent_id} не найден")
        if payment.payment_method_id is None:
            raise serializers.ValidationError(f"У платежа id - {payment_intent_id} нет метода платежа")
        return value


class PaymentIntentDetailSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=255)

    def validate(self, value):
        payment_intent_id = value['payment_intent_id']
        try:
            Payment.objects.get(payment_intent_id=payment_intent_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"платеж с id - {payment_intent_id} не найден")
        return value
