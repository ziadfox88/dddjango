from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView


# Create your views here.
#def post_list(request):
    #post_list = Post.objects.all()
    #paginator = Paginator(post_list, 2)
    #page_number = request.GET.get('page',1)
    
    #try:
        #posts = paginator.page(page_number)
    #except EmptyPage:
        #posts = paginator.page(paginator.num_pages) 
    #except PageNotAnInteger:
        #posts = paginator.page(1)
    #return render(request, 'post_list.html', {'posts': posts})
    
    
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post_list.html'


def post_detail(request,year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=post) 
    return render(request, 'post_detail.html', {'post': post})