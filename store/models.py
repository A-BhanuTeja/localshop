from django.db import models
from django.contrib.auth.models import User


# ───────────────────────────────
# SHOP
# ───────────────────────────────
class Shop(models.Model):
    owner        = models.OneToOneField(User, on_delete=models.CASCADE)
    name         = models.CharField(max_length=100)
    slug         = models.SlugField(unique=True)
    tagline      = models.CharField(max_length=200, blank=True)
    logo         = models.ImageField(upload_to='logos/', blank=True, null=True)
    theme_color  = models.CharField(max_length=7, default='#16a34a')
    address      = models.TextField(blank=True)
    phone        = models.CharField(max_length=15, blank=True)
    email        = models.EmailField(blank=True)
    is_open      = models.BooleanField(default=True)
    closed_msg   = models.CharField(max_length=200, default='Shop is closed today. Please visit again!')
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ───────────────────────────────
# PRODUCT
# ───────────────────────────────
class Product(models.Model):
    shop               = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name               = models.CharField(max_length=100)
    description        = models.TextField(blank=True)
    price              = models.DecimalField(max_digits=8, decimal_places=2)
    image              = models.ImageField(upload_to='products/', blank=True, null=True)
    category           = models.CharField(max_length=50, blank=True)
    stock_count        = models.PositiveIntegerField(default=0)
    low_stock_threshold= models.PositiveIntegerField(default=5)
    expiry_date        = models.DateField(blank=True, null=True)
    is_available       = models.BooleanField(default=True)
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.shop.name})"

    def is_low_stock(self):
        return self.stock_count <= self.low_stock_threshold


# ───────────────────────────────
# DELIVERY RULE
# ───────────────────────────────
class DeliveryRule(models.Model):
    shop                  = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='delivery_rule')
    free_delivery_above   = models.DecimalField(max_digits=8, decimal_places=2, default=500)
    delivery_charge       = models.DecimalField(max_digits=6, decimal_places=2, default=30)

    def __str__(self):
        return f"Delivery rule for {self.shop.name}"


# ───────────────────────────────
# COUPON
# ───────────────────────────────
class Coupon(models.Model):
    shop            = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='coupons')
    code            = models.CharField(max_length=20)
    discount_percent= models.PositiveIntegerField(default=10)
    min_order_amount= models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active       = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% off"


# ───────────────────────────────
# ORDER
# ───────────────────────────────
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    shop              = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    customer_name     = models.CharField(max_length=100)
    customer_email    = models.EmailField()
    customer_phone    = models.CharField(max_length=15)
    customer_address  = models.TextField()
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount      = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge   = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount_amount   = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    coupon_used       = models.CharField(max_length=20, blank=True)
    payment_method    = models.CharField(max_length=20, default='cod')
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    def grand_total(self):
        return self.total_amount + self.delivery_charge - self.discount_amount


# ───────────────────────────────
# ORDER ITEM
# ───────────────────────────────
class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.name}"

    def subtotal(self):
        return self.price * self.quantity


# ───────────────────────────────
# REVIEW
# ───────────────────────────────
class Review(models.Model):
    order        = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    stars        = models.PositiveIntegerField(default=5)
    comment      = models.TextField(blank=True)
    owner_reply  = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars} stars - Order #{self.order.id}"


# ───────────────────────────────
# DAMAGE REPORT
# ───────────────────────────────
class DamageReport(models.Model):
    STATUS_CHOICES = [
        ('open',     'Open'),
        ('resolved', 'Resolved'),
    ]
    order           = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='damage_reports')
    product_name    = models.CharField(max_length=100)
    photo           = models.ImageField(upload_to='damage_reports/', blank=True, null=True)
    message         = models.TextField()
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    resolution_note = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Damage report - Order #{self.order.id}"
