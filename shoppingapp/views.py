from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from .models import Product, Order, Cart, Warehouse, DeliveryPartner, Seller, Review

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

    search = request.GET.get('search')

    category = request.GET.get('category')

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category=category)

    categories = Product.objects.values_list(
        'category',
        flat=True
    ).distinct()

    customer_name = request.session.get(
        'customer_name',
        'Guest'
    )

    return render(
        request,
        'shoppingapp/product_list.html',
        {
            'products': products,
            'customer_name': customer_name,
            'categories': categories
        }
    )



def buy_product(request, product_id):

    product = Product.objects.get(product_id=product_id)

    quantity = 1

    # OUT OF STOCK CHECK
    if product.stock < quantity:
        return HttpResponse("Product out of stock")

    # FIND AVAILABLE WAREHOUSE
    warehouse = Warehouse.objects.filter(
        current_load__lt=models.F('max_capacity'),
        is_active=True
    ).first()

    if not warehouse:
        return HttpResponse("No warehouse available / delayed")

    # INCREASE WAREHOUSE LOAD
    warehouse.current_load += 1
    warehouse.save()

    # FIND DELIVERY PARTNER
    partner = DeliveryPartner.objects.filter(
    is_available=True
    ).first()
    
    if not partner:
        return HttpResponse("No delivery partner available")

    # REDUCE PRODUCT STOCK
    product.stock -= quantity
    product.save()

    # REWARD POINTS
    reward_points = int(product.price / 10)

    # CREATE ORDER
    order = Order.objects.create(
        customer_name="Rev",
        customer_location="Chennai",
        product=product,
        quantity=quantity,
        delivery_type="Fast",
        order_status="Placed",
        warehouse=warehouse,
        delivery_partner=partner,
        reward_points=reward_points
    )

    return HttpResponse(
        f"""
        Order placed successfully <br>
        Warehouse: {warehouse.name} <br>
        Delivery Partner: {partner.username} <br>
        Reward Points: {reward_points} <br>
        Remaining Stock: {product.stock}
        """
    )


def add_to_cart(request, product_id):

    customer_name = request.session.get(
        'customer_name',
        'Guest'
    )

    product = Product.objects.get(
        product_id=product_id
    )

    cart_item = Cart.objects.filter(
        customer_name=customer_name,
        product=product
    ).first()

    if cart_item:

        cart_item.quantity += 1
        cart_item.save()

    else:

        Cart.objects.create(
            customer_name=customer_name,
            product=product,
            quantity=1
        )

    return redirect('/cart/')


def view_cart(request):

    customer_name = request.session.get(
        'customer_name',
        'Guest'
    )

    cart_items = Cart.objects.filter(
        customer_name=customer_name
    )

    total = 0

    for item in cart_items:

        item.subtotal = item.product.price * item.quantity
        
        total += item.subtotal

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

        return redirect('/seller/dashboard/')

    return render(
        request,
        'shoppingapp/seller_login.html'
    )

def delivery_login(request):

    partner = DeliveryPartner.objects.first()

    request.session['delivery_partner'] = (
        partner.username
    )

    return redirect('/delivery/dashboard/')

def seller_add_product(request):

    seller_name = request.session.get('seller_name')

    if not seller_name:
        return HttpResponse("Seller not logged in")

    seller = Seller.objects.filter(
        username__iexact=seller_name
    ).first()

    if not seller:
        return HttpResponse("Seller does not exist")

    if request.method == "POST":

        Product.objects.create(

            name=request.POST.get('name'),

            category=request.POST.get('category'),

            price=request.POST.get('price'),

            stock=request.POST.get('stock'),

            image_url=request.POST.get('image_url'),

            seller=seller
        )

        return redirect('/seller/dashboard/')

    return render(
        request,
        'shoppingapp/seller_add_product.html'
    )

