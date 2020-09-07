from django.db import models
from loginApp.models import *
from adminApp.models import *


class ShippingInfo(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.PositiveIntegerField()

    user = models.ForeignKey(
        User, related_name='shippingInfo', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BillingInfo(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentInfo(models.Model):
    card_number = models.PositiveIntegerField()
    expiration_date = models.CharField(max_length=7)
    security_number = models.IntegerField()

    user = models.ForeignKey(
        User, related_name='paymentInfo', on_delete=models.CASCADE)
    billingInfo = models.OneToOneField(
        BillingInfo, related_name='paymentInfo', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # one to many relationship with product


class WishList(models.Model):
    user = models.OneToOneField(
        User, related_name='wishList', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # one to many relationship with product


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, related_name='shoppingCart', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # one to many relationship with product


class Category(models.Model):
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # one to many relationship with product


class Product(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    # price = models.DecimalField(max_digits = 5, decimal_places = 2)
    price = models.PositiveIntegerField()
    image = models.CharField(max_length=200)

    order = models.ForeignKey(
        Order, related_name='products', on_delete=models.CASCADE, null=True)
    wishList = models.ForeignKey(
        WishList, related_name='products', on_delete=models.CASCADE, null=True)
    shoppingCart = models.ForeignKey(
        ShoppingCart, related_name='products', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
