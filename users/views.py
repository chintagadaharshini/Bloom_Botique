from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm


# ─────────────────────────────────────────
# REGISTER VIEW
# ─────────────────────────────────────────
def register_view(request):
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, f'Welcome to Bloom Boutique, {user.first_name}! 🌸')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# ─────────────────────────────────────────
# LOGIN VIEW
# ─────────────────────────────────────────
def login_view(request):
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 🌸')
            # Redirect to next page if specified, else home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


# ─────────────────────────────────────────
# LOGOUT VIEW
# ─────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out. See you soon! 👋')
    return redirect('home')


# ─────────────────────────────────────────
# PROFILE VIEW
# ─────────────────────────────────────────
@login_required(login_url='login')
def profile_view(request):
    # Get user's orders — we'll populate this in Step 10
    orders = request.user.orders.all()
    context = {
        'orders': orders
    }
    return render(request, 'users/profile.html', context)