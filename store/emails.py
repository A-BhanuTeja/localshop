from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation(order):
    # Email to customer
    subject = f"Order Confirmed — {order.shop.name} (Order #{order.id})"
    items_text = "\n".join([
        f"  • {item.name} × {item.quantity} = ₹{item.subtotal()}"
        for item in order.items.all()
    ])
    message = f"""
Hi {order.customer_name},

Thank you for your order from {order.shop.name}!

Order #{order.id}
─────────────────
{items_text}

Products Total : ₹{order.total_amount}
Delivery Charge: ₹{order.delivery_charge}
Grand Total    : ₹{order.grand_total()}

Delivery Address:
{order.customer_address}

We will notify you once your order is confirmed.

— {order.shop.name}
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.customer_email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_order_to_owner(order):
    # Email to shop owner
    subject = f"New Order #{order.id} — {order.customer_name}"
    items_text = "\n".join([
        f"  • {item.name} × {item.quantity} = ₹{item.subtotal()}"
        for item in order.items.all()
    ])
    message = f"""
New order received!

Customer  : {order.customer_name}
Phone     : {order.customer_phone}
Email     : {order.customer_email}
Address   : {order.customer_address}

Items Ordered:
{items_text}

Grand Total: ₹{order.grand_total()}
Payment    : {order.payment_method.upper()}

Login to your dashboard to confirm:
http://127.0.0.1:8000/dashboard/orders/{order.id}/
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.shop.email or settings.EMAIL_HOST_USER],
            fail_silently=True,
        )
    except Exception:
        pass


def send_review_request(order):
    # Sent after owner marks order as delivered
    subject = f"How was your order from {order.shop.name}?"
    message = f"""
Hi {order.customer_name},

Your order #{order.id} from {order.shop.name} has been delivered!

We'd love to know how your experience was.
Take 30 seconds to rate your order here:

http://127.0.0.1:8000/shop/{order.shop.slug}/review/{order.id}/

Thank you for shopping with {order.shop.name}!
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.customer_email],
            fail_silently=True,
        )
    except Exception:
        pass