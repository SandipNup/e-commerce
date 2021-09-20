from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, serializers
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response

 # Create your views here.
# def index(request):
#     return HttpResponse("Welcome to online shop.")


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserTypeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
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


class RegisterUser(APIView):
    def post(self,request):
        # data = {'password': 'test_user123', 'username': 'test_user', 'user_type': 1, 'phone': '9844892222'}
        # take user required field from request
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        user_type = request.data.get("user_type", None)
        phone = request.data.get("phone", None)

        user_type_instance = UserType.objects.get(id=user_type)

        user = User(
            username = username,
            password=password,
            user_type=user_type_instance,
            phone=phone
        )
        user.save()
        
        response = {
            "username": user.username,
            "message": "User was successfully register"
        }

        return Response(response)



class LoginUser(APIView):

    def get(self,request):
        username = request.data["username"]
        password = request.data["password"]

        user = UserExtended.object.filter(username= username, password= password)

        if user:
            token = Token.objects.get(user=user)
            if token:
                pass
            else:
                token = Token.objects.create(user=user)


            return {
                "username": user.username,
                "token": token.key
            }
        else:
            return {
                "message": "User does not exist"
            }





