from .views import *
from django.urls import path,include

urlpatterns = [
    path('book_app',Book_app.as_view()),
    path('book_app_load',Staff_load.as_view()),
    path('staff_log',Staff_login.as_view()),
    path('staff_profile',Staff_profile.as_view()),
    path('add_salon',AddSalon.as_view()),
    path('add_appointment',AddAppointment.as_view()),
    path('paygate_appointment',PayAppointment.as_view()),
    path('charge_appointment',ChargeAppointment.as_view()),
    path('add_staff',AddStaff.as_view()),
    path('add_service',AddService.as_view()),
    path('staff_view',StaffView.as_view()),
    path('service_view',ServiceView.as_view()),
    path('salon_view',SalonView.as_view()),
    path('reception_login',ReceptionLogin.as_view()),
    path('manager_login',ManagerLogin.as_view()),
    path('receptionist_accCreation',CreateAccReceptionist.as_view()),
    path('manager_accCreation',CreateAccManager.as_view()),
    path('reception_dashboard',ReceptionDashboard.as_view()),
    path('manager_dashboard',ManagerDashboard.as_view()),


]
