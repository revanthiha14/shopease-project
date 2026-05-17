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
    path('seller/dashboard/', views.seller_dashboard),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),
    path('remove-cart/<int:cart_id>/',views.remove_cart_item,name='remove_cart'),
    path('increase-cart/<int:cart_id>/',views.increase_cart_quantity),
    path('decrease-cart/<int:cart_id>/',views.decrease_cart_quantity),
    path('orders/',views.order_history,name='orders'),
    path('delivery/dashboard/',views.delivery_dashboard,name='delivery_dashboard'),
    path('cancel-order/<int:order_id>/',views.cancel_order,name='cancel_order'),
    path('return-order/<int:order_id>/',views.return_order,name='return_order'),
    path('payment/',views.payment_page,name='payment'),
]