from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .forms import RegisterForm, PostForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'main/home.html')
    # return HttpResponse("<p>Welcome to Home<p>")

def registration(request):
    form = RegisterForm()
    return render(request, 'main/registration.html', {'form': form})


# @login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            # Extract cleaned data from the form
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            # Note you cannot have a feild called password

            # # Return a JSON response (never return the raw password in production!)
            # return JsonResponse({
            #     'username': username,
            #     'first_name': first_name,
            #     'last_name': last_name,
            #     'email': email
            # })
        
            # # Create and save the user Method A
            # user = User.objects.create_user(
            #     username=username,
            #     first_name=first_name,
            #     last_name=last_name,
            #     email=email,
            #     password=password
            # )

            form.save() # Method B
            messages.success(request, "Account created successfully!")

            return redirect('main:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()  # make sure the form instance is created here

    # return render(request, 'register.html', {'form': form})
    return render(request, 'main/registration.html', {'form': form})


# # Method A
# def register(request):
#     if request.method == 'POST':    
#         username = request.POST.get('username').strip().lower() 

#         # first_name = request.POST.get('first_name').strip().lower().capitalize()
#         first_name = request.POST.get('first_name', '').strip().title()
#         last_name = request.POST.get('last_name').strip().title()
#         email = request.POST.get('email').strip().lower()
#         password = request.POST.get('password').strip()
#         confirm_password = request.POST.get('confirm_password').strip()

#         if not all([username, first_name, last_name, email, password]):
#             messages.error(request, 'All fields are required')
#             return redirect('main:registration')
        
#         if password != confirm_password:
#             messages.error(request, 'password no match')
#             return redirect('main:registration')
        
#         # # to view form content
#         # return JsonResponse({
#         #     'username': username,
#         #     'first_name': first_name,
#         #     'last_name': last_name,
#         #     'email': email,
#         #     'password': password
#         # })

#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#             return redirect('main:registration')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists.')
#             return redirect('main:registration')
        
#         try:
#             user = User.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password,
#                 first_name=first_name,
#                 last_name=last_name
#             )
        
#             login(request, user)
#             messages.success(request, "Account created successfully!")
#             return redirect('main:home')

#         except IntegrityError:
#             messages.error(request, "Something went wrong. Try again.")
#             return redirect('main:registration')
#     else:
#         messages.error(request, "Method Not Allowed. Try again.")
#         return redirect('main:registration')
        

@require_POST
def login_view(request):
        identifier = request.POST.get('username_or_email', '').strip().lower()
        password = request.POST.get('password', '').strip()

        # Try as username
        user = authenticate(request, username=identifier, password=password)
        
        # If not username, try as email
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('main:home')
        
        messages.error(request, "Invalid username or password.")
        return redirect('main:home')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successful logout')
    return redirect('main:home')
