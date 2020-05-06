from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .models import *
from sales.views import *
from .services import *
from .serializer import *
from django.conf import settings
from twilio.rest import Client

stripe.api_key = settings.STRIPE_SECRET_KEY
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

class ReceptionLogin(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):
        return render(request,'reception_login.html')
    def post(self, request):
        se = LoginSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            username = request.data.get('username')
            password = request.data.get('password')
            user_exist = Salon_Receptionist.objects.filter(username=username).exists()
            user = Salon_Receptionist.objects.filter(username=username)
            if user_exist:
                for i in user:
                    check = check_password(password,i.password)
                if check:
                    reception.name = username
                    user = authenticate(username=username,password=password)
                    if user is not None:
                        login(request,user)
                        return HttpResponseRedirect('reception_dashboard')
                    else:
                        return Response({"Response":"User is not authorized user"})
                else:
                    return Response({"Response":"check password"})
            else:
                return Response({"Response":"check username"})

reception = ReceptionLogin()


class ReceptionDashboard(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        print(request.user)
        context = {}
        get_salon = Salon_Receptionist.objects.filter(username=reception.name)
        for i in get_salon:
            salon = i.salon
        get_staff = Staff.objects.filter(salon_name=salon)
        for i in get_staff:
            staff = i.staff_name
            appointment = Appointment.objects.filter(assign_staff=staff)
            appointment_dict = {i.staff_name:appointment}
            context.update(appointment_dict)
        return render(request,'reception_dashboard.html',{'context':context})

class ManagerDashboard(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        context = {}
        get_salon = Salon_Receptionist.objects.filter(username=reception.name)
        for i in get_salon:
            salon = i.salon
        get_staff = Staff.objects.filter(salon_name=salon)
        for i in get_staff:
            staff = i.staff_name
            appointment = Appointment.objects.filter(assign_staff=staff)
            appointment_dict = {i.staff_name:appointment}
            context.update(appointment_dict)
        return render(request,'manager_dashboard.html',{'context':context})

class ManagerLogin(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):
        return render(request,'manager_login.html')
    def post(self, request):
        se = LoginSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            username = request.data.get('username')
            password = request.data.get('password')
            user_exist = Salon_Manager.objects.filter(username=username).exists
            if user_exist:
                for i in user_exist:
                    check = check_password(password,i.password)
                if check:
                    user = authenticate(username=username,password=password)
                    if user is not None:
                        login(request,user)
                        return HttpResponseRedirect('manager_dashboard')
                else:
                    return Response({"Response":"check password"})
            else:
                return Response({"Response":"check username"})

class CreateAccReceptionist(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render (request,'createacc_receptionist.html')
    def post(self,request):
        se = ReceptionSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            username = request.data.get('username')
            salon = request.data.get('salon')
            salon_exist = Salon.objects.filter(salon_name=salon).exists()
            password = request.data.get('password')
            password1 = request.data.get('confirm_password')
            string = 'Account created for' + ' ' + username +' '+ 'salon'
            string1 = "salon" + ' ' + salon + ' ' + 'is not exist'
            if salon_exist:
                if password == password1:
                    acc = Salon_Receptionist.objects.create(username=username, password=make_password(password),salon=salon)
                    user = User.objects.create_user(username=username,password=password)
                    return Response({"Response":string})
                else:
                    return Response({"Response":'Verify your password'})
            else:
                return Response({"Response":string1})

class CreateAccManager(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render (request,'createacc_manager.html')
    def post(self,request):
        se = ManagerSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            username = request.data.get('username')
            salon = request.data.get('salon')
            salon_exist = Salon.objects.filter(salon_name=salon).exists()
            password = request.data.get('password')
            password1 = request.data.get('confirm_password')
            string = 'Account created for' + ' ' + username +' '+ 'salon'
            string1 = "salon" + ' ' + salon + ' ' + 'is not exist'
            if salon_exist:
                if password == password1:
                    acc = Salon_Manager.objects.create(username=username, password=make_password(password),salon=salon)
                    return Response({"Response":string})
                else:
                    return Response({"Response":'Verify your password'})
            else:
                return Response({"Response":string1})

class StaffView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        staff = Staff.objects.all()
        return render(request, 'stafflist_view.html',{"staff":staff})

class AddStaff(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render(request,'add_staff.html')
    def post(self, request):
        se = StaffSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            try :
                staff_name = request.data.get("staff_name")
                job_title = request.data.get("job_title")
                skills = request.data.get("skills")
                location = request.data.get("branch")
                contact_number = request.data.get("contact_number")
                address = request.data.get("address")
                joining_date = request.data.get("joining_date")
                email = request.data.get("email")
                staff_img = request.data.get("staff_img")
                dob = request.data.get('dob')
                gender = request.data.get("gender")
                shift = request.data.get("shift")
                salon_name = request.data.get("salon_name")
                salon = Salon.objects.filter(salon_name=salon_name).exists()
                AddingStaff(staff_name,job_title,skills,location,contact_number,
                            address,joining_date,email,staff_img,dob,gender,shift,salon_name)
                return Response({"Response":"Staff has been added"})
            except Exception as e:
                return Response({"Response":str(e)})

class AppointmentView(APIView):
    #permission_classes = [IsAdminUser,]
    def get(self,request):
        appointment = Appointment.objects.all()
        return render(request, 'appointmentlist_view.html',{"appointment":appointment})

class AddAppointment(APIView):
    #permission_classes = [IsAdminUser]
    def get(self,request):
        print(request.user)
        return render(request,'add_appointment.html')
    def post(self, request):
        se = AppointmentSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            try :
                app.customer_name = request.data.get("customer_name")
                app.treatment = request.data.get("treatment")
                app.customer_address = request.data.get("customer_address")
                app.customer_number = request.data.get("customer_number")
                app.appointment_date = request.data.get("appointment_date")
                app.appointment_time = request.data.get("appointment_time")
                app.assign_staff = request.data.get("assign_staff")
                service_price = Services.objects.get(service_name=app.treatment)
                app.service_price = service_price.service_price
                return HttpResponseRedirect('paygate_appointment')
            except Exception as e:
                return Response({"Response":str(e)})
app = AddAppointment()

class PayAppointment(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,**kwargs):
        context = {}
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        tot = {"tot":app.service_price}
        tot.update(context)
        return render(request,'paygate_app.html',tot)

class ChargeAppointment(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request):
        charge = stripe.Charge.create(
                amount = int(app.service_price),
                currency='INR',
                description='A Django charge',
                source=request.POST['stripeToken']
            )
        sender = "whatsapp:+14155238886"
        receiver = 'whatsapp:+91{0}'.format(app.customer_number)
        body = 'Hi {0} You have an appointment coming up on {1} at {2}.'.format(app.customer_name,app.appointment_date,app.appointment_time)
        message=client.messages.create(body=body,from_= sender,to=receiver)
        AddingAppointment(app.customer_name,app.treatment,app.customer_address,app.customer_number,
                            app.appointment_date,app.appointment_time,app.assign_staff)
        return render(request, 'charge_app.html')

    def get(self,request):
        return render(request, 'charge_app.html')


class SalonView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        salon = Salon.objects.all()
        return render(request, 'salonlist_view.html',{"salon":salon})

class AddSalon(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render(request,'add_salon.html')
    def post(self, request):
        se = SalonSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            try :
                salon_name = request.data.get("salon_name")
                location = request.data.get("branch")
                contact_number = request.data.get("contact_number")
                services = request.data.get("services")
                opening_date = request.data.get("opening_date")
                email = request.data.get("email")
                salon_img = request.data.get("salon_img")
                AddingSalon(salon_name,location,contact_number,services,opening_date,email,salon_img)
                return Response({"Response":"Salon has been added"})
            except Exception as e:
                return Response({"Response":str(e)})

class ServiceView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        service = Services.objects.all()
        return render(request, 'servicelist_view.html',{"service":service})

class AddService(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render(request,'add_service.html')
    def post(self, request):
        se = ServiceSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            try :
                service_name = request.data.get("service_name")
                service_category = request.data.get("service_category")
                service_price = request.data.get("service_price")
                service_tax = request.data.get("service_tax")
                discount = request.data.get("discount")
                serivice_img = request.data.get("appointment_time")
                AddingService(service_name,service_category,service_price,service_tax,
                            discount,serivice_img)
                return Response({"Response":"Service has been added"})
            except Exception as e:
                return Response({"Response":str(e)})


# class Book_app(APIView):
#     permission_classes = [IsAdminUser]
#     def post(self, request):

#         book.treatment=request.data.get('treatment')
#         book.time = request.data.get('time')
#         outlet = request.data.get('outlet')
#         return HttpResponseRedirect('book_app_load')

#     def get(self, request):
#         return render(request, 'book_app.html')
# book = Book_app()

# class Staff_load(APIView):
#     def get(self, request):
#         staf = Staff.objects.filter(expertise=book.treatment)
#         for i in staf:
#             k = Appointments.objects.filter(staff_id=i.staff_name)
#             print(k.staff_id)
#         return render(request, 'book_app_load.html',{"staf":staf,"treatment":book.treatment})
#     def post(self, request):
#         if request.data.get("test"):
#             s.staff = request.data.get('staff')

#         free = App_req.objects.filter(staff=s.staff,time=request.data.get('time')).exists()
#         free1 = Appointments.objects.filter(staff_id=s.staff,time=request.data.get('time')).exists()
#         if not free:
#             if not free1:
#                 try:
#                         customer_n=login.name
#                         treatment = book.treatment
#                         AppointmentReqCreation(s.staff,customer_n,treatment,time,outlet)
#                         return Response({"ok":"ok"})

#                 except Exception as e:

#                     return Response(str(e))
#             else:

#                 return Response("data is already booked")
#         else:

#             return Response("data is already booked")
# s = Staff_load()

# class Crm(APIView):
#     def get(self, request):
#         return render(request, 'crm.html')

# class Staff_login(APIView):
#     def get(self, request):
#         return render(request,"staff_login.html")
#     def post(self, request):
#         user_exist = Staff.objects.filter(email=request.data.get('email')).exists()
#         # ps = Staff.objects.filter(
#         #     email=request.data.get('email'),
#         #     password=request.data.get('password'))
#         if user_exist:
#             if  True:
#                 staff = Staff.objects.get(email=request.data.get('email'))
#                 obj_staff.n=staff.staff_name
#                 return HttpResponseRedirect('staff_profile')
#             else:
#                 return Response({"Response":"plz check ur email "})
#         else:
#             return Response("email is not valid")
# obj_staff = Staff_login()


# class Staff_profile(APIView):
#     authentication_classes = [TokenAuthentication,]
#     #permission_classes = [IsAuthenticated]
#     def get(self, request):
#         con = Appointment.objects.filter(assign_staff=obj_staff.n)
#         return render(request, "staff_profile.html",{"con":con})
#     def post(self, request):
#         pass
#         return Response({"Response":"Need to code"})

# pro = Staff_profile()
