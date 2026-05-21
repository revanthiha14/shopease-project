from django.contrib import admin
from .models import Product, Order, Warehouse, DeliveryPartner, Seller, Review, Address, Worker


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'product',
        'quantity',
        'order_status',
        'delivery_type',
        'warehouse',
        'delivery_partner',
        'reward_points'
    )


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Warehouse)
admin.site.register(DeliveryPartner)
admin.site.register(Seller)
admin.site.register(Review)
admin.site.register(Address)
admin.site.register(Worker)