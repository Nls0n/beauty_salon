from django.contrib import admin
from .models import Category, Service, Employee, EmployeeService, Client, Appointment


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


# Inline-интерфейс для редактирования услуг прямо в карточке сотрудника
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
    
    # Использование полей связанных моделей в фильтрах (__поле)
    list_filter = ('status', 'appointment_datetime', 'employee__position', 'service__category')
    
    # Глубокий поиск по именам клиентов, мастеров и названиям услуг
    search_fields = (
        'client__first_name', 
        'client__phone_number', 
        'employee__first_name', 
        'employee__last_name', 
        'service__name'
    )
    
    # Исключаем просадку производительности при тысячах клиентов/мастеров/услуг
    raw_id_fields = ('client', 'employee', 'service')
    
    date_hierarchy = 'appointment_datetime'  # Удобная навигация по датам вверху админки