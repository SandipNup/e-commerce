from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class UserType(models.Model):
    user_type = models.CharField(max_length=100)  # vendor - customer

    def register(self):
        self.save()
    def __str__(self):
        return self.user_type

class UserExtended(User):
    phone = models.CharField(max_length=10)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def register(self):
        self.save()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(UserExtended, on_delete=models.CASCADE, default=1)
  
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name

# class Customer(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=10)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return '{} {}'.format(self.first_name, self.last_name)
  
#     # to save the data
#     def register(self):
#         self.save()
  

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    created_by = models.ForeignKey(UserExtended,
                                 on_delete=models.CASCADE, default=1)
    description = models.CharField(
    max_length=250, default='', blank=True, null=True)
    imageUrl = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    # def save(self):
    #     self.save()
  

class Order(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(UserExtended,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
  
    def placeOrder(self):
        self.save()

    def __str__(self):
        return '{} {}'.format(self.quantity, self.product)



# @receiver(post_save, sender=UserExtended)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

