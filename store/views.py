from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shop, Product, Order, OrderItem, DeliveryRule, Coupon, Review, DamageReport


# ── AUTH ─────────────────────────────────────
def owner_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Wrong username or password')
    return render(request, 'dashboard/login.html')


def owner_logout(request):
    logout(request)
    return redirect('owner_login')


# ── DASHBOARD HOME ────────────────────────────
@login_required(login_url='/dashboard/login/')
def dashboard_home(request):
    shop = get_object_or_404(Shop, owner=request.user)
    total_orders   = Order.objects.filter(shop=shop).count()
    pending_orders = Order.objects.filter(shop=shop, status='pending').count()
    total_products = Product.objects.filter(shop=shop).count()
    low_stock      = Product.objects.filter(shop=shop, is_available=True).count()
    context = {
        'shop': shop,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'low_stock': low_stock,
    }
    return render(request, 'dashboard/home.html', context)


# ── PRODUCTS ──────────────────────────────────
@login_required(login_url='/dashboard/login/')
def product_list(request):
    shop     = get_object_or_404(Shop, owner=request.user)
    products = Product.objects.filter(shop=shop)
    return render(request, 'dashboard/products.html', {'shop': shop, 'products': products})


@login_required(login_url='/dashboard/login/')
def product_add(request):
    shop = get_object_or_404(Shop, owner=request.user)
    if request.method == 'POST':
        Product.objects.create(
            shop        = shop,
            name        = request.POST['name'],
            description = request.POST.get('description', ''),
            price       = request.POST['price'],
            category    = request.POST.get('category', ''),
            stock_count = request.POST['stock_count'],
            low_stock_threshold = request.POST.get('low_stock_threshold', 5),
            expiry_date = request.POST.get('expiry_date') or None,
            image       = request.FILES.get('image'),
        )
        messages.success(request, 'Product added successfully!')
        return redirect('product_list')
    return render(request, 'dashboard/product_form.html', {'shop': shop, 'action': 'Add'})


@login_required(login_url='/dashboard/login/')
def product_edit(request, pk):
    shop    = get_object_or_404(Shop, owner=request.user)
    product = get_object_or_404(Product, pk=pk, shop=shop)
    if request.method == 'POST':
        product.name        = request.POST['name']
        product.description = request.POST.get('description', '')
        product.price       = request.POST['price']
        product.category    = request.POST.get('category', '')
        product.stock_count = request.POST['stock_count']
        product.low_stock_threshold = request.POST.get('low_stock_threshold', 5)
        product.expiry_date = request.POST.get('expiry_date') or None
        product.is_available = 'is_available' in request.POST
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, 'Product updated!')
        return redirect('product_list')
    return render(request, 'dashboard/product_form.html', {'shop': shop, 'product': product, 'action': 'Edit'})


@login_required(login_url='/dashboard/login/')
def product_delete(request, pk):
    shop    = get_object_or_404(Shop, owner=request.user)
    product = get_object_or_404(Product, pk=pk, shop=shop)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect('product_list')


# ── ORDERS ────────────────────────────────────
@login_required(login_url='/dashboard/login/')
def order_list(request):
    shop   = get_object_or_404(Shop, owner=request.user)
    orders = Order.objects.filter(shop=shop).order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'shop': shop, 'orders': orders})


@login_required(login_url='/dashboard/login/')
def order_detail(request, pk):
    shop  = get_object_or_404(Shop, owner=request.user)
    order = get_object_or_404(Order, pk=pk, shop=shop)
    return render(request, 'dashboard/order_detail.html', {'shop': shop, 'order': order})


@login_required(login_url='/dashboard/login/')
def order_status(request, pk):
    shop  = get_object_or_404(Shop, owner=request.user)
    order = get_object_or_404(Order, pk=pk, shop=shop)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        messages.success(request, f'Order status updated to {order.status}!')
    return redirect('order_detail', pk=pk)


# ── DELIVERY ──────────────────────────────────
@login_required(login_url='/dashboard/login/')
def delivery_rule(request):
    shop = get_object_or_404(Shop, owner=request.user)
    rule, created = DeliveryRule.objects.get_or_create(shop=shop)
    if request.method == 'POST':
        rule.free_delivery_above = request.POST['free_delivery_above']
        rule.delivery_charge     = request.POST['delivery_charge']
        rule.save()
        messages.success(request, 'Delivery rule updated!')
    return render(request, 'dashboard/delivery.html', {'shop': shop, 'rule': rule})


# ── COUPONS ───────────────────────────────────
@login_required(login_url='/dashboard/login/')
def coupon_list(request):
    shop    = get_object_or_404(Shop, owner=request.user)
    coupons = Coupon.objects.filter(shop=shop)
    if request.method == 'POST':
        Coupon.objects.create(
            shop             = shop,
            code             = request.POST['code'].upper(),
            discount_percent = request.POST['discount_percent'],
            min_order_amount = request.POST.get('min_order_amount', 0),
        )
        messages.success(request, 'Coupon created!')
        return redirect('coupon_list')
    return render(request, 'dashboard/coupons.html', {'shop': shop, 'coupons': coupons})


