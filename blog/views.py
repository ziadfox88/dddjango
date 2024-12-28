from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm,CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def post_list(request,tag_slug=None):
    post_list = Post.objects.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page',1)
    
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'post_list.html', {'posts': posts , 'tag':tag})
    
    
#class PostListView(ListView):
    #model = Post
    #context_object_name = 'posts'
    #paginate_by = 3
    #template_name = 'post_list.html'


def post_detail(request,year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=post) 
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    
    return render(request, 'post_detail.html', {'post': post , 'comments':comments,'form':form,'similar_posts':similar_posts})

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
    
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
        
    if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return render(request, 'post_comment.html', {'post': post,
                                                'form': form,'comment':comment})