from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    storage_location = models.CharField(max_length=50)
    image_url = models.URLField(default="https://via.placeholder.com/200")

    def __str__(self):
        return self.name


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('Normal', 'Normal'),
        ('Fast', 'Fast')
    ]

    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Picking', 'Picking'),
        ('Packed', 'Packed'),
        ('Dispatched', 'Dispatched'),
        ('Delayed', 'Delayed')
    ]

    customer_name = models.CharField(max_length=100)
    customer_location = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    warehouse = models.ForeignKey('Warehouse',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
class Cart(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

def __str__(self):
    return f"{self.customer_name} - {self.product.name}"
    
    
class Seller(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

def __str__(self):
        return self.username


class DeliveryPartner(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    current_status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.username
    

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    max_capacity = models.IntegerField()
    current_load = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name