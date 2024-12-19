from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id , status=Post.Status.PUBLISHED) 
    return render(request, 'post_detail.html', {'post': post})