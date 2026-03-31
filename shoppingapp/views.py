from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Order


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