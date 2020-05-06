from rest_framework import serializers
from .models import *



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ('area', 'pin', 'phone_number', 'state', 'remarks')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_name','email','contact_number','address')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
