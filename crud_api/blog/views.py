from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse, Http404
from .models import Post
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')


def allposts(request):
    if request.method == 'GET':
        # posts = Post.objects.all() # for HTML page
        # return JsonResponse({
        #     'msg': 'all posts'
        # })
        posts = list(Post.objects.values('id', 'title', 'body', 'created_at', 'updated_at'))
        return JsonResponse(posts, safe=False)


def singlepost(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)  # get post by id
        post_data = {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created_at': post.created_at,
            'updated_at': post.updated_at
        }
        return JsonResponse(post_data)

def createpost(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').title()
        body = request.POST.get('body', '').strip()

        if not title or not body:
            # Return to HTML Form
            return JsonResponse ({'msg': 'no title or content'})
        
        post = Post.objects.create(
            title = title,
            body = body,
            created_at = timezone.now(),
            updated_at = timezone.now()
        )
        # Return Success JSON Message
        return JsonResponse({
            'id': post.id,
            'msg': 'Post created successfully',
        }, status=201)
    

def editpost(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)  # get post by id
        title = request.POST.get('title', '').title()
        body = request.POST.get('body', '').strip()

        # Update fields
        post.title = title
        post.body = body
        post.updated_at = timezone.now()
        post.save()

        return JsonResponse({
            'id': post.id,
            'msg': 'Post updated successfully'
        }, status=200)
    

def deletepost(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)  # get post by id
        post_id = post.id  # store id before deletion
        post.delete()
        return JsonResponse({
            'id': post_id,
            'msg': 'Post deleted successfully'
        }, status=200)