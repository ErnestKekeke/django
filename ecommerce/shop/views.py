from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Product, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, "shop/home.html")

def shop(request):
    products = Product.objects.all()
    return render(request, "shop/shop.html", {"products": products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    # if product != None
    return render(request, "shop/product.html", {"product": product})

@login_required
def add_cart(request, id):
    # cart01 = {'a': 2, 'b': 3, 'c': 10,}
    # cart01['a'] = cart01['a'] + 2
    # cart01['a'] += 2
    # print(cart01['a'])
    # del cart01['c']
    # return HttpResponse(f"cart: {cart01}")

    # # for production use a databse and table 
    product = Product.objects.get(id=id)
    user = request.user
    print(user.username)
    print(product.id)

    # # ......... 
    # cart = request.session.get('cart', {})
    # if str(id) in cart:
    #     cart[str(id)] += 1
    # else:
    #     cart[str(product.id)] = 1
    # request.session['cart'] = cart
    # # ..........

    cart = request.session.get(user.username+'cart', {})
    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1
    request.session[user.username+'cart'] = cart

    # return HttpResponse(f"cart: {cart}")
    return redirect('shop:shop')


@login_required
def add_item(request, id):
    # # for production use a databse and table 
    product = Product.objects.get(id=id)
    user = request.user
    print(user.username)
    print(product.id)

    cart = request.session.get(user.username+'cart', {})
    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1
    request.session[user.username+'cart'] = cart

    # return HttpResponse(f"cart: {cart}")
    return redirect('shop:cart')

@login_required
def remove_item(request, id):
    # # for production use a databse and table 
    product = Product.objects.get(id=id)
    user = request.user
    print(user.username)
    print(product.id)

    cart = request.session.get(user.username+'cart', {})
    if str(product.id) in cart:
        if(cart[str(product.id)] > 1):
            cart[str(product.id)] -= 1
        else:
            del cart[str(product.id)]

    request.session[user.username+'cart'] = cart

    # return HttpResponse(f"cart: {cart}")
    return redirect('shop:cart')


@login_required
def cart(request):
    # cart = request.session.get('cart', {})
    user = request.user
    print(user.username)
    cart = request.session.get(user.username+'cart', {})
    # {'1': 4, '2': 1}

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product.total_price = product.price * quantity
        product.quantity = quantity
        total += product.total_price
        products.append(product)

    return render(request, "shop/cart.html", {
        "products": products,
        "total": total
    })

@login_required
def checkout(request):
    user = request.user
    cart = request.session.get(user.username+'cart', {})
    if not cart:
        messages.error(request, "Cart is empty.")
        return redirect("shop:cart")

    order = Order.objects.create(user=user)

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
    request.session[user.username+'cart'] = {}
    messages.success(request, "Order placed successfully!")

    return redirect("shop:shop")


def register_view(request):
    return render(request, "shop/register.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip().lower()
        first_name = request.POST.get("first_name", "").strip().title()
        last_name = request.POST.get("last_name", "").strip().title()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        # 🔹 Check if any field is empty
        if not username or not first_name or not last_name or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("shop:register")

        # 🔹 Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("shop:register")

        # 🔹 Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("shop:register")

        # 🔹 Create user safely (password hashed automatically)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully.")
        return redirect("shop:login")

    return render(request, "shop/register.html")


def login_view(request):
    return render(request, "shop/login.html")


def login_user(request):
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user = authenticate(request, username=username, password=password)
    #     if user:
    #         login(request, user)
    #         return redirect("home")
    # return render(request, "login.html")

    if request.method == "POST":
        username_or_email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # 🔹 Check empty fields
        if not username_or_email or not password:
            messages.error(request, "Both fields are required.")
            return redirect("shop:login")

        # 🔹 If input is email, convert to username
        if User.objects.filter(email=username_or_email).exists():
            user_obj = User.objects.filter(email=username_or_email).first()
            username = user_obj.username
        else:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("shop:shop")  # ✅ correct URL name
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("shop:login")

    return render(request, "shop/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, 'You have successful logout')
    return redirect('shop:home')
