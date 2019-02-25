from django.shortcuts import render
from album.models import Jar
from blog.models import Post
from home.views import check_set_session
from django.db.models import Q


# Create your views here.

def album(request):
    check_set_session(request)
    context = {
        'title': 'Jar Album',
        'posts': Post.objects.all().order_by('-date_created')[:3],
        'jar': Jar.objects.filter(Q(jar_status='Available') | Q(jar_status='Sold')).order_by('jar_number'),
    }

    return render(request, 'album/album.html', context)


def historic_album(request):
    check_set_session(request)
    context = {
        'title': 'Jar Album',
        'posts': Post.objects.all().order_by('-date_created')[:3],
        'jar': Jar.objects.filter(
            Q(jar_status='Historic Album') | Q(jar_status='Sold') | Q(jar_status='Damaged')).order_by('jar_number'),
    }

    return render(request, 'album/album.html', context)
