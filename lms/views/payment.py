from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Lesson, Payment
from lms.serrializers.payment import PaymentSerializer, PaymentIntentCreateSerializer, PaymentMethodCreateSerializer, \
    PaymentIntentConfirmSerializer, PaymentIntentDetailSerializer
from lms.services.stripe_api import StripeAPI


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date', 'amount']
    permission_classes = [IsAuthenticated]


class PaymentIntentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PaymentIntentCreateSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = PaymentIntentCreateSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            user_id = request.user.id
            try:
                payment_intent = StripeAPI.create_payment_intent(course_id, user_id)
                payment = Payment.objects.get(payment_intent_id=payment_intent['id'])
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PaymentMethodCreateSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = PaymentMethodCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            payment_token = serializer.validated_data['payment_token']
            try:
                StripeAPI.update_payment_intent(payment_intent_id, payment_token)
                payment = Payment.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentConfirmView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PaymentIntentConfirmSerializer()})
    def post(self, request, *args, **kwargs):

        serializer = PaymentIntentConfirmSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            try:
                StripeAPI.confirm_payment_intent(payment_intent_id)
                payment = Payment.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PaymentIntentDetailSerializer()})
    def get(self, request, *args, **kwargs):

        serializer = PaymentIntentDetailSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            try:
                StripeAPI.retrieve_payment_intent(payment_intent_id)
                payment = Payment.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_200_OK)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
