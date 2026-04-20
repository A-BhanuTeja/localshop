from django.urls import path
from . import views

urlpatterns = [

    # ── OWNER DASHBOARD ──────────────────────
    path('login/',    views.owner_login,    name='owner_login'),
    path('logout/',   views.owner_logout,   name='owner_logout'),
    path('',          views.dashboard_home, name='dashboard_home'),

    # products
    path('products/',          views.product_list,   name='product_list'),
    path('products/add/',      views.product_add,    name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # orders
    path('orders/',                       views.order_list,   name='order_list'),
    path('orders/<int:pk>/',              views.order_detail, name='order_detail'),
    path('orders/<int:pk>/status/',       views.order_status, name='order_status'),

    # delivery & coupons
    path('delivery/',  views.delivery_rule, name='delivery_rule'),
    path('coupons/',   views.coupon_list,   name='coupon_list'),

    # damage reports
    path('damage-reports/', views.damage_reports, name='damage_reports'),

    # reviews
    path('reviews/', views.review_list, name='review_list'),

    # ── CUSTOMER STOREFRONT ───────────────────
    path('<slug:shop_slug>/',             views.storefront,   name='storefront'),
    path('<slug:shop_slug>/cart/',        views.cart,         name='cart'),
    path('<slug:shop_slug>/checkout/',    views.checkout,     name='checkout'),
    path('<slug:shop_slug>/order/<int:pk>/', views.order_tracking, name='order_tracking'),
    path('<slug:shop_slug>/review/<int:pk>/', views.submit_review, name='submit_review'),
    path('<slug:shop_slug>/damage/<int:pk>/', views.submit_damage, name='submit_damage'),
]