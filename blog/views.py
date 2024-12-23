from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm


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

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ziadfox888@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'post_share.html', {'post': post,
                                                'form': form,
                                                'sent': sent})