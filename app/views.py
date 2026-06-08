from django import forms
from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EmployeeForm
from .models import Appointment, Category, Client, Employee, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["category", "title", "price", "duration_minutes"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


def DashboardView(request):

    appointments = Appointment.objects.all() #select_related("client", "employee", "service")



    employees = Employee.objects.prefetch_related("services").all()

    services = Service.objects.select_related("category").all()


    return render(request, "app/dashboard.html", {"appointments": appointments, "employees": employees, "services": services})


def service_create_view(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ServiceForm()
    return render(request, "app/service_form.html", {"form": form, "action": "Создать"})


def service_edit_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ServiceForm(instance=service)
    return render(request, "app/service_form.html", {"form": form, "action": "Редактировать"})


def service_delete_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        return redirect("dashboard")
    return render(request, "app/service_confirm_delete.html", {"service": service})


def employee_detail_view(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return redirect("dashboard")
    return render(request, "app/employee_detail.html", {"employee": employee})


def employee_delete_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect("dashboard")  # Редирект после успешного удаления
    return render(request, "app/employee_confirm_delete.html", {"employee": employee})


def analytics_view(request):
    # __contains — поиск с учетом регистра (case-sensitive)
    exact_match_services = Service.objects.filter(title__contains="стрижка")

    # __icontains — поиск без учета регистра (case-insensitive)
    any_case_services = Service.objects.filter(title__icontains="стрижка")

    services_dicts = Service.objects.values("title", "price")

    # values_list() возвращает QuerySet, состоящий из КОРТЕЖЕЙ ('значение1', 'значение2')
    # Если передать flat=True (работает только для одного поля), вернет простой плоский список значений
    client_phones = Client.objects.values_list("phone_number", flat=True)

    # count() делает в базе 'SELECT COUNT(*)' вместо вытягивания записей в Python
    total_appointments = Appointment.objects.count()

    # exists() возвращает True/False. Оптимизирует запрос, завершая его, как только найдена ХОТЯ БЫ одна запись
    has_broken_clients = Client.objects.filter(phone_number="").exists()

    trigger_action = request.GET.get("action")

    if trigger_action == "mass_discount":
        # update() выполняется на уровне SQL и НЕ вызывает метод save() модели
        Service.objects.filter(price__gt=3000).update(price=models.F("price") - 300)
        return redirect("analytics")

    elif trigger_action == "clean_canceled":
        month_ago = timezone.now() - timezone.timedelta(days=30)
        Appointment.objects.filter(status="canceled", appointment_datetime__lt=month_ago).delete()
        return redirect("analytics")

    context = {
        "exact_match_services": exact_match_services,
        "any_case_services": any_case_services,
        "services_dicts": services_dicts[:5],
        "client_phones": list(client_phones)[:5],
        "total_appointments": total_appointments,
        "has_broken_clients": has_broken_clients,
    }

    return render(request, "app/analytics.html", context)


def home_view(request):
    search_query = request.GET.get("q", "")
    search_results = None

    if search_query:
        search_results = Service.objects.filter(title__icontains=search_query).select_related("category")

    # считаем количество их записей (агрегация COUNT) и сортируем по убыванию
    top_masters = Employee.objects.filter(is_active=True).annotate(appointments_count=Count("appointments")).order_by("-appointments_count")[:4]

    categories = Category.objects.annotate(services_count=Count("services")).all()

    # distinct() - получаем список уникальных специализаций в салоне
    unique_specialties = Employee.objects.values_list("specialty", flat=True).distinct()

    try:
        vip_service = Service.objects.get(id=1)
    except Service.DoesNotExist:
        vip_service = None

    context = {
        "search_query": search_query,
        "search_results": search_results,
        "top_masters": top_masters,
        "categories": categories,
        "unique_specialties": unique_specialties,
        "vip_service": vip_service,
    }

    return render(request, "app/home.html", context)


def employee_list_view(request):
    employees = Employee.objects.all().order_by("-id")
    return render(request, "app/employee_list.html", {"employees": employees})


def employee_detail_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    services = employee.services.all()
    return render(request, "app/employee_detail.html", {"employee": employee, "services": services})


def employee_create_view(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm()
    return render(request, "app/employee_form.html", {"form": form, "action": "Добавить мастера"})


def employee_update_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "app/employee_form.html", {"form": form, "action": "Редактировать мастера"})


def employee_delete_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")
    return render(request, "app/employee_confirm_delete.html", {"employee": employee})
