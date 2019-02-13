from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from album.models import Jar, Decorator
from .models import SentWishlist
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core import serializers
import json
from django.core.mail import send_mail
from blog.models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.defaulttags import register
from home.views import check_set_session
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add(request):
    print(request.session['session'])
    if request.method == "POST" and request.POST.get("jar"):
        print(request.POST.get("jar"))
        status = request.POST.get("jar")
        if status not in request.session['session']['products']:
            request.session['session']['products'].append(status)
            request.session.modified = True
    else:
        if request.POST.get("buyjar"):
            jar_number = request.POST.get("buyjar", )
            request.session['session']['buy'] = jar_number
            request.session.modified = True

    return JsonResponse("Type in a Jar name", safe=False)


def viewwishlist(request):
    WishlistedItemsDetailList = []
    output = {}
    if request.method == "GET":
        try:
            WishlistedItems = request.session.get('session')['products']

            for item in WishlistedItems:
                WishlistedItemsDetails = Jar.objects.select_related('decorator').filter(jar_number__iexact=item)
                WishlistedItemsDetailList.append(WishlistedItemsDetails)
            i = 0
            for item in WishlistedItemsDetailList:
                # STRING
                data = serializers.serialize('json', item)
                # List and inside dictionary
                d = json.loads(data)
                # Append only dictionary to a list with dictionary
                for dec in item:
                    decorator = dec.decorator
                    d[0]['fields']['decorator'] = str(decorator)
                output[i] = d[0]
                i += 1
            d = json.dumps([output])

        except:
            d = None
    return HttpResponse(d, content_type='application/json')


def sendwishlistemail(request):
    email = request.POST.get("mail")
    print(email)
    JarsObjects = []
    WishlistedItems = request.session.get('session')['products']
    for jar in WishlistedItems:
        JarsObjects.append(Jar.objects.get(jar_number=jar))

    print(JarsObjects)
    a = SentWishlist(email=email)
    a.save()
    a.wishlistedjars.set(JarsObjects)

    subject, from_email = 'Subject', 'support@havaso.com',
    link = str(get_current_site(request)) +'/wishlist/?wishlist=' + str(a.url_ref)
    html_content = render_to_string('wishlist/mail.html', {'link': link})  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Done!")


def wishlist(request):
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(pk=key)

    check_set_session(request)
    wishlist_slug = request.GET.get("wishlist")
    jars = SentWishlist.objects.get(url_ref=wishlist_slug)
    decorators = Decorator.objects.filter(id__in=jars.wishlistedjars.values_list('decorator_id'))  # query
    context = {
        'decorator': decorators,
        'jars': jars.wishlistedjars.values(),
        'posts': Post.objects.all().order_by('-date_created')[:3],
    }
    return render(request, 'wishlist/wishlist.html', context)
