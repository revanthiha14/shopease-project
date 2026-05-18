from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import timedelta
from django.utils import timezone


# ==========================================
# HOME PAGE / PRODUCT LIST
# ==========================================

def product_list(request):

    products = Product.objects.all()

    customer_name = request.session.get(
        'customer_name',
        'Guest'
    )

    return render(
        request,
        'shoppingapp/product_list.html',
        {
            'products': products,
            'customer_name': customer_name
        }
    )


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        customer = Customer.objects.filter(
            username=username,
            password=password
        ).first()

        if customer:

            request.session[
                'customer_name'
            ] = customer.username

            request.session[
                'customer_id'
            ] = customer.id

            return redirect('/')

        return HttpResponse(
            "Invalid username or password"
        )

    return render(
        request,
        'shoppingapp/login.html'
    )


# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    request.session.flush()

    return redirect('/login/')


# ==========================================
# REGISTER
# ==========================================

def register_view(request):

    if request.method == "POST":

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        if Customer.objects.filter(
            username=username
        ).exists():

            return HttpResponse(
                "Username already exists"
            )

        Customer.objects.create(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(
        request,
        'shoppingapp/register.html'
    )


# ==========================================
# ADD TO CART
# ==========================================

def add_to_cart(request, product_id):

    if not request.session.get(
        'customer_name'
    ):

        return redirect('/login/')

    product = Product.objects.get(
        product_id=product_id
    )

    customer_name = request.session.get(
        'customer_name'
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


# ==========================================
# VIEW CART
# ==========================================

def view_cart(request):

    if not request.session.get(
        'customer_name'
    ):

        return redirect('/login/')

    customer_name = request.session.get(
        'customer_name'
    )

    cart_items = Cart.objects.filter(
        customer_name=customer_name
    )

    total = 0

    for item in cart_items:

        total += (
            item.product.price * item.quantity
        )

    return render(
        request,
        'shoppingapp/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


# ==========================================
# INCREASE QUANTITY
# ==========================================

def increase_quantity(request, cart_id):

    cart_item = Cart.objects.get(
        id=cart_id
    )

    cart_item.quantity += 1

    cart_item.save()

    return redirect('/cart/')


# ==========================================
# DECREASE QUANTITY
# ==========================================

def decrease_quantity(request, cart_id):

    cart_item = Cart.objects.get(
        id=cart_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect('/cart/')


# ==========================================
# CHECKOUT ADDRESS
# ==========================================

def checkout_address(request):

    if not request.session.get(
        'customer_name'
    ):

        return redirect('/login/')

    customer = Customer.objects.filter(
        id=request.session.get(
            'customer_id'
        )
    ).first()

    if not customer:

        return redirect('/login/')

    if request.method == "POST":

        Address.objects.create(

            customer=customer,

            full_name=request.POST.get(
                'full_name'
            ),

            phone=request.POST.get(
                'phone'
            ),

            address_line=request.POST.get(
                'address_line'
            ),

            city=request.POST.get(
                'city'
            ),

            state=request.POST.get(
                'state'
            ),

            pincode=request.POST.get(
                'pincode'
            )
        )

        request.session['delivery_type'] = (
            request.POST.get(
                'delivery_type'
            )
        )

        return redirect('/payment/')

    return render(
        request,
        'shoppingapp/checkout_address.html'
    )


# ==========================================
# ASSIGN WAREHOUSE
# ==========================================

def assign_warehouse(city):

    city = city.lower().strip()

    # SOUTH TAMIL NADU

    south_tn = [

        'madurai',

        'tirunelveli',

        'thoothukudi',

        'kanyakumari',

        'nagercoil',

        'virudhunagar',

        'ramanathapuram'
    ]

    # WEST TAMIL NADU

    west_tn = [

        'coimbatore',

        'tiruppur',

        'erode',

        'salem',

        'namakkal'
    ]

    # CHENNAI REGION

    chennai_region = [

        'chennai',

        'vellore',

        'trichy',

        'cuddalore',

        'kanchipuram',

        'thanjavur'
    ]

    # KARNATAKA

    karnataka = [

        'bangalore',

        'mysore',

        'mangalore',

        'hubli'
    ]

    # TELANGANA / ANDHRA

    hyderabad_region = [

        'hyderabad',

        'warangal',

        'vijayawada',

        'vizag'
    ]

    # NORTH INDIA

    north_india = [

        'delhi',

        'kashmir',

        'jaipur',

        'lucknow',

        'chandigarh'
    ]

    if city in south_tn:

        return Warehouse.objects.filter(
            name='Madurai Hub'
        ).first()

    elif city in west_tn:

        return Warehouse.objects.filter(
            name='Coimbatore Hub'
        ).first()

    elif city in chennai_region:

        return Warehouse.objects.filter(
            name='Chennai Hub'
        ).first()

    elif city in karnataka:

        return Warehouse.objects.filter(
            name='Bangalore Hub'
        ).first()

    elif city in hyderabad_region:

        return Warehouse.objects.filter(
            name='Hyderabad Hub'
        ).first()

    elif city in north_india:

        return Warehouse.objects.filter(
            name='Delhi Hub'
        ).first()

    return Warehouse.objects.first()


# ==========================================
# ASSIGN DELIVERY PARTNER
# ==========================================

def assign_delivery_partner():

    partner = DeliveryPartner.objects.filter(
        is_available=True
    ).order_by(
        'assigned_orders'
    ).first()

    if partner:

        partner.assigned_orders += 1

        partner.save()

        return partner

    return None


# ==========================================
# PAYMENT PAGE
# ==========================================

def payment_page(request):

    if not request.session.get(
        'customer_name'
    ):

        return redirect('/login/')

    customer_name = request.session.get(
        'customer_name'
    )

    cart_items = Cart.objects.filter(
        customer_name=customer_name
    )

    total = 0

    for item in cart_items:

        total += (
            item.product.price * item.quantity
        )

    delivery_type = request.session.get(
        'delivery_type',
        'Normal'
    )

    delivery_charge = 40

    estimated_days = "3-5 Days"

    if delivery_type == "Fast":

        delivery_charge = 100

        estimated_days = "1-2 Days"

    total += delivery_charge

    if request.method == "POST":
        
        payment_method = request.POST.get(
            'payment_method'
        )
        
        customer = Customer.objects.get(
            id=request.session.get(
                'customer_id'
            )
        )

        address = Address.objects.filter(
            customer=customer
        ).last()

        warehouse = assign_warehouse(
            address.city
        )

        partner = assign_delivery_partner()

        # DELIVERY ESTIMATION

        if delivery_type == "Fast":

            if warehouse:

                estimated_delivery = "1 Day"

            else:

                estimated_delivery = "2 Days"

        else:

            if warehouse:

                estimated_delivery = "3 Days"

            else:

                estimated_delivery = "5 Days"
        
        
        for item in cart_items:

            reward_points = int(
                item.product.price / 100
            )

            if delivery_type == "Fast":

                reward_points += 10

            if item.product.price > 5000:

                reward_points += 50
            
            package_id = (
                "PKG" +
                str(item.product.product_id) +
                str(customer.id)
            )
            
            packing_counter = (
                "Counter " +
                str((item.product.product_id % 3) + 1)
            )
            
            # PRIORITY LOGIC

            if delivery_type == "Fast":

                priority = "High"

            elif item.product.price > 5000:

                priority = "Medium"

            else:

                priority = "Low"
            
            Order.objects.create(

                customer_name=customer.username,

                customer_location=address.city,

                product=item.product,

                quantity=item.quantity,

                delivery_type=delivery_type,

                order_status="Placed",

                warehouse=warehouse,

                delivery_partner=partner,

                reward_points=reward_points,
                
                estimated_delivery=estimated_delivery,
                
                package_id=package_id,
                    
                packing_counter=packing_counter,
                
                priority=priority    
            )
            
            item.product.stock -= item.quantity
            
            item.product.save()


        cart_items.delete()

        return HttpResponse(
            "Order placed successfully"
        )

    return render(
        request,
        'shoppingapp/payment.html',
        {
            'cart_items': cart_items,

            'total': total,

            'delivery_type': delivery_type,

            'delivery_charge': delivery_charge,

            'estimated_days': estimated_days
        }
    )


# ==========================================
# ORDER HISTORY
# ==========================================

def order_history(request):
    
    update_order_statuses()
    
    if not request.session.get(
        'customer_name'
    ):

        return redirect('/login/')

    customer_name = request.session.get(
        'customer_name'
    )

    orders = Order.objects.filter(
        customer_name=customer_name
    ).order_by('-id')

    return render(
        request,
        'shoppingapp/orders.html',
        {
            'orders': orders
        }
    )
    
def buy_product(request, product_id):

    if not request.session.get(
        'customer_name'
    ):

        return redirect('/login/')

    product = Product.objects.get(
        product_id=product_id
    )

    customer_name = request.session.get(
        'customer_name'
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

    return redirect('/checkout-address/')


def seller_login(request):

    if request.method == "POST":

        seller_name = request.POST.get(
            "username"
        )

        request.session[
            'seller_name'
        ] = seller_name

        return HttpResponse(
            "Seller logged in successfully"
        )

    return HttpResponse(
        "Seller Login Page"
    )
    
    
def delivery_login(request):

    if request.method == "POST":

        delivery_name = request.POST.get(
            "username"
        )

        request.session[
            'delivery_name'
        ] = delivery_name

        return HttpResponse(
            "Delivery Partner Logged In"
        )

    return HttpResponse(
        "Delivery Login Page"
    )
    
    
def seller_add_product(request):

    seller_name = request.session.get(
        'seller_name',
        'Unknown Seller'
    )

    Product.objects.create(

        name="New Product",

        category="Electronics",

        price=999,

        stock=10,

        seller_name=seller_name,

        image_url="https://via.placeholder.com/200"
    )

    return HttpResponse(
        f"Product added by seller {seller_name}"
    )
    
    
# ==========================================
# REMOVE CART ITEM
# ==========================================

def remove_cart_item(request, cart_id):

    cart_item = Cart.objects.get(
        id=cart_id
    )

    cart_item.delete()

    return redirect('/cart/')


# ==========================================
# SELLER DASHBOARD
# ==========================================

def seller_dashboard(request):

    seller_name = request.session.get(
        'seller_name'
    )

    if not seller_name:

        return HttpResponse(
            "Seller not logged in"
        )

    products = Product.objects.filter(
        seller_name=seller_name
    )

    return render(
        request,
        'shoppingapp/seller_dashboard.html',
        {
            'products': products,
            'seller_name': seller_name
        }
    )


# ==========================================
# PRODUCT DETAIL
# ==========================================

def product_detail(request, product_id):

    product = Product.objects.get(
        product_id=product_id
    )

    return render(
        request,
        'shoppingapp/product_detail.html',
        {
            'product': product
        }
    )


# ==========================================
# DELIVERY DASHBOARD
# ==========================================

def delivery_dashboard(request):

    orders = Order.objects.exclude(
        order_status="Delivered"
    ).exclude(
        order_status="Cancelled"
    ).exclude(
        order_status="Returned"
    )

    return render(
        request,
        'shoppingapp/delivery_dashboard.html',
        {
            'orders': orders
        }
    )
    
# ==========================================
# CANCEL ORDER
# ==========================================

def cancel_order(request, order_id):

    order = Order.objects.get(
        id=order_id
    )

    order.order_status = "Cancelled"

    order.save()

    return redirect('/orders/')


# ==========================================
# RETURN ORDER
# ==========================================

def return_order(request, order_id):

    order = Order.objects.get(
        id=order_id
    )

    order.order_status = "Returned"

    order.save()

    return redirect('/orders/')


# ==========================================
# UPDATE DELIVERY STATUS
# ==========================================

def update_delivery_status(request, order_id):

    order = Order.objects.get(
        id=order_id
    )

    # WAREHOUSE FLOW

    if order.order_status == "Placed":

        order.order_status = "Packed"

    elif order.order_status == "Packed":

        order.order_status = "Dispatched"

    # DELIVERY FLOW

    elif order.order_status == "Dispatched":

        order.order_status = "Out for Delivery"

    elif order.order_status == "Out for Delivery":

        order.order_status = "Delivered"

    order.save()

    return redirect('/delivery/dashboard/')

def staff_portal(request):

    return render(
        request,
        'shoppingapp/staff_portal.html'
    )

def update_order_statuses():

    orders = Order.objects.all()

    for order in orders:

        time_passed = timezone.now() - order.order_time

        hours = time_passed.total_seconds() / 3600

        if order.delivery_type == "Fast":

            if hours >= 1:

                order.order_status = "Packed"

            if hours >= 2:

                order.order_status = "Dispatched"

            if hours >= 3:

                order.order_status = "Delivered"

        else:

            if hours >= 2:

                order.order_status = "Packed"

            if hours >= 4:

                order.order_status = "Dispatched"

            if hours >= 6:

                order.order_status = "Delivered"

        order.save()