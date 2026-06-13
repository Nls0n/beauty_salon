from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import Appointment, Service

class ServiceSerializer(serializers.ModelSerializer):
    is_expensive = serializers.SerializerMethodField()
    personal_discount = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'title', 'price', 'category', 'is_expensive', 'personal_discount']

    def get_is_expensive(self, obj):
        return obj.price > 3000

    def get_personal_discount(self, obj):
        request = self.context.get('request')
        if request and request.user.is_staff:
            return 15  # Скидка 15% для персонала
        return 0


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'client', 'employee', 'service', 'appointment_datetime', 'price_at_booking']
        read_only_fields = ['price_at_booking', 'client']

    def validate_appointment_datetime(self, value):
        # Валидация БЛ: Запрет записи в прошлое
        if value < timezone.now():
            raise ValidationError("Нельзя записаться на прошедшее время.")
        return value

    def validate(self, data):
        # Валидация БЛ: Проверка накладок (занят ли мастер)
        employee = data.get('employee')
        appointment_datetime = data.get('appointment_datetime')

        overlap = Appointment.objects.filter(
            employee=employee,
            appointment_datetime=appointment_datetime
        ).exists()

        if overlap:
            raise ValidationError({"appointment_datetime": "У этого мастера уже есть запись на выбранное время."})
        return data

    def create(self, validated_data):
        service = validated_data['service']
        validated_data['price_at_booking'] = service.price
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)