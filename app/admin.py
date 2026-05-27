from django.contrib import admin

from .models import Appointment, Category, Client, Employee, EmployeeService, Service


class EmployeeServiceInline(admin.TabularInline):
    model = EmployeeService
    extra = 1

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'specialty', 'is_active')
    list_filter = ('is_active', 'specialty')
    search_fields = ('first_name', 'specialty')
    inlines = [EmployeeServiceInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'duration_minutes')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone_number', 'registration_date')
    search_fields = ('first_name', 'phone_number')
    readonly_fields = ('registration_date',)
    filter_horizontal = ('favorite_masters',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # list_display со своим методом, декоратором @admin.display и short_description
    list_display = ('id', 'client', 'employee', 'service', 'appointment_datetime', 'status_badge', 'formatted_price')
    list_display_links = ('id', 'client')

    list_filter = ('status', 'appointment_datetime', 'employee')

    search_fields = ('client__first_name', 'client__phone_number')

    raw_id_fields = ('client', 'employee', 'service') # Защита от тяжелых select-запросов
    date_hierarchy = 'appointment_datetime'

    @admin.display()
    def status_badge(self, obj):
        from django.utils.html import format_html
        colors = {
            'created': '#ffc107',
            'confirmed': '#17a2b8',
            'completed': '#28a745',
            'canceled': '#dc3545',
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )

    status_badge.short_description = 'Статус визита'


    @admin.display()
    def formatted_price(self, obj):
        return f"{obj.service.price} ₽"

    formatted_price.short_description = 'Стоимость'
