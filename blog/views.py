from django.shortcuts import render
from blog.models import Posts

# Create your views here.
def blog(request):

    content = request.GET

    try:
        post = Posts.objects.get(slug__iexact=content['post'])
        single = True
    except:
        if False:
            post = Posts.objects.all().order_by('-date_created')[5:]
        else:
            post = Posts.objects.all().order_by('-date_created')[:5]
        single = False

    context = {
        'single' : single,
        'post': post,
        'posts': Posts.objects.all().order_by('-date_created')[:3],
    }

    return render(request, 'blog/blog.html', context)