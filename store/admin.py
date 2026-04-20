from django.contrib import admin
from .models import Shop, Product, DeliveryRule, Coupon, Order, OrderItem, Review, DamageReport


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_open', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price', 'stock_count', 'is_available']
    list_filter  = ['shop', 'is_available']


@admin.register(DeliveryRule)
class DeliveryRuleAdmin(admin.ModelAdmin):
    list_display = ['shop', 'free_delivery_above', 'delivery_charge']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'shop', 'discount_percent', 'is_active']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'shop', 'status', 'grand_total', 'created_at']
    list_filter  = ['status', 'shop']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'price', 'quantity']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'stars', 'created_at']


@admin.register(DamageReport)
class DamageReportAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'status', 'created_at']
    list_filter  = ['status']
