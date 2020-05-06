from django.urls import path,include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',Login.as_view()),
    path('logout',Logout.as_view()),
    path('admin',AdminDashboard.as_view()),
    path('create',Create.as_view()),
    path('catalog',Catalog.as_view()),
    path('paygate',Pay.as_view()),
    path('charge',Charge.as_view()),
    path('friend_search',FrdSearchApi.as_view()),
    path('results',Result.as_view()),
    path('gift',SendGift.as_view()),
    path('topup',Topup.as_view()),
    path('topuppay',TopupPay.as_view()),
    path('topupcharge',TopupCharge.as_view()),
    path('payment_method',PayMethod.as_view()),
    path('billing',Billing.as_view()),
    path('coupon',Voucher.as_view()),
    path('add_customer',AddCustomer.as_view()),
    path('add_product',AddProduct.as_view()),
    path('product_view',ProductView.as_view()),
    path('customer_view',CustomerView.as_view()),
    path('select_customer',SelectCustomer.as_view()),
    

]
