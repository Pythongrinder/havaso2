from django.shortcuts import render

# Create your views here.
# Create your views here.
from album.models import Jar, JarPurpose
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.views import check_set_session


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
                if list(result.values('jar_number'))[0]['jar_number'] not in request.session['session']['products']:
                    request.session['session']['products'].append(list(result.values('jar_number'))[0]['jar_number'])
                    request.session.modified = True

                else:
                    request.session['session']['buy'] = list(result.values('jar_number'))[0]['jar_number']
                    request.session.modified = True

                queryset = result.values()
                return JsonResponse({"models_to_return": list(queryset)})

    return JsonResponse("Type in a Jar name", safe=False)


def Checkout(request):
    result = ""
    if request.GET.get('purpose'):
        purpose = request.GET.get('purpose')
        if purpose == "General":
            result = JarPurpose.objects.all()
            print(result)
        elif purpose == "Personal":
            result = JarPurpose.objects.all()
        queryset = result.values()
        return JsonResponse({"models_to_return": list(queryset)})

    if request.GET.get('keywords'):
        keywords = request.GET.get('keywords')
        if keywords is not "":
            result = JarPurpose.objects.all()

            queryset = result.values()
            return JsonResponse({"models_to_return": list(queryset)})

    return JsonResponse("Type in a Jar name", safe=False)

def tocheckout(request):

    return JsonResponse("Type in a Jar name", safe=False)


def payment(request):

    buy_jar_number = request.session.get('session')['buy']
    # purpose = request.session.get('session')['purpose']

    context = {

        'jar': buy_jar_number,
        # 'purpose': purpose,

    }

    return render(request, 'shop/payment.html', context)

def thankyou(request):
    return render(request, 'shop/thankyou.html')