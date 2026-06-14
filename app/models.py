from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User 


class ActiveEmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"

    def __str__(self):
        return self.title


class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    specialty = models.CharField(max_length=100, verbose_name="Специализация")
    is_active = models.BooleanField(default=True, verbose_name="Работает ли сейчас")

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Фото мастера")
    certificate = models.FileField(upload_to="certificates/", null=True, blank=True, verbose_name="Документ/Сертификат (PDF)")

    objects = models.Manager()
    active_objects = ActiveEmployeeManager()

    services = models.ManyToManyField("Service", through="EmployeeService", related_name="employees", verbose_name="Оказываемые услуги")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.first_name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services", verbose_name="Категория", null=True, blank=True)
    title = models.CharField(max_length=150, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_minutes = models.IntegerField(default=30, verbose_name="Длительность (мин)")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class EmployeeService(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    is_primary_skill = models.BooleanField(default=True, verbose_name="Является ли основным профилем мастера")

    class Meta:
        verbose_name = "Услуга мастера"
        verbose_name_plural = "Услуги мастеров"
        unique_together = ("employee", "service")

    def __str__(self):
        return f"{self.employee.first_name} - {self.service.title}"



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    favorite_masters = models.ManyToManyField("Employee", blank=True, related_name="favorite_clients", verbose_name="Любимые мастера")
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")

    social_profile = models.URLField(max_length=200, blank=True, null=True, verbose_name="Ссылка на профиль (VK/TG)")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.first_name


class Appointment(models.Model):
    STATUS_CREATED = "created"
    STATUS_CONFIRMED = "confirmed"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_CONFIRMED, "Подтверждена"),
        (STATUS_COMPLETED, "Выполнена"),
        (STATUS_CANCELED, "Отменена"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments", verbose_name="Клиент")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="appointments", verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments", verbose_name="Услуга")

    appointment_datetime = models.DateTimeField(verbose_name="Дата и время сеанса")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name="Статус")

    updated_at = models.DateTimeField(auto_now=timezone.now, verbose_name="Последнее изменение")

    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-appointment_datetime", "status"]
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    # def __str__(self):
        # return f"Запись #{self.id} — {self.client.first_name}"
