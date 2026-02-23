from django.urls import path 
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.allposts, name='createpost'),
    path('posts/create', views.createpost, name='createpost'),
    path('posts/<int:id>/', views.singlepost, name='singlepost'),
    path('posts/<int:id>/edit/', views.editpost, name='editpost'),
    path('posts/<int:id>/delete/', views.deletepost, name='deletepost'),
]