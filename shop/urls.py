from django.urls import path
from django.contrib import admin
from . import views 
from . import models







urlpatterns = [
    path ('vendor', views.ListVendor.as_view(), name='vendor'),
    path ('vendor/<int:pk>/', views.DetailVendor.as_view(),name='singlevendor'),
    path ('categories', views.ListCategory.as_view(), name='categorie'),
    path ('categories/<int:pk>/', views.DetailCategory.as_view(),name='singlecategory'),
    path ('customers', views.ListCustomer.as_view(), name='customers'),
    path ('customers/<int:pk>/', views.DetailCustomer.as_view(),name='singlecustomer'),
    path ('products', views.ListProduct.as_view(), name='products'),
    path ('products/<int:pk>/', views.DetailProduct.as_view(),name='singleproduct'),  
    path ('orders', views.ListOrder.as_view(), name='orders'),
    path ('orders/<int:pk>/', views.DetailOrder.as_view(),name='singleorder'),     
]
