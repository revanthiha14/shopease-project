from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('login/', views.customer_login, name='customer_login'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
]