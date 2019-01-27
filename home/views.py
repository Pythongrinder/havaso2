from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Posts
from album.models import Jar
from home.models import WebContent
# from newsletter.forms import NewsletterForm
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage

description = "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Morbi leo risus, porta ac consectetur ac, vestibulum at eros."

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_set_session(request):
    current_session_state = request.session.get('wishlist')
    if current_session_state is None:
        ip = get_client_ip(request)
        print("It is triggered!")
        request.session['wishlist'] = {
            'ip': ip,
            'products': ''
        }
        current_session_state = request.session.get('wishlist')
        return current_session_state
    else:
        return current_session_state



def index(request):


    # if request.method == "POST":
    #     form = NewsletterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form = NewsletterForm()
    #         messages.success(request, 'Thank you for signing up!')
    #     else:
    #         messages.error(request, 'Email not valid or already exists!')
    #         form = NewsletterForm()
    # else:
    #     form = NewsletterForm()

    context =  {
        'title' : 'Homepage',
        'description' : WebContent.objects.get(position__iexact="HomePageDescriptionText"),
         'posts' : Posts.objects.all().order_by('-date_created')[:3],
        }


    print(check_set_session(request))
    print(request.session.get('wishlist'))

    return render(request, 'home/index.html', context)

def album(request):
    print(request.session.get('wishlist'))
    # if request.method == "POST":
    #     form = NewsletterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form = NewsletterForm()
    #         messages.success(request, 'Thank you for signing up!')
    #     else:
    #         messages.error(request, 'Email not valid or already exists!')
    #         form = NewsletterForm()
    #
    # else:
    #     form = NewsletterForm()

    context =  {
        'title' : 'Jar Album',
        'posts': Posts.objects.all().order_by('-date_created')[:3],
        'jar': Jar.objects.all(),
        }

    return render(request, 'home/album.html', context)

def about(request):
    context = {
        'AboutText': WebContent.objects.get(position__iexact="AboutPageText")
    }
    print(request.session.get('wishlist'))
    return render(request, 'home/about.html', context)

def page(request):


    content = request.GET
    print(content['page'])

    context = {
        'AboutText': WebContent.objects.get(position__iexact=content['page'])
    }
    print(request.session.get('wishlist'))
    return render(request, 'home/about.html', context)



def shop(request):
    check_set_session(request)
    # The shop page has to get data from the database of the selected Jar
    jar_number = request.session.get('wishlist')['products']
    if jar_number is not "":
        product = Jar.objects.select_related('product_details').get(jar_number__iexact=jar_number)
    else:
        product = None

    context = {
        'product': product,
    }


    return render(request, 'home/shop.html', context)

def contact(request):

    form = ContactForm()

    context =  {
        'title' : 'Contact Us',
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

def payment(request):
    return render(request, 'home/payment.html')

def thankyou(request):
    return render(request, 'home/thankyou.html')
