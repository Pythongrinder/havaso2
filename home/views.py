from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post
from album.models import Jar
from home.models import WebContent
# from newsletter.forms import NewsletterForm
from django.contrib import messages
from .forms import ContactForm
# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

description = "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Morbi leo risus, porta ac consectetur ac, vestibulum at eros."


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_set_session(request):
    current_session_state = request.session.get('session')
    if current_session_state is None:
        ip = get_client_ip(request)
        print("It is triggered!")
        request.session['session'] = {
            'ip': ip,
            'products': [],
            'buy': "",
            'purpose': "",
            'purposetext': '',
            'invoice': '',
        }
        current_session_state = request.session.get('session')
        return current_session_state
    else:
        return current_session_state


def index(request):
    context = {
        'title': 'Homepage',
        'description': WebContent.objects.get(position="HomePageDescriptionText"),
        'posts': Post.objects.filter(categories__position='Jars').order_by('-date_created')[:3],
    }

    print(Site.objects.get_current())
    print(check_set_session(request))

    return render(request, 'home/index.html', context)


def about(request):
    context = {
        'AboutText': WebContent.objects.get(position="AboutPageText")
    }
    print(request.session.get('session'))
    request.session.clear()
    return render(request, 'home/about.html', context)


def page(request):
    content = request.GET
    print(content['page'])

    context = {
        'AboutText': WebContent.objects.get(position=content['page'])
    }
    print(request.session.get('wishlist'))
    return render(request, 'home/about.html', context)


def contact(request):
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
            messages.success(request, 'Thank you for signing up!')
        else:
            messages.error(request, 'Email not valid or already exists!')
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', context)
