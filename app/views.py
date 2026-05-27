from django import forms
from django.shortcuts import render, redirect, get_object_or_404

from .models import Appointment, Employee, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'title', 'price', 'duration_minutes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


def DashboardView(request):

    appointments = Appointment.objects.select_related('client', 'employee', 'service').all()

    employees = Employee.objects.prefetch_related('services').all()

    services = Service.objects.select_related('category').all()

    return render(request, 'app/dashboard.html', {
        'appointments': appointments,
        'employees': employees,
        'services': services
    })


def service_create_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ServiceForm()
    return render(request, 'app/service_form.html', {'form': form, 'action': 'Создать'})


def service_edit_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'app/service_form.html', {'form': form, 'action': 'Редактировать'})


def service_delete_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('dashboard')
    return render(request, 'app/service_confirm_delete.html', {'service': service})

def employee_detail_view(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return redirect('dashboard') 
    return render(request, 'app/employee_detail.html', {'employee': employee})

def employee_delete_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('dashboard') # Редирект после успешного удаления
    return render(request, 'app/employee_confirm_delete.html', {'employee': employee})