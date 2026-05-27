from datetime import timedelta

from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_repr_or_404, render
from django.utils import timezone

from .models import Appointment, Client, Employee, Service


def analytics_and_search_view(request):
    ivan_appointments = Appointment.objects.filter(employee__first_name="Иван")

    future_appointments = Appointment.objects.filter(appointment_datetime__gt=timezone.now())


    active_workflow_appointments = Appointment.objects.exclude(status=Appointment.STATUS_CANCELED)



    ordered_services = Service.objects.all().order_by('price', 'title')


    avg_service_price = Service.objects.aggregate(average_price=Avg('price'))

    clients_with_appointment_count = Client.objects.annotate(total_visits=Count('appointments'))

    employees_with_revenue = Employee.objects.filter(
        appointments__status=Appointment.STATUS_COMPLETED
    ).annotate(
        total_revenue=Sum('appointments__service__price')
    )


    seven_days_ago = timezone.now() - timedelta(days=7)
    new_clients = Client.objects.filter(registration_date__gte=seven_days_ago)


    context = {
        'avg_price': avg_service_price['average_price'],
        'ordered_services': ordered_services,
        'clients': clients_with_appointment_count,
        'new_clients': new_clients,
    }
    return render(request, 'app/analytics.html', context)


def service_detail_view(request, pk):
    """Страница конкретной услуги."""
    service = get_object_or_repr_or_404(Service, pk=pk)
    return render(request, 'app/service_detail.html', {'service': service})
