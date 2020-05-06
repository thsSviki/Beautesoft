from .models import *
from . import views
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User



def AddingSalon(salon_name,location,contact_number,services,opening_date,email,salon_img):
    add = Salon.objects.create(salon_name=salon_name,
                                branch=location,
                                contact_number=contact_number,
                                services=services,
                                opening_date=opening_date,
                                email=email)
    img = Salon_image.objects.create(salon=add,salon_img=salon_img)

def AddingStaff(staff_name,job_title,skills,location,contact_number,
                address,joining_date,email,staff_img,dob,gender,shift,salon_name):
    
    add = Staff.objects.create(staff_name=staff_name,job_title=job_title,
                               skills=skills,branch=location,contact_number=contact_number,
                               address=address,joining_date=joining_date,email=email,
                               staff_img=staff_img,dob=dob,gender=gender,shift=shift,salon_name=salon_name)
    

def AddingAppointment(customer_name,treatment,customer_address,customer_number,
                            appointment_date,appointment_time,assign_staff):
    add = Appointment.objects.create(customer_name=customer_name,treatment=treatment,
                                     customer_address=customer_address,
                                     customer_number=customer_number,
                                     appointment_date=appointment_date,
                                     appointment_time=appointment_time,
                                     assign_staff=assign_staff)

def AddingService(service_name,service_category,service_price,service_tax,
                            discount,serivice_img):    
    add = Services.objects.create(service_name=service_name,service_category=service_category,
                                    service_price=service_price,service_tax=service_tax,
                                    discount=discount,serivice_img=serivice_img)
