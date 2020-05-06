from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework.views import APIView
from .serializer import *
from .models import *
import stripe
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .services import *
from appointment.models import *
from django.contrib.auth.hashers import make_password,check_password
from django_simple_coupons.validations import validate_coupon
from django_simple_coupons.models import Coupon
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY


class Create(APIView):
    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')
        user = Admin.objects.create(username=username,password=make_password(password))
        usr = User.objects.create_user(username=username,password=password)
        return Response({'Response':'created'})
        

class Login(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        return render(request, "admin_signin.html")
    def post(self, request):
        se = UserSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            user_exist = Admin.objects.filter(username=request.data.get('username')).exists()
            password = request.data.get('password')
            username = request.data.get('username')
            user = authenticate(username=username,password=password)
            get_user = Admin.objects.filter(username=username)
            for i in get_user:
                check = check_password(password,i.password)
            if  user_exist:
                if  check:
                    if user is not None:
                        login(request,user)
                        return HttpResponseRedirect('admin')
                else:
                    return Response({"Response":"plz verify your password"})
            else:
                return  Response({"Response":"Email is not registered"})
admin = Login()

class Logout(APIView):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')

class AdminDashboard(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        print(request.user)
        return render(request, 'admin_dashboard.html')

class ProductView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        product = Product.objects.all()
        return render(request,'productlist_view.html',{"product":product})

class AddProduct(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render(request,'add_product.html')
    def post(self, request):
        se = ProductSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            try :
                product_name = request.data.get("product_name")
                product_category = request.data.get("product_category")
                brand = request.data.get("brand")
                product_size = request.data.get("product_size")
                product_price = request.data.get("product_price")
                discount = request.data.get("discount")
                product_tax = request.data.get("product_tax")
                product_img = request.data.get("product_img")
                expiry_date = request.data.get('expiry_date')
                stock = request.data.get('stock')
                AddingProduct(product_name,product_category,brand,product_size,
                            product_price,discount,product_tax,product_img,expiry_date,stock)
                return Response({"Response":"Product has been added"})
            except Exception as e:
                return Response({"Response":str(e)})

class CustomerView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        customer = Customer.objects.all()
        return render(request,'customerlist_view.html',{"customer":customer})


class AddCustomer(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        return render(request,'add_customer.html')
    def post(self, request):
        se = CustomerSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            try :
                customer_name = request.data.get("customer_name")
                address = request.data.get("address")
                email = request.data.get("email")
                contact_number = request.data.get("contact_number")
                AddingCustomer(customer_name,address,email,contact_number)
                return Response({"Response":"Customer has been added"})
            except Exception as e:
                return Response({"Response":str(e)})

class Voucher(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return render(request, 'coupon.html')
    def post(self, request,*args, **kwargs):
        user = User.objects.get(username=select.name)
        coupon_code = request.data.get("coupon_code")
        status = validate_coupon(coupon_code=coupon_code, user=user)
        if status['valid']:
            coupon = Coupon.objects.get(code=coupon_code)
            discount = coupon.get_discount()
            offer = (discount['value']/100) * catalog.total
            catalog.total = catalog.total - offer
            coupon.use_coupon(user=user)
            return HttpResponseRedirect('paygate')
        else:
            return Response({"Response":"Not valid"})

class Billing(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return render(request,"billing.html")
    def post(self, request):
        se = AddressSerializer(data=request.data)
        if se.is_valid(raise_exception=True):
            name = select.name
            email = request.data.get('email')
            area = request.data.get('area')
            pin = request.data.get('pin')
            phone_number = request.data.get('phone_number')
            state = request.data.get('state')
            remarks = request.data.get('remarks')
            try:
                BillingCreation(name,email,area,pin,phone_number,state,remarks)
                return HttpResponseRedirect('payment_method')
            except Exception as e :
                return Response({"response":str(e)})

class PayMethod(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return render(request,'paymethod.html')
        
    def post(self, request):
        if request.data.get("method1"):

            if top.topup > cat.total:
                successful_order()
                #Customer.objects.filter(email=obj.n).update(topup=top.topup-cat.total)
                Clearance()
                return render(request,"charge.html")
            elif top.topup < cat.total :
                cat.total = cat.total - top.topup
                Custom.objects.filter(email=obj.n).update(topup=0)
                return HttpResponseRedirect('paygate')

        elif request.data.get("method2"):
            return HttpResponseRedirect('paygate')




class Pay(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,**kwargs):
        if request.user.is_authenticated:
            context = {}
            context['key'] = settings.STRIPE_PUBLISHABLE_KEY
            tot = {"tot":cat.total}
            tot.update(context)
            return render(request,'paygate.html',tot)
        else:
            return HttpResponseRedirect('/')


class Charge(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request):
        charge = stripe.Charge.create(
                amount = int(catalog.total),
                currency='INR',
                description='A Django charge',
                source=request.POST['stripeToken']
            )
        Placed_orders()
        Clearance()
        return render(request, 'charge.html')

    def get(self,request):
        if request.user.is_authenticated:
             return render(request, 'charge.html')
        else:
            return HttpResponseRedirect('/')

class FrdSearchApi(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
         return render(request, "friends.html")
        
    def post(self, request):
        if request.data.get("test"):
            frd.name = request.data.get("name")
        return HttpResponseRedirect('results')

frd = FrdSearchApi()

class Result(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        if select.name != frd.name:
            if Customer.objects.filter(customer_name=frd.name).exists():
                results = Customer.objects.filter(customer_name=frd.name)
                return render(request, "result.html", {"results":results})
            else:
                return Response({"Response":"No Results Found"})
        else:
            return Response({"Response":"Try With Different Name"})

    def post (self, request):
        email_g=request.data.get("email")
        name_g=request.data.get("name")
        return HttpResponseRedirect('gift')

class SendGift(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        gift = Appointment.objects.filter(customer_name=select.name)
        return render(request, "gift.html",{"gift":gift})
        
    def post(self, request):
        Appointment.objects.filter(customer_name=select.name).update(customer_n=frd.name)
        return Response("gifted")

class Topup(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        return render(request, "topup.html")
    def post(self,request):
        top.amount = request.data.get("Amount")
        return HttpResponseRedirect('topuppay')
top = Topup()

class TopupPay(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,**kwargs):
        context = {}
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        tot = {"tot":top.amount}
        tot.update(context)
        return render(request,'topuppay.html',tot)
        

class TopupCharge(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request):
        charge = stripe.Charge.create(
                amount = int(top.amount),
                currency='INR',
                description='Topup for Beautesoft',
                source=request.POST['stripeToken']
            )
        topup = Customer.objects.get(customer_name=select.name)

        Customer.objects.filter(customer_name=select.name).update(topup=topup.topup+int(top.amount))
        return render (request,"topupcharge.html")

class SelectCustomer(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        customer = Customer.objects.all()
        return render(request, 'select_customer.html',{"customer":customer})
        
    def post(self, request):
        if request.data.get('test'):
            select.name = request.data.get('customer')
        return HttpResponseRedirect('catalog')
select = SelectCustomer()

class Catalog(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            pro = Product.objects.all()
            items = Purchase.objects.filter(purchaser=select.name)
            total = 0
            for i in items:
                total += i.price
            catalog.total = total
            return render(request,"catalog.html",{"pro":pro,"items":items,"total":total})
        except Exception as e:
            return Response({"response":str(e)})
        
    def post(self, request):
        r_product = request.data.get('r_product')
        r_price = request.data.get('r_price')
        Remove(r_product,r_price,select.name)
        product = request.data.get('product')
        price = request.data.get('price')
        try:
            PurchaseCreation(product,price,select.name)
        except Exception as e:
            return Response(str(e))


catalog = Catalog()
