from django.db import models

class Salon(models.Model):
    salon_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    services = models.CharField(max_length=100)
    opening_date = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    

class Salon_image(models.Model):
    salon = models.ForeignKey(Salon, related_name='Salon_img',on_delete=models.CASCADE)
    salon_img = models.ImageField(upload_to='img/')

class Staff(models.Model):
    staff_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=20)
    skills = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    joining_date = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    staff_img = models.ImageField(upload_to='img/')
    dob = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    shift = models.CharField(max_length=100)
    salon_name = models.CharField(max_length=100)
    

class Appointment(models.Model):
    customer_name = models.CharField(max_length=100)
    treatment = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=10)
    appointment_date = models.CharField(max_length=100)
    appointment_time = models.TimeField()
    assign_staff = models.CharField(max_length=100)

class Services(models.Model):
    service_name = models.CharField(max_length=100)
    service_category = models.CharField(max_length=100)
    service_price = models.IntegerField()
    service_tax = models.FloatField()
    discount = models.FloatField()
    serivice_img = models.ImageField(upload_to='img/')

class Salon_Receptionist(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    salon = models.CharField(max_length=100)

class Salon_Manager(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    salon = models.CharField(max_length=100)
