from django.urls import path
from . import views

urlpatterns = [
    # Store pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_summary, name='order_summary'),
]
