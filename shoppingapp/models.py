from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    storage_location = models.CharField(max_length=50)
    image_url = models.URLField(default="https://via.placeholder.com/200")
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, null=True, blank=True)
    
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
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled'),
        ('Return Requested', 'Return Requested'),
        ('Delivered', 'Delivered')
    ]

    customer_name = models.CharField(max_length=100)

    customer_location = models.CharField(max_length=100)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    order_time = models.DateTimeField(auto_now_add=True)

    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES
    )

    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    delivery_partner = models.ForeignKey(
        'DeliveryPartner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    reward_points = models.IntegerField(default=0)
    
    estimated_delivery = models.CharField(
        max_length=100,
        default="3 Days"
    )
    
    payment_method = models.CharField(
        max_length=50,
        default="COD"
    )
    
    package_id = models.CharField(
        max_length=100,
        default="PKG000"
    )

    packing_counter = models.CharField(
        max_length=100,
        default="Counter 1"
    )
    
    priority = models.CharField(
        max_length=50,
        default="Low"
    )
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    

    
class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(
        max_length=100
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.customer_name} - "
            f"{self.product.name}"
        )
        

    
class Cart(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
    
    
class Seller(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100, default="My Shop")
    email = models.EmailField(default="seller@gmail.com")
    phone = models.CharField(max_length=15, default="0000000000")

    def __str__(self):
        return self.shop_name


class DeliveryPartner(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    current_status = models.CharField(max_length=50, default="Available")
    is_available = models.BooleanField(default=True)
    assigned_orders = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    max_capacity = models.IntegerField()
    current_load = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Customer(models.Model):

    username = models.CharField(
        max_length=100,
        unique=True
    )

    email = models.EmailField()

    password = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.username
    

class Address(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    address_line = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    is_default = models.BooleanField(
        default=True
    )

    def __str__(self):

        return (
            f"{self.full_name} - "
            f"{self.city}"
        )