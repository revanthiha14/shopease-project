from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('login/', views.customer_login, name='customer_login'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('seller-login/', views.seller_login),
    path('delivery-login/', views.delivery_login),
    path('seller-add-product/', views.seller_add_product),
    path('update-status/<int:order_id>/',views.update_delivery_status,name='update_status'),
    path('return-order/<int:order_id>/',views.return_order,name='return_order'),
]