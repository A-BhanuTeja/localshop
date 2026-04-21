from django import forms
from .models import Shop, Product, DeliveryRule, Coupon, Review, DamageReport


class ShopForm(forms.ModelForm):
    class Meta:
        model  = Shop
        fields = [
            'name', 'slug', 'tagline', 'logo',
            'theme_color', 'address', 'phone',
            'email', 'is_open', 'closed_msg'
        ]
        widgets = {
            'name'       : forms.TextInput(attrs={'class': 'form-control'}),
            'slug'       : forms.TextInput(attrs={'class': 'form-control'}),
            'tagline'    : forms.TextInput(attrs={'class': 'form-control'}),
            'theme_color': forms.TextInput(attrs={
                'class': 'form-control',
                'type' : 'color'
            }),
            'address'   : forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'phone'     : forms.TextInput(attrs={'class': 'form-control'}),
            'email'     : forms.EmailInput(attrs={'class': 'form-control'}),
            'closed_msg': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = [
            'name', 'description', 'price', 'image',
            'category', 'stock_count', 'low_stock_threshold',
            'expiry_date', 'is_available'
        ]
        widgets = {
            'name'       : forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'price'      : forms.NumberInput(attrs={'class': 'form-control'}),
            'category'   : forms.TextInput(attrs={'class': 'form-control'}),
            'stock_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'low_stock_threshold': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
        }


class DeliveryRuleForm(forms.ModelForm):
    class Meta:
        model  = DeliveryRule
        fields = ['free_delivery_above', 'delivery_charge']
        widgets = {
            'free_delivery_above': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg'
            }),
            'delivery_charge': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg'
            }),
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model  = Coupon
        fields = ['code', 'discount_percent', 'min_order_amount', 'is_active']
        widgets = {
            'code'            : forms.TextInput(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_order_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ReviewReplyForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['owner_reply']
        widgets = {
            'owner_reply': forms.Textarea(attrs={
                'class'      : 'form-control',
                'rows'       : 3,
                'placeholder': 'Write your reply...'
            }),
        }


class DamageResolveForm(forms.ModelForm):
    class Meta:
        model  = DamageReport
        fields = ['resolution_note']
        widgets = {
            'resolution_note': forms.Textarea(attrs={
                'class'      : 'form-control',
                'rows'       : 3,
                'placeholder': 'Describe resolution...'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['stars', 'comment']
        widgets = {
            'stars'  : forms.Select(
                choices=[(i, '★' * i) for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(attrs={
                'class'      : 'form-control',
                'rows'       : 3,
                'placeholder': 'Write your review (optional)'
            }),
        }


class DamageReportForm(forms.ModelForm):
    class Meta:
        model  = DamageReport
        fields = ['product_name', 'photo', 'message']
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class'      : 'form-control',
                'placeholder': 'Which product was damaged?'
            }),
            'message': forms.Textarea(attrs={
                'class'      : 'form-control',
                'rows'       : 3,
                'placeholder': 'Describe the damage...'
            }),
        }