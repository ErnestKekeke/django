from django.urls import path
from . import views

app_name = "main"  # namespace import to avoid conflicts 

urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.about, name='about')
]
 