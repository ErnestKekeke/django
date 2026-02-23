from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('post/<int:id>/', views.post, name='post'),
    path('addpost/', views.add_post, name='addpost'),
    path('agepage/', views.age_page, name='agepage'),
]