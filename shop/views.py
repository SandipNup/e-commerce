from django.db.models.signals import pre_delete
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, serializers
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .serializers import ProductSerializer
import pandas as pd


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

        user_type_instance = UserType.objects.get(id=user_type)

        user = User(
            username = username,
            password=password,
            user_type=user_type_instance
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

        user = User.objects.get(username= username, password= password)

        if user:
            token = Token.objects.get(user=user)

            if token:
                pass
            else:
                token = Token.objects.create(user=user)

            return Response({
                "username": user.username,
                "token": token.key
            })
        else:
            return Response({
                "message": "User does not exist"
            })


class VendorAddedProduct(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsVendor]

    def get(self, request):
        user = request.user
        vendor_user_type = UserType.objects.get(user_type = 'Vendor')

        if user.user_type.id == vendor_user_type.id:
            vendor_added_products_list = list(Products.objects.filter(created_by=user).values())
            # serializer = ProductSerializer(vendor_added_products, many=True)
            categories = list(Category.objects.values())
            category_dict = {}
            for category in categories:
                category_dict[category["id"]] = category["name"]
            
            final_json = []

            for product in vendor_added_products_list:
                product["category"] = category_dict[product["category_id"]]

            df = pd.DataFrame(vendor_added_products_list).set_index("category")

            unique_idex = list(df.index.unique())
            print(unique_idex)

            for each_index in unique_idex:
                filtered_df = df.loc[each_index]
                prodcut_list = []
                for index, row in filtered_df.iterrows():
                    _dict = row.to_dict()
                    prodcut_list.append(_dict)
                
                final_json.append({
                    each_index : prodcut_list
                })
                    
            return Response(final_json)

        else:
            raise Exception("User is not Vendor")