# ── DAMAGE REPORTS ────────────────────────────
@login_required(login_url='/dashboard/login/')
def damage_reports(request):
    shop    = get_object_or_404(Shop, owner=request.user)
    reports = DamageReport.objects.filter(order__shop=shop).order_by('-created_at')
    return render(request, 'dashboard/damage_reports.html', {'shop': shop, 'reports': reports})


# ── REVIEWS ───────────────────────────────────
@login_required(login_url='/dashboard/login/')
def review_list(request):
    shop    = get_object_or_404(Shop, owner=request.user)
    reviews = Review.objects.filter(order__shop=shop).order_by('-created_at')
    return render(request, 'dashboard/reviews.html', {'shop': shop, 'reviews': reviews})


# ── CUSTOMER STOREFRONT ───────────────────────
def storefront(request, shop_slug):
    shop     = get_object_or_404(Shop, slug=shop_slug)
    products = Product.objects.filter(shop=shop, is_available=True)
    return render(request, 'storefront/shop.html', {'shop': shop, 'products': products})


def cart(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug)
    return render(request, 'storefront/cart.html', {'shop': shop})


def checkout(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug)

    try:
        rule = shop.delivery_rule
    except DeliveryRule.DoesNotExist:
        rule = None

    if request.method == 'POST':
        # Get cart data sent from frontend
        import json
        cart_data     = request.POST.get('cart_data', '[]')
        cart_items    = json.loads(cart_data)

        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('storefront', shop_slug=shop_slug)

        # Calculate totals
        total = sum(
            float(item['price']) * int(item['qty'])
            for item in cart_items
        )
        delivery_charge = 0
        if rule:
            delivery_charge = (
                0 if total >= float(rule.free_delivery_above)
                else float(rule.delivery_charge)
            )

        # Handle coupon
        coupon_code     = request.POST.get('coupon_code', '').upper()
        discount_amount = 0
        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    shop=shop,
                    code=coupon_code,
                    is_active=True
                )
                if total >= float(coupon.min_order_amount):
                    discount_amount = total * coupon.discount_percent / 100
            except Coupon.DoesNotExist:
                pass

        # Create Order
        order = Order.objects.create(
            shop             = shop,
            customer_name    = request.POST['customer_name'],
            customer_email   = request.POST['customer_email'],
            customer_phone   = request.POST['customer_phone'],
            customer_address = request.POST['customer_address'],
            total_amount     = total,
            delivery_charge  = delivery_charge,
            discount_amount  = discount_amount,
            coupon_used      = coupon_code,
            payment_method   = request.POST.get('payment_method', 'cod'),
        )

        # Create Order Items + reduce stock
        for item in cart_items:
            OrderItem.objects.create(
                order    = order,
                name     = item['name'],
                price    = item['price'],
                quantity = item['qty'],
            )
            # Reduce stock count
            try:
                product = Product.objects.get(
                    id=item['id'], shop=shop
                )
                product.stock_count = max(
                    0, product.stock_count - int(item['qty'])
                )
                product.save()
            except Product.DoesNotExist:
                pass

        # Send emails
        from .emails import send_order_confirmation, send_order_to_owner
        send_order_confirmation(order)
        send_order_to_owner(order)

        # Clear cart instruction to frontend
        return redirect('order_tracking',
                        shop_slug=shop_slug, pk=order.pk)

    context = {
        'shop': shop,
        'rule': rule,
    }
    return render(request, 'storefront/checkout.html', context)


def order_tracking(request, shop_slug, pk):
    shop  = get_object_or_404(Shop, slug=shop_slug)
    order = get_object_or_404(Order, pk=pk, shop=shop)
    return render(request, 'storefront/order_track.html', {'shop': shop, 'order': order})


def submit_review(request, shop_slug, pk):
    shop  = get_object_or_404(Shop, slug=shop_slug)
    order = get_object_or_404(Order, pk=pk, shop=shop)
    if request.method == 'POST':
        Review.objects.create(
            order   = order,
            stars   = request.POST.get('stars', 5),
            comment = request.POST.get('comment', ''),
        )
        messages.success(request, 'Thank you for your review!')
    return redirect('order_tracking', shop_slug=shop_slug, pk=pk)


def submit_damage(request, shop_slug, pk):
    shop  = get_object_or_404(Shop, slug=shop_slug)
    order = get_object_or_404(Order, pk=pk, shop=shop)
    if request.method == 'POST':
        DamageReport.objects.create(
            order        = order,
            product_name = request.POST['product_name'],
            message      = request.POST['message'],
            photo        = request.FILES.get('photo'),
        )
        messages.success(request, 'Damage report submitted!')
    return redirect('order_tracking', shop_slug=shop_slug, pk=pk)