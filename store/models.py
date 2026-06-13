from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ─────────────────────────────────────────
# CATEGORY MODEL
# Represents product categories like:
# "Electronics", "Clothing", "Books" etc.
# ─────────────────────────────────────────
class Category(models.Model):
    name = models.CharField(max_length=200)
    # slug = URL-friendly version of name
    # e.g. "Summer Collection" → "summer-collection"
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'  # Fix plural in admin panel
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ─────────────────────────────────────────
# PRODUCT MODEL
# Represents individual products in store
# ─────────────────────────────────────────
# ────────────────────────────────────────
# CART MODEL
# One cart per user (created when needed)
# ─────────────────────────────────────────
class Cart(models.Model):
    # OneToOneField = each user can only have ONE cart
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        # Sum up all cart items: price × quantity for each item
        return sum(item.get_subtotal() for item in self.items.all())


# ─────────────────────────────────────────
# CART ITEM MODEL
# Each row = one product in the cart
# ─────────────────────────────────────────
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'    # Access items via cart.items.all()
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.product.price * self.quantity


# ─────────────────────────────────────────
# ORDER MODEL
# Created when user completes checkout
# ─────────────────────────────────────────
class Order(models.Model):

    # Order status choices — tracks where the order is
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    # Shipping details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest orders first

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# ─────────────────────────────────────────
# ORDER ITEM MODEL
# Snapshot of each product in an order
# ─────────────────────────────────────────
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    # We store price at time of purchase
    # (product price might change later)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.price * self.quantity
    
    
