from django.contrib import admin

from .models import Appointment, Category, Client, Employee, EmployeeService, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'duration_minutes')
    list_filter = ('category',)
    search_fields = ('name', 'category__title')
    # Защита от выпадающего списка категорий, если их станет много
    raw_id_fields = ('category',)


class EmployeeServiceInline(admin.TabularInline):
    model = EmployeeService
    extra = 1
    raw_id_fields = ('service',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'position')
    list_filter = ('position',)
    search_fields = ('first_name', 'last_name', 'position')
    inlines = [EmployeeServiceInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'registration_date')
    search_fields = ('first_name', 'phone_number')
    list_filter = ('registration_date',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'service', 'appointment_datetime', 'status')

    list_filter = ('status', 'appointment_datetime', 'employee__position', 'service__category')

    search_fields = (
        'client__first_name',
        'client__phone_number',
        'employee__first_name',
        'employee__last_name',
        'service__name'
    )

    raw_id_fields = ('client', 'employee', 'service')

    date_hierarchy = 'appointment_datetime'
