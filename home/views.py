from django.shortcuts import render
from blog.models import Post
from home.models import WebContent
from django.contrib import messages
from .forms import ContactForm
from havasoweb.session import check_set_session
import logging

def index(request):
    check_set_session(request)
    context = {
        'title': 'Homepage',
        'description': WebContent.objects.get(position="HomePageDescriptionText"),
        'posts': Post.objects.filter(categories__position='Jars').order_by('-date_created')[:3],
    }
    return render(request, 'home/index.html', context)


def about(request):
    check_set_session(request)
    context = {
        'title': 'About',
        'PageContent': WebContent.objects.get(position="AboutPageText")
    }
    return render(request, 'home/page.html', context)

def cng(request):
    check_set_session(request)
    context = {
        'title': 'About',
        'PageContent': WebContent.objects.get(position="CNGPageText")
    }
    return render(request, 'home/page.html', context)


def page(request):
    check_set_session(request)
    content = request.GET
    context = {
        'PageContent': WebContent.objects.get(position=content['page'])
    }
    return render(request, 'home/page.html', context)


def contact(request):
    check_set_session(request)
    form = ContactForm()
    context = {
        'title': 'Contact Us',
        'form': form
    }

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()
            messages.success(request, 'Thank you!')
        else:
            messages.error(request, 'Email not valid or already exists!')
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', context)
