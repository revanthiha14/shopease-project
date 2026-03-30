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

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"