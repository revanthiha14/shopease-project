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

    if product.stock > 0:
        product.stock -= 1
        product.save()

        Order.objects.create(
            customer_name=request.session.get('customer_name', 'Guest'),
            customer_location=request.session.get('location', 'Unknown'),
            product=product,
            quantity=1,
            delivery_type="Fast",
            order_status="Placed"
        )

        return HttpResponse(f"""
            <h2>Order placed successfully ✅</h2>
            <p>Customer: {request.session.get('customer_name', 'Guest')}</p>
            <p>Delivery Address: {request.session.get('location', 'Unknown')}</p>
            <p>Product: {product.name}</p>
            <p>Remaining stock: {product.stock}</p>
            <a href="/">Go back to Shop</a>
        """)

    else:
        return HttpResponse("""
            <h2>Out of Stock ❌</h2>
            <a href="/">Go back to Shop</a>
        """)
        

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