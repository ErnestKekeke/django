from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Logic
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

