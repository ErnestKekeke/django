from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404

from blog.models import Post
from django.utils import timezone
import json


def index(request):
    return render(request, "blog/home.html")
    return HttpResponse("<h2>Hello blog posts!</h2>")


# def posts(request):
#     # # Fetch all posts from the database
#     # all_posts = Post.objects.all().order_by('-created_at')  # order_by optional 
#     # context = {'posts': all_posts}
#     # return render(request, 'blog/posts.html', context)


# Send to HTML PAGE
def posts(request):
    # Method A ................................
    # Fetch all posts from the database
    all_posts = Post.objects.all().values('id', 'title', 'content', 'created_at')
    # Convert QuerySet to list for JSON serialization
    posts_list = list(all_posts)
    return JsonResponse(posts_list, safe=False)  # safe=False allows returning a list

    #Method B .................................
    all_posts = Post.objects.all()  # Fetch all posts from the database
    # Convert each Post object into a dictionary
    posts_list = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at
        }
        for post in all_posts
    ]
    return JsonResponse(posts_list, safe=False)


def post(request, id):
    try:
        post_obj = Post.objects.get(id=id)
        post_data = {
            'id': post_obj.id,
            'title': post_obj.title,
            'content': post_obj.content,
            'created_at': post_obj.created_at
        }
        return JsonResponse(post_data)
    except Post.DoesNotExist:
        raise Http404("Post not found")


# Using HTML Form
def add_post(request):
    if request.method == 'POST':
        # for json format body, like in POSTMAN
        # data = json.loads(request.body) 
        # title = data.get('title')
        # content = data.get('content')

        # Get form data (no JSON decoding)
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return JsonResponse({'error': 'Title and content are required'}, status=400)

        post = Post.objects.create(title=title, content=content)
        return JsonResponse({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat()  # convert datetime to string
        }, status=201)




# def add_post(request):
#     # Create a new post directly
#     post = Post.objects.create(
#         title="My Add a new Post",
#         content="A new post is added.",
#         created_at= timezone.now() # optional if your model auto-adds
#     )
#     # Optional: check that it worked
#     print(post.id, post.title, post.content, post.created_at)

#     # return JSON
#     return JsonResponse({
#         'id': post.id,
#         'title': post.title,
#         'content': post.content,
#         'created_at': post.created_at.isoformat()  # convert datetime to string
#     }, status=201)




def age_page(request):
    # If user passes age check, this page is shown
    return HttpResponse("Welcome! You are old enough to see this page.")