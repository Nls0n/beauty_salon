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
        fields = ['id', 'employee', 'service', 'appointment_datetime', 'price_at_booking']
        read_only_fields = ['client', 'price_at_booking']

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
        request = self.context.get('request')
        
        # Проверяем, есть ли у юзера профиль клиента
        if not hasattr(request.user, 'client_profile'):
            raise serializers.ValidationError({
                "detail": "У текущего пользователя нет привязанного профиля Client."
            })
            
        # Присваиваем клиента из профиля юзера
        validated_data['client'] = request.user.client_profile
        
        # (Опционально) Устанавливаем цену из сервиса
        service = validated_data.get('service')
        validated_data['price_at_booking'] = service.price
        
        return super().create(validated_data)