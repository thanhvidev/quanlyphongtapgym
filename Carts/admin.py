from django.contrib import admin
from .models import CartItem


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id', 'courses', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['id', 'cart_id', 'courses',  'is_active']


admin.site.register(CartItem, CartItemAdmin)
