from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


# ─────────────────────────────────────────
# CATEGORY ADMIN
# ─────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']        # Columns shown in list view
    prepopulated_fields = {'slug': ('name',)}  # Auto-fills slug from name


# ─────────────────────────────────────────
# PRODUCT ADMIN
# ─────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'category']   # Filter sidebar
    list_editable = ['price', 'stock', 'is_available']  # Edit inline
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']      # Search box


# ─────────────────────────────────────────
# CART ADMIN
# ─────────────────────────────────────────
class CartItemInline(admin.TabularInline):
    # Shows cart items INSIDE the cart page
    model = CartItem
    extra = 0   # Don't show empty extra rows


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]   # Show items inside cart


# ─────────────────────────────────────────
# ORDER ADMIN
# ─────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']    # Update order status directly from list
    search_fields = ['full_name', 'email', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'total_price', 'created_at']
