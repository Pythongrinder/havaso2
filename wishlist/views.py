from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from album.models import Jar, Decorator
from .models import SentWishlist
from django.core import serializers
import json
from blog.models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.defaulttags import register
from home.views import check_set_session
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone


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


@csrf_exempt
def remove_jar_from_wish_list(request):
    print(request.session['session'])
    if request.POST.get("removejar"):
        jar_number = request.POST.get("removejar", )
        request.session['session']['products'].remove(jar_number)
        request.session.modified = True
    return JsonResponse("Jar Removed", safe=False)


def viewwishlist(request):
    wish_listed_items_detail_list = []
    output = {}
    if request.method == "GET":
        try:
            wish_listed_items = request.session.get('session')['products']

            for item in wish_listed_items:
                wish_listed_items_details = Jar.objects.select_related('decorator').filter(jar_number__iexact=item)
                wish_listed_items_detail_list.append(wish_listed_items_details)
            i = 0
            for item in wish_listed_items_detail_list:
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
    jars_objects = []
    wish_listed_items = request.session.get('session')['products']
    if len(wish_listed_items) is not 0:
        print(email)
        for jar in wish_listed_items:
            jars_objects.append(Jar.objects.get(jar_number=jar))

        a = SentWishlist(email=email)
        a.save()
        a.wishlistedjars.set(jars_objects)

        subject, from_email = 'Your Medicine Jar Wish List', 'support@havaso.com',
        link = str(get_current_site(request)) + '/wishlist/?wishlist=' + str(a.url_ref)
        html_content = render_to_string('wishlist/mail.html', {'link': link})  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("Done!")
    else:
        return HttpResponse("Empty")


def wishlist(request):
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(pk=key)

    check_set_session(request)
    wish_list_slug = request.GET.get("wishlist")
    wish_list_object = SentWishlist.objects.get(url_ref=wish_list_slug)
    decorators = Decorator.objects.filter(id__in=wish_list_object.wishlistedjars.values_list('decorator_id'))

    time_between_insertion = datetime.now(timezone.utc) - wish_list_object.date_created
    print(wish_list_object.wishlistedjars.values())
    if time_between_insertion.days < 30:
        context = {
            'decorator': decorators,
            'jars': wish_list_object.wishlistedjars.values(),
            'posts': Post.objects.all().order_by('-date_created')[:3],
        }
    else:
        context = {
            'decorator': "",
            'jars': "Expired",
            'posts': Post.objects.all().order_by('-date_created')[:3],
        }

    return render(request, 'wishlist/wishlist.html', context)
