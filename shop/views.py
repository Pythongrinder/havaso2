from django.shortcuts import render
from shop.tasks import after_sale_email
from album.models import Jar, JarPurpose
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from havasoweb.session import check_set_session
from shop.models import CheckOut as StoreCheckoutData
from bitpay.exceptions import *
import bitpay.key_utils as bku
from bitpay.client import *
import pprint
import requests
import os.path
from django.contrib.sites.shortcuts import get_current_site
import string
import random

API_HOST = "https://bitpay.com" #for production, live bitcoin
# API_HOST = "https://test.bitpay.com"  # for testing, testnet bitcoin
KEY_FILE = "realkey.priv"
TOKEN_FILE = "realtoken.priv"

# check if there is a preexisting key file
if os.path.isfile(KEY_FILE):
    f = open(KEY_FILE, 'r')
    key = f.read()
    f.close()
    print("Creating a bitpay client using existing private key from disk.")
else:
    key = bku.generate_pem()
    f = open(KEY_FILE, 'w')
    f.write(key)
    f.close()

client = Client(API_HOST, False, key)


def fetch_token(facade):
    if os.path.isfile(TOKEN_FILE + facade):
        f = open(TOKEN_FILE + facade, 'r')
        token = f.read()
        f.close()
        print("Reading " + facade + " token from disk.")
        # global client
        # client = Client(API_HOST, False, key, {facade: token})
        client.tokens[facade] = token
    else:
        pairingCode = client.create_token(facade)
        print("Creating " + facade + " token.")
        print(
            "Please go to:  %s/dashboard/merchant/api-tokens  then enter \"%s\" then click the \"Find\" button, then click \"Approve\"" % (
                API_HOST, pairingCode))
        input("When you've complete the above, hit enter to continue...")
        print("token is: %s" % client.tokens[facade])
        f = open(TOKEN_FILE + facade, 'w')
        f.write(client.tokens[facade])
        f.close()


def get_from_bitpay_api(client, uri, token):
    pp = pprint.PrettyPrinter(indent=4)
    payload = "?token=%s" % token
    xidentity = bku.get_compressed_public_key_from_pem(client.pem)
    xsignature = bku.sign(uri + payload, client.pem)
    headers = {"content-type": "application/json",
               "X-Identity": xidentity,
               "X-Signature": xsignature, "X-accept-version": "2.0.0"}
    try:
        pp.pprint(headers)
        print(uri + payload)
        response = requests.get(uri + payload, headers=headers, verify=client.verify)
    except Exception as pro:
        raise BitPayConnectionError(pro.args)
    if response.ok:
        return response.json()['data']
    client.response_error(response)


def shop(request):
    check_set_session(request)
    # The shop page has to get data from the database of the selected Jar
    wishlist_jar_number = request.session.get('session')['products']
    buy_jar_number = request.session.get('session')['buy']
    print(request.session.get('session'))
    if buy_jar_number:
        product = Jar.objects.select_related('product_details').get(jar_number__iexact=buy_jar_number)
        if product.jar_status == "Sold":
            request.session.get('session')['products'].remove(buy_jar_number)
            request.session.get('session')['buy'] = ""
            request.session.modified = True

    elif len(wishlist_jar_number) == 1:
        product = Jar.objects.select_related('product_details').get(jar_number__iexact=wishlist_jar_number[0])
        if product.jar_status == "Sold":
            request.session.get('session')['products'].remove(buy_jar_number)
            request.session.get('session')['buy'] = ""
            request.session.modified = True
    else:
        product = None

    if len(wishlist_jar_number) > 1:
        SeveralItemsWishlisted = True
    else:
        SeveralItemsWishlisted = False

    context = {
        'product': product,
        'itemswishlisted': SeveralItemsWishlisted
    }

    return render(request, 'shop/shop.html', context)


@csrf_exempt
def Selectjar(request):
    jar_number = request.GET.get('jar')

    if jar_number:
        result = Jar.objects.filter(jar_name__contains=jar_number, jar_status="Available")
        queryset = result.values()
        return JsonResponse({"models_to_return": list(queryset)})

    elif request.GET.get('jarnumber'):

        jar_number = request.GET.get('jarnumber')

        if jar_number:
            result = Jar.objects.filter(jar_number__iexact=jar_number, jar_status="Available")

            if result.count() is 0:
                result = Jar.objects.filter(jar_name__iexact=jar_number, jar_status="Available")

            if result.count() > 0:
                if str(list(result.values('jar_number'))[0]['jar_number']) not in request.session['session'][
                        'products']:
                    request.session['session']['products'].append(
                        str(list(result.values('jar_number'))[0]['jar_number']))
                    request.session.get('session')['buy'] = str(list(result.values('jar_number'))[0]['jar_number'])
                    request.session.modified = True

                else:
                    request.session['session']['buy'] = list(result.values('jar_number'))[0]['jar_number']
                    request.session.modified = True

                queryset = result.values()
                return JsonResponse({"models_to_return": list(queryset)})

    return JsonResponse({"models_to_return": ""})


def Checkout(request):
    if request.GET.get('purpose'):
        purpose = request.GET.get('purpose')
        request.session.get('session')['purpose'] = purpose
        request.session.modified = True
        if purpose == "General":
            result = JarPurpose.objects.all()
            queryset = result.values()
            return JsonResponse({"models_to_return": list(queryset)})

    if request.GET.get('puprosetext'):
        keywords = request.GET.get('puprosetext')
        request.session.get('session')['purposetext'] = keywords
        request.session.modified = True

    return JsonResponse("Type in a Jar name", safe=False)


def tocheckout(request):
    jar = request.POST.get('jarnumber')
    purpose = request.POST.get('jarpurpose')
    keywords = request.POST.get('jarkeyword')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    address = request.POST.get('address')
    address2 = request.POST.get('address2')
    country = request.POST.get('country')
    state = request.POST.get('state')
    zip = request.POST.get('zip')
    paymentmethod = request.POST.get('paymentMethod')

    if purpose == "Guided":
        price = 75.00
    elif purpose == "General":
        price = 27.50
    else:
        price = 42.50

    checkout = StoreCheckoutData(first_name=firstname, last_name=lastname, email=email, address1=address,
                                 address2=address2,
                                 country=country, state=state, zip=zip, paymentMethod=paymentmethod,
                                 order_details=jar + " " + purpose + " " + keywords)
    checkout.save()
    order_id = checkout.pk

    if paymentmethod == 'paypal':
        def id_generator(size=21, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        invoice = id_generator()
        checkout.paymentInvoice = invoice
        checkout.save()
        request.session.get('session')['invoice'] = invoice
        request.session.modified = True

        return JsonResponse("Paypal " + invoice, safe=False)

    if paymentmethod == 'bitcoin':
        fetch_token("merchant")
        print("We will create an invoice using the merchant facade")

        invoice = client.create_invoice({"price": float(price), "currency": "EUR", "token": client.tokens['merchant'],
                                         "redirectURL": "http://" + str(get_current_site(request)) + "/shop/thankyou/",
                                         "posData": '{ "ref" : ' + str(order_id) + ' }'})
        checkout.paymentInvoice = invoice['id']
        checkout.save()
        request.session.get('session')['invoice'] = invoice['id']
        request.session.modified = True
        return JsonResponse(invoice['url'], safe=False)
    return JsonResponse("none", safe=False)


def payment(request):
    jar_number = request.session.get('session')['buy']

    if jar_number == '':
        jar_number = request.session.get('session')['products'][0]

    buy_jar_data = Jar.objects.get(jar_number__iexact=jar_number)
    purpose = request.session.get('session')['purpose']
    if purpose == "Guided":
        price = "%.2f" % 75.00
    elif purpose == "General":
        price = "%.2f" % 27.50
    else:
        price = "%.2f" % 42.50

    context = {

        'jar': buy_jar_data,
        'purpose': purpose,
        'price': str(price),
        'keywords': request.session.get('session')['purposetext']

    }

    return render(request, 'shop/payment.html', context)


def thankyou(request):
    sold = False
    if request.session.get('session')['invoice'] != "":
        jar_number = request.session.get('session')['buy']
        if jar_number == '':
            jar_number = request.session.get('session')['products'][0]

        invoice_id = request.session.get('session')['invoice']
        checkout_object = StoreCheckoutData.objects.filter(paymentInvoice=invoice_id)
        if checkout_object.values('paymentMethod')[0]['paymentMethod'] == "bitcoin":
            fetch_token("merchant")
            token = client.tokens['merchant']
            invoice = get_from_bitpay_api(client, client.uri + "/invoices/" + invoice_id, token)
            StoreCheckoutData.objects.filter(paymentInvoice=invoice_id).update(paymentResponse=invoice['status'])
            if invoice['status'] == "confirmed" or invoice['status'] == "complete":
                sold = True
        elif checkout_object.values('paymentMethod')[0]['paymentMethod'] == "paypal":
            if checkout_object.values('paymentResponse')[0]['paymentResponse'] == "Complete":
                sold = True
        if sold:
            Jar.objects.filter(jar_number=jar_number).update(jar_status='Sold')
            jar_number = Jar.objects.get(jar_number=jar_number)
            request.session.get('session')['buy'], request.session.get('session')['invoice'] = "", ""
            request.session.modified = True
            order_details = StoreCheckoutData.objects.get(paymentInvoice=invoice_id)
            purpose = request.session.get('session')['purpose']
            print(order_details.address1)
            after_sale_email.delay(purpose, order_details.email, order_details.first_name, order_details.last_name,
                                   order_details.address1, order_details.address2, jar_number.jar_name)
            print(sold)
    return render(request, 'shop/thankyou.html')


@csrf_exempt
def paypal(request):
    VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
    # Switch as appropriate
    VERIFY_URL = VERIFY_URL_PROD
    # CGI preamble
    print(request.POST.dict())
    answer = request.POST.dict()
    dictlist = list(answer.items())
    dictlist.append(('cmd', '_notify-validate'))
    # Post back to PayPal for validation
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Python-IPN-Verification-Script'}
    r = requests.post(VERIFY_URL, params=dictlist, headers=headers, verify=True)
    r.raise_for_status()

    # Check return message and take action as needed
    if r.text == 'VERIFIED':
        print('VERIFIED')
        invoice = answer['custom'].split(':', 1)[1]
        print(invoice)
        StoreCheckoutData.objects.filter(paymentInvoice=invoice).update(paymentResponse='Complete')
        pass
    elif r.text == 'INVALID':
        print('INVALID')
        pass
    else:
        pass

    return JsonResponse("Thanks!", safe=False)
