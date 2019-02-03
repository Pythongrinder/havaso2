from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from album.models import Jar
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core import serializers
import json
import itertools

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create(request):
    if request.method == "POST" and request.POST.get("jar"):
        print("PAY ATTENTION")
        print(request.POST.get("jar"))
        status = request.POST.get("jar")
        if status not in request.session['wishlist']['products']:
            request.session['wishlist']['products'].append(status)
            request.session.modified = True
        print(request.session.get('wishlist'))
    else:
        if request.POST.get("buyjar"):
            jar_number = request.POST.get("buyjar", )
            request.session['wishlist']['buy'] = jar_number
            request.session.modified = True
        print(request.session.get('wishlist'))


    return JsonResponse("Type in a Jar name", safe=False)


def viewwishlist(request):
    WishlistedItemsDetailList = []
    output = {}
    if request.method == "GET":
        try:
            WishlistedItems = request.session.get('wishlist')['products']

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


def sendwishlist(request):
    sender_email = "my@gmail.com"
    receiver_email = "your@gmail.com"
    password = input("Type your password and press enter:")

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a> 
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
