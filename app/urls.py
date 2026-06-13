from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, AppointmentViewSet, EmployeeStatsAPIView

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='api_services')
router.register(r'appointments', AppointmentViewSet, basename='api_appointments')

urlpatterns = [
    path("dashboard/", views.DashboardView, name="dashboard"),
    path("service/new/", views.service_create_view, name="service_create"),
    path("service/<int:pk>/edit/", views.service_edit_view, name="service_edit"),
    path("service/<int:pk>/delete/", views.service_delete_view, name="service_delete"),
    path("analytics/", views.analytics_view, name="analytics"),
    path("", views.home_view, name="home"),
    path('masters/', views.employee_list_view, name='employee_list'),
    path('masters/<int:pk>/', views.employee_detail_view, name='employee_detail'),
    path('masters/create/', views.employee_create_view, name='employee_create'),
    path('masters/<int:pk>/update/', views.employee_update_view, name='employee_update'),
    path('masters/<int:pk>/delete/', views.employee_delete_view, name='employee_delete'),
    path('api/', include(router.urls)),
    path('api/employees/stats/', EmployeeStatsAPIView.as_view(), name='api_employee_stats'),
] + debug_toolbar_urls()
