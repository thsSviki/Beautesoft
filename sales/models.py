from django.db import models

class Admin(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact_number = models.CharField(max_length=10)
    topup = models.IntegerField(default=0)



class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    product_size = models.IntegerField()
    product_price = models.IntegerField()
    product_tax = models.FloatField()
    discount = models.FloatField()
    product_img = models.ImageField(upload_to='img/')
    expiry_date = models.CharField(max_length=100)
    stock = models.IntegerField()

class Purchase(models.Model):
    product = models.CharField(max_length=255)
    price = models.FloatField()
    purchaser = models.CharField(max_length=100)

class Friends(models.Model):
    sender_email = models.EmailField(max_length=100)
    receiver_email = models.EmailField(max_length=100)

class Billing(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    area = models.CharField(max_length=100)
    pin = models.BigIntegerField()
    phone_number = models.BigIntegerField()
    state = models.CharField(max_length=100)
    remarks = models.CharField(max_length=500)

class Placed_Orders(models.Model):
    address = models.ForeignKey(Billing, on_delete=models.CASCADE)
    product_n = models.CharField(max_length=255)
    price = models.FloatField()
    


