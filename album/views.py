from django.shortcuts import render
from album.models import Jar
from blog.models import Posts
from home.views import check_set_session


# Create your views here.

def album(request):


    check_set_session(request)
    context =  {
        'title' : 'Jar Album',
        'posts': Posts.objects.all().order_by('-date_created')[:3],
        'jar': Jar.objects.all(),
        }

    return render(request, 'album/album.html', context)