def seller_dashboard(request):

    seller_name = request.session.get('seller_name')

    print("SESSION SELLER:", seller_name)

    all_sellers = Seller.objects.all()

    for s in all_sellers:
        print("DB SELLER:", s.username)

    if not seller_name:
        return HttpResponse("Seller not logged in")

    seller = Seller.objects.filter(
        username__iexact=seller_name
    ).first()

    if not seller:
        return HttpResponse("Seller does not exist")

    products = Product.objects.filter(seller=seller)

    return render(
        request,
        'shoppingapp/seller_dashboard.html',
        {
            'seller': seller,
            'products': products
        }
    )


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

def product_detail(request, product_id):

    product = Product.objects.get(
        product_id=product_id
    )

    reviews = Review.objects.filter(
        product=product
    ).order_by('-created_at')

    if request.method == "POST":

        Review.objects.create(

            product=product,

            customer_name=request.session.get(
                'customer_name',
                'Guest'
            ),

            rating=request.POST.get('rating'),

            comment=request.POST.get('comment')
        )

        return redirect(
            f'/product/{product_id}/'
        )

    return render(
        request,
        'shoppingapp/product_detail.html',
        {
            'product': product,
            'reviews': reviews
        }
    )

    
def remove_cart_item(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.delete()

    return redirect('/cart/')


def increase_cart_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.quantity += 1

    cart_item.save()

    return redirect('/cart/')


def decrease_cart_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect('/cart/')


def order_history(request):

    customer_name = request.session.get(
        'customer_name',
        'Guest'
    )

    orders = Order.objects.filter(
        customer_name=customer_name
    ).order_by('-order_time')

    return render(
        request,
        'shoppingapp/order_history.html',
        {
            'orders': orders
        }
    )
    

def delivery_dashboard(request):

    partner_name = request.session.get(
        'delivery_partner'
    )

    if not partner_name:
        return HttpResponse(
            "Delivery partner not logged in"
        )

    partner = DeliveryPartner.objects.filter(
        username__iexact=partner_name
    ).first()

    if not partner:
        return HttpResponse(
            "Delivery partner does not exist"
        )

    orders = Order.objects.filter(
        delivery_partner=partner
    )

    return render(
        request,
        'shoppingapp/delivery_dashboard.html',
        {
            'partner': partner,
            'orders': orders
        }
    )
    

def cancel_order(request, order_id):

    order = Order.objects.get(id=order_id)

    if order.order_status == "Placed":

        product = order.product

        product.stock += order.quantity

        product.save()

        order.order_status = "Cancelled"

        order.save()

        return redirect('/orders/')

    return HttpResponse(
        "Order cannot be cancelled now"
    )


def return_order(request, order_id):

    order = Order.objects.get(id=order_id)

    if order.order_status == "Delivered":

        product = order.product

        product.stock += order.quantity

        product.save()

        order.order_status = "Return Requested"

        order.reward_points = 0

        order.save()

        return redirect('/orders/')

    return HttpResponse(
        "Return allowed only after delivery"
    )
    
    
def payment_page(request):

    customer_name = request.session.get(
        'customer_name',
        'Guest'
    )

    cart_items = Cart.objects.filter(
        customer_name=customer_name
    )

    total = 0

    for item in cart_items:

        total += (
            item.product.price * item.quantity
        )

    if request.method == "POST":

        for item in cart_items:

            product = item.product

            if product.stock >= item.quantity:

                product.stock -= item.quantity

                product.save()

                warehouse = Warehouse.objects.filter(
                    current_load__lt=models.F(
                        'max_capacity'
                    ),
                    is_active=True
                ).first()

                partner = DeliveryPartner.objects.filter(
                    is_available=True
                ).first()

                reward_points = int(
                    product.price / 10
                )

                Order.objects.create(

                    customer_name=customer_name,

                    customer_location="Chennai",

                    product=product,

                    quantity=item.quantity,

                    delivery_type="Fast",

                    order_status="Placed",

                    warehouse=warehouse,

                    delivery_partner=partner,

                    reward_points=reward_points
                )

        cart_items.delete()

        return render(
            request,
            'shoppingapp/payment_success.html'
        )

    return render(
        request,
        'shoppingapp/payment.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )