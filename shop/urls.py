from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from . import models

router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'order', views.OrderViewSet)
# router.register(r'register', views.RegisterUser.as_view())
# router.register(r'login', views.LoginUser.as_view())




urlpatterns = [
    path('', include(router.urls)),
    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    path('vendor-dashboard-products', views.VendorAddedProduct.as_view()),
    path('vendor-products', views.VendorAddedProductQuery.as_view()),
    path('vendor-ordered-products', views.LoogedInVendorOrderedProducts.as_view())


]



# urlpatterns = [
#     path ('vendor', views.ListVendor.as_view(), name='vendor'),
#     path ('vendor/<int:pk>/', views.DetailVendor.as_view(),name='singlevendor'),
#     path ('categories', views.ListCategory.as_view(), name='categorie'),
#     path ('categories/<int:pk>/', views.DetailCategory.as_view(),name='singlecategory'),
#     path ('customers', views.ListCustomer.as_view(), name='customers'),
#     path ('customers/<int:pk>/', views.DetailCustomer.as_view(),name='singlecustomer'),
#     path ('products', views.ListProduct.as_view(), name='products'),
#     path ('products/<int:pk>/', views.DetailProduct.as_view(),name='singleproduct'),  
#     path ('orders', views.ListOrder.as_view(), name='orders'),
#     path ('orders/<int:pk>/', views.DetailOrder.as_view(),name='singleorder'),     
# ]
