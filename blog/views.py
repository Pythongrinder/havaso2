from django.shortcuts import render
from blog.models import Post


# Create your views here.
def blog(request):
    content = request.GET

    try:
        post = Post.objects.get(slug__iexact=content['post'])
        single = True
    except:
        if False:
            post = Post.objects.all().order_by('-date_created')[5:]
        else:
            post = Post.objects.all().order_by('-date_created')[:5]
        single = False

    context = {
        'single': single,
        'post': post,
        'posts': Post.objects.all().order_by('-date_created')[:3],
    }

    return render(request, 'blog/blog.html', context)
