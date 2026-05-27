from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Категория"
    )
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин.)")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Должность")
    bio = models.TextField(blank=True, null=True, verbose_name="О мастере")

    services = models.ManyToManyField(
        Service,
        through='EmployeeService',
        related_name='employees',
        verbose_name="Оказываемые услуги"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position or 'Мастер'})"


class EmployeeService(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")

    class Meta:
        verbose_name = "Услуга сотрудника"
        verbose_name_plural = "Услуги сотрудников"
        unique_together = ('employee', 'service')

    def __str__(self):
        return f"{self.employee} — {self.service.name}"


class Client(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.first_name} [{self.phone_number}]"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments", verbose_name="Клиент")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="appointments", verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments", verbose_name="Услуга")
    appointment_datetime = models.DateTimeField(verbose_name="Дата и время записи")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['-appointment_datetime']

    def __str__(self):
        return f"Запись №{self.id} — {self.client.first_name} ({self.appointment_datetime.strftime('%d.%m.%Y %H:%M')})"
