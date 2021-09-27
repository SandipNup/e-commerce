from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin


class UserType(models.Model):
    user_type = models.CharField(max_length=100)  # vendor - customer

    def register(self):
        self.save()
    def __str__(self):
        return self.user_type

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given email must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(_('active'), default=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def __str__(self):
        return '{}'.format(self.username)

    def register(self):
        self.save()


# all products added by particular vendor group by category

# {
#     "jacket": [
#         {
#             "jacked1"
#         },
#         {
#             "jacked2"
#         },
#     ],
#     "pant" : [
#         {
#             "pant1"
#         },
#         {
#             "pant2"
#         },
#     ],
# }



# # all products sold from particular vendor
# {
#     "jacket": [
#         {
#             "jacked1"
#         },
#         {
#             "jacked2"
#         },
#     ],
#     "pant" : [
#         {
#             "pant1"
#         },
#         {
#             "pant2"
#         },
#     ],
# }

# # total product sold and total amount
# {
#     "jacket": [
#         {
#             "jacked1",
#             "quantity": 2,
#             "price": 100
#         },
#         {
#             "jacked2"
#         },
#     ],
#     "pant" : [
#         {
#             "pant1"
#         },
#         {
#             "pant2"
#         },
#     ],
# }

# 1 - M
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
  
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


# Products.object.select_related('category')

# response = {
#     "name" : "sandip",
#     "price" : 10,
#     "category" : {
#         "name": "",
#         "created_by": ""
#     },
#     "created_by" : "vendor_id",
#     "description"  : "sandip",
#     "imageUrl" : "sandip"
# }


# Products.objects.all()

# response = {
#     "name" : "sandip",
#     "price" : 10,
#     "category" : 1,
#     "created_by" : "vendor_id",
#     "description"  : "sandip",
#     "imageUrl" : "sandip"
# }

# 1. Reverse foregin Key


# 2. ManyToManyField


# Products.objects.prefetch_related('category')
# {"name" : "sandip",
#     "price" : 10,
#     "category" : [
#         {
#         "name": "",
#         "created_by": ""
#         },
#         {
#         "name": "",
#         "created_by": ""
#         }
#     ],
#     "created_by" : "vendor_id",
#     "description"  : "sandip",
#     "imageUrl" : "sandip"
# }
# 1        ->  M
# Category, Products

# Category.objects.prefetch_related('products_set')

# Products.object.filter(category__name = 'jeans')


#[
#     {
#         "jeans": [
#             {
#                 "id": 1,
#                 "name": "LBD jeans",
#                 "price": 500,
#                 "category_id": 1,
#                 "created_by_id": 18,
#                 "description": "good jeans",
#                 "imageUrl": null
#             },
#             {
#                 "id": 2,
#                 "name": "American Eagle",
#                 "price": 1000,
#                 "category_id": 1,
#                 "created_by_id": 18,
#                 "description": "shhshsh",
#                 "imageUrl": null
#             }
#         ]
#     },
#     {
#         "jackets": [
#             {
#                 "id": 3,
#                 "name": "jacket1",
#                 "price": 500,
#                 "category_id": 2,
#                 "created_by_id": 18,
#                 "description": null,
#                 "imageUrl": null
#             },
#             {
#                 "id": 4,
#                 "name": "jacket2",
#                 "price": 10000,
#                 "category_id": 2,
#                 "created_by_id": 18,
#                 "description": null,
#                 "imageUrl": null
#             }
#         ]
#     }
# ]

# fetch pk of all category of a product

# fetch category pk


class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
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
    customer = models.ForeignKey(User,
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

    
    def save(self):
        final_amount = self.product.price * self.quantity
        self.price = final_amount
        super().save()



# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

