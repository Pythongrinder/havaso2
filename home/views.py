from django.shortcuts import render
from blog.models import Post
from home.models import WebContent
from django.contrib import messages
from .forms import ContactForm
from havasoweb.session import check_set_session
from django.http import HttpResponse 
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

def services(request):
    check_set_session(request)
    context = {
        'title': 'Services',
        'PageContent': WebContent.objects.get(position="Services")
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
        'PageContent': WebContent.objects.get(position="Contact"),
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

def contact2(request):
    check_set_session(request)
    form = ContactForm()
    context = {
        'title': 'Contact Us',
        'PageContent': WebContent.objects.get(position="Contact"),
        'PageContent2': WebContent.objects.get(position="Contactdetails"),
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
    return render(request, 'home/contact2.html', context)
