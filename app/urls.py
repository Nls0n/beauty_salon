from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView, name="dashboard"),
    path("service/new/", views.service_create_view, name="service_create"),
    path("service/<int:pk>/edit/", views.service_edit_view, name="service_edit"),
    path("service/<int:pk>/delete/", views.service_delete_view, name="service_delete"),
]
