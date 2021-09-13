from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, serializers
from .serializers import *
from .models import *
from rest_framework import viewsets

 # Create your views here.
# def index(request):
#     return HttpResponse("Welcome to online shop.")


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserExtended.objects.all()
    serializer_class = UserTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserExtended.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer





