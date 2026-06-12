from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


# ─────────────────────────────────────────
# HELPER FUNCTION
# ─────────────────────────────────────────
def get_or_create_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart


# ─────────────────────────────────────────
# HOME VIEW
# ─────────────────────────────────────────
def home(request):
    products = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


# ─────────────────────────────────────────
# PRODUCT LIST VIEW
# ─────────────────────────────────────────
def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'store/product_list.html', context)


# ─────────────────────────────────────────
# PRODUCT DETAIL VIEW
# ─────────────────────────────────────────
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


# ─────────────────────────────────────────
# CART VIEW
# ─────────────────────────────────────────
@login_required(login_url='login')
def cart_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


# ─────────────────────────────────────────
# ADD TO CART
# ─────────────────────────────────────────
@login_required(login_url='login')
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated quantity of {product.name}! 🛒')
    else:
        messages.success(request, f'{product.name} added to cart! 🛒')

    next_url = request.META.get('HTTP_REFERER', 'cart')
    return redirect(next_url)


# ─────────────────────────────────────────
# CART UPDATE
# ─────────────────────────────────────────
@login_required(login_url='login')
def cart_update(request, item_id):
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user
    )
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
            return redirect('cart')

    return redirect('cart')


# ─────────────────────────────────────────
# CART REMOVE
# ─────────────────────────────────────────
@login_required(login_url='login')
def cart_remove(request, item_id):
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user
    )
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart')


# ─────────────────────────────────────────
# CHECKOUT VIEW
# ─────────────────────────────────────────
@login_required(login_url='login')
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    # If cart is empty redirect to shop
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the Order
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                total_price=cart.get_total(),
                status='pending'
            )

            # Create OrderItems from CartItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Clear the cart after order
            cart_items.delete()

            messages.success(
                request,
                f'Order #{order.id} placed successfully! 🎉'
            )
            return redirect('order_summary', order_id=order.id)
    else:
        # Pre-fill email from user account
        form = CheckoutForm(initial={
            'email': request.user.email,
            'full_name': request.user.get_full_name()
        })

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


# ─────────────────────────────────────────
# ORDER SUMMARY VIEW
# ─────────────────────────────────────────
@login_required(login_url='login')
def order_summary(request, order_id):
    order = get_object_or_404(
        Order, id=order_id, user=request.user
    )
    order_items = order.items.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_summary.html', context)
