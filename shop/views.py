from django.shortcuts import render

# Create your views here.
# Create your views here.
from album.models import Jar, JarPurpose
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.views import check_set_session
from shop.models import CheckOut as StoreCheckoutData
from bitpay.exceptions import *
import bitpay.key_utils as bku
from bitpay.client import *
import pprint
import requests
import json
import re
import os.path
from django.contrib.sites.shortcuts import get_current_site


def shop(request):
    check_set_session(request)
    # The shop page has to get data from the database of the selected Jar
    wishlist_jar_number = request.session.get('session')['products']
    buy_jar_number = request.session.get('session')['buy']
    print(request.session.get('session'))
    if len(wishlist_jar_number) == 1:
        product = Jar.objects.select_related('product_details').get(jar_number__iexact=wishlist_jar_number[0])
    elif buy_jar_number:
        product = Jar.objects.select_related('product_details').get(jar_number__iexact=buy_jar_number)
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
        result = Jar.objects.filter(jar_name__contains=jar_number)
        queryset = result.values()
        return JsonResponse({"models_to_return": list(queryset)})

    elif request.GET.get('jarnumber'):
        jar_number = request.GET.get('jarnumber')

        if jar_number:
            result = Jar.objects.filter(jar_number__iexact=jar_number)
            print(result.count())

            if result.count() is 0:
                result = Jar.objects.filter(jar_name__iexact=jar_number)
                print(result.count())

            if result.count() > 0:
                if str(list(result.values('jar_number'))[0]['jar_number']) not in request.session['session']['products']:
                    request.session['session']['products'].append(str(list(result.values('jar_number'))[0]['jar_number']))
                    request.session.get('session')['buy'] = str(list(result.values('jar_number'))[0]['jar_number'])
                    request.session.modified = True

                else:
                    request.session['session']['buy'] = list(result.values('jar_number'))[0]['jar_number']
                    request.session.modified = True

                queryset = result.values()
                return JsonResponse({"models_to_return": list(queryset)})

    return JsonResponse({"models_to_return": ""})


def Checkout(request):
    result = ""
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

    checkout = StoreCheckoutData(first_name=firstname, last_name=lastname, email=email, address1=address,
                                 address2=address2,
                                 country=country, state=state, zip=zip, paymentMethod=paymentmethod,
                                 order_details=jar + " " + purpose + " " + keywords)
    checkout.save()
    orderId = checkout.pk


    if paymentmethod == 'bitcoin':

        # API_HOST = "https://bitpay.com" #for production, live bitcoin
        API_HOST = "https://test.bitpay.com"  # for testing, testnet bitcoin
        KEY_FILE = "/tmp/key.priv"
        TOKEN_FILE = "/tmp/token.priv"

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

        """
        POST to any resource
        Make sure to include the proper token in the params
        """

        def post_to_bitpay_api(client, uri, resource, params):
            payload = json.dumps(params)
            uri = uri + "/" + resource
            xidentity = key_utils.get_compressed_public_key_from_pem(client.pem)
            xsignature = key_utils.sign(uri + payload, client.pem)
            headers = {"content-type": "application/json",
                       "accept": "application/json", "X-Identity": xidentity,
                       "X-Signature": xsignature, "X-accept-version": "2.0.0"}
            try:
                response = requests.post(uri, data=payload, headers=headers,
                                         verify=client.verify)
            except Exception as pro:
                raise BitPayConnectionError(pro.args)
            if response.ok:
                return response.json()['data']
            client.response_error(response)

        fetch_token("merchant")

        # Now we assume that the pairing code that we generated along with the crypto keys is paired with your merchant account

        print("We will create an invoice using the merchant facade")

        invoice = client.create_invoice({"price": float(2.00), "currency": "EUR", "token": client.tokens['merchant'],
                                         "redirectURL": "http://"+str(get_current_site(request))+"/shop/thankyou/",
                                         "posData": '{ "ref" : '+ str(orderId) +' }'})
        checkout.paymentInvoice = invoice['id']
        checkout.save()
        return JsonResponse(invoice['url'], safe=False)

    return JsonResponse("none", safe=False)


def payment(request):
    jar_number = request.session.get('session')['buy']
    buy_jar_data = Jar.objects.get(jar_number__iexact=jar_number)
    purpose = request.session.get('session')['purpose']
    if purpose == "Guided":
        price = "%.2f" % 75.00
    elif purpose == "General":
        price = "%.2f" % 27.50
    elif purpose == "Personal":
        price = "%.2f" % 42.50

    print(buy_jar_data)
    context = {

        'jar': buy_jar_data,
        'purpose': purpose,
        'price':str(price),
        'keywords': request.session.get('session')['purposetext']

    }

    return render(request, 'shop/payment.html', context)


def thankyou(request):
    return render(request, 'shop/thankyou.html')
