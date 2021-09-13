from django.db.models import fields
from rest_framework import serializers
from .models import *


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        fields = {
            'id'
            'first_name'
            'last_name'
            'phone'
            'email'
            'password'
        }
        model = Vendor
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = {
            'id'
            'name'
            'created_by'
        }
        model = Category
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = {
            'id'
            'first_name'
            'last_name'
            'phone'
            'email'
            'password'
        }
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = {
            'id'
            'name'
            'price'
            'category'
            'created_by'
            'description'
            'image'
        }
        model = Products
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        fields = {
            'id'
            'product'
            'customer'
            'quantity'
            'price'
            'address'
            'phone'
            'date'
            'status'
        }
        model = Order
        fields = '__all__'


