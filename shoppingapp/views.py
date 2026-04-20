from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Order, Cart


def customer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        location = request.POST.get("location")

        request.session['customer_name'] = username
        request.session['location'] = location

        return redirect('/')

    return render(request, 'shoppingapp/login.html')


def product_list(request):
    products = Product.objects.all()
    customer_name = request.session.get('customer_name', 'Guest')

    return render(
        request,
        'shoppingapp/products.html',
        {
            'products': products,
            'customer_name': customer_name
        }
    )


def buy_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    customer_name = request.session.get('customer_name', 'Guest')
    location = request.session.get('location', 'Unknown')

    quantity = 1

    warehouse = Warehouse.objects.filter(
        is_active=True,
        current_load__lt=models.F('max_capacity')
    ).order_by('current_load').first()

    if warehouse is None:
        return HttpResponse("No warehouse available / delayed")

    partner = assign_delivery_partner()

    if partner is None:
        return HttpResponse("No delivery partner available")

    if product.stock >= quantity:
        product.stock -= quantity
        product.save()

        warehouse.current_load += 1
        warehouse.save()

        reward_points = int(product.price // 10)

        Order.objects.create(
            customer_name=customer_name,
            customer_location=location,
            product=product,
            quantity=quantity,
            delivery_type="Fast",
            order_status="Picking",
            reward_points=reward_points,
            warehouse=warehouse
        )

        return HttpResponse(f"""
            Order placed successfully <br>
            Warehouse: {warehouse.name} <br>
            Delivery Partner: {partner.username} <br>
            Reward Points: {reward_points}
        """)

    return HttpResponse("Out of Stock")      

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    customer_name = request.session.get('customer_name', 'Guest')

    cart_item, created = Cart.objects.get_or_create(
        customer_name=customer_name,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/')


def view_cart(request):
    customer_name = request.session.get('customer_name', 'Guest')
    cart_items = Cart.objects.filter(customer_name=customer_name)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(
        request,
        'shoppingapp/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )
    

def seller_login(request):
    if request.method == "POST":
        seller_name = request.POST.get("username")
        request.session['seller_name'] = seller_name
        return HttpResponse("Seller logged in successfully")

    return HttpResponse("Seller Login Page")


def delivery_login(request):
    if request.method == "POST":
        delivery_name = request.POST.get("username")
        request.session['delivery_name'] = delivery_name
        return HttpResponse("Delivery partner logged in")

    return HttpResponse("Delivery Login Page")

def seller_add_product(request):
    seller_name = request.session.get('seller_name', 'Unknown Seller')

    Product.objects.create(
        name="New Seller Product",
        category="Seller Item",
        price=999,
        stock=10,
        storage_location="Warehouse A",
        image_url="https://via.placeholder.com/200"
    )

    return HttpResponse(f"Product added by seller {seller_name}")


def assign_delivery_partner():
    partner = DeliveryPartner.objects.filter(
        is_available=True
    ).order_by('assigned_orders').first()

    if partner:
        partner.assigned_orders += 1
        partner.save()
        return partner

    return None


def update_delivery_status(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.order_status == "Picking":
        order.order_status = "Packed"

    elif order.order_status == "Packed":
        order.order_status = "Dispatched"

    elif order.order_status == "Dispatched":
        order.order_status = "Delivered"

    order.save()

    return HttpResponse(
        f"Updated Status: {order.order_status}"
    )
    
    
def return_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.order_status == "Delivered":
        order.order_status = "Return Requested"

        product = order.product
        product.stock += order.quantity
        product.save()

        order.reward_points = 0
        order.save()

        return HttpResponse(
            "Return approved. Refund initiated."
        )

    return HttpResponse(
        "Return not allowed before delivery"
    )