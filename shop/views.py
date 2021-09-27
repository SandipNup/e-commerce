import re
from django.db.models.query import QuerySet
from django.db.models.signals import pre_delete
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, serializers
from rest_framework import response
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .serializers import ProductSerializer
import pandas as pd
from django.db.models import Prefetch
import json


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

        print(Products.objects.select_related('category'))

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


class VendorAddedProductQuery(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsVendor]

    def get(self, request):
        user = request.user
        vendor_user_type = UserType.objects.get(user_type = 'Vendor')

        if user.user_type.id == vendor_user_type.id:
            # print(Category.objects.prefetch_related(''))
            response_query = Category.objects.prefetch_related(Prefetch('products_set', queryset=Products.objects.filter(created_by__id=user.id))).all()

            category = Category.objects.all()  # 3
           
            response_arr = []

            for category in response_query:
                product = category.products_set.all()  # data base operation is not performed
                response = ProductSerializer(product, many=True)
                json_response = json.dumps(response.data)

                response_arr.append({
                    category.name: json_response
                })
            print(response_arr)    
                                  
            return Response(response_arr)

        else:
            raise Exception("User is not Vendor")


class LoogedInVendorOrderedProducts(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsVendor]

    def get(self, request):
        user = request.user
        vendor_user_type = UserType.objects.get(user_type = 'Vendor')

        
        if user.user_type.id == vendor_user_type.id:
            # print(Category.objects.prefetch_related(''))

            # get all the ordered products id of a vendor
            vendor_product_orders = Order.objects.filter(product__created_by__id=user.id).values_list("product__id").all()

            if vendor_product_orders:
                product_id = []
                for each_product in vendor_product_orders:
                    product_id.append(each_product[0])

                # queryset filter by products id
                print(product_id)
                response_query = Category.objects.prefetch_related(Prefetch('products_set', queryset=Products.objects.filter(id__in = product_id))).all()

                category = Category.objects.all()  # 3
            
                response_arr = []

                for category in response_query:
                    product = category.products_set.all()  # data base operation is not performed
                    response = ProductSerializer(product, many=True)
                    json_response = json.dumps(response.data)

                    response_arr.append({
                        category.name: json_response
                    })
                print(response_arr)    
                                    
                return Response(response_arr)
            else:
                return Response("Vendor does not have ordered products")

        else:
            raise Exception("User is not Vendor")






