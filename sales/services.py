from .models import *
from . import views
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


    
def Remove(product,price,purchaser):
    
    Purchase.objects.filter(purchaser=purchaser,product=product,price=price).delete()
    
def AddingCustomer(customer_name,address,email,contact_number):
    
    add = Customer.objects.create(customer_name=customer_name,
                                  address=address,email=email,contact_number=contact_number)

def AddingProduct(product_name,product_category,brand,product_size,
                            product_price,discount,product_tax,product_img,expiry_date,stock):
    add = Product.objects.create(product_name=product_name,product_category=product_category,
                                brand=brand,product_size=product_size,                          product_price=product_price,discount=discount,product_tax=product_tax,product_img=product_img,expiry_date=expiry_date,stock=stock)

def PurchaseCreation(product,price,purchaser):
    k = Purchase.objects.create(
                        product=product,
                        price=price,
                        purchaser=purchaser)

def Clearance():
    pro = Purchase.objects.filter(purchaser=views.select.name)        
    for i in pro:
        quan = Product.objects.get(product_name=i.product)
        Product.objects.filter(product_n=i.product).update(stock=int(quan.stock)-1)
    Purchase.objects.filter(purchaser=views.select.name).delete()

bill = ""
def BillingCreation(name,email,area,pin,phone_number,state,remarks):
    global bill
    bill = Billing.objects.create(name=name,email=email,area=area,pin=pin,phone_number=phone_number,state=state,remarks=remarks)
    print(bill.state)


def successful_order():
    print(bill.name)
    purchase = Purchase.objects.filter(purchaser=views.obj.n)
    for i in purchase:
        orders = Placed_Orders.objects.create(address=bill,product_n=i.product,price=i.price)
