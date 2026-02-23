from django.urls import path
from . import views

app_name = "calculator"

urlpatterns = [
    path('', views.home, name='home'),
    path('calulate/', views.calu, name='cal'),
    path('agepage/', views.check_age_page, name='agepage'),
]