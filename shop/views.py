from django.shortcuts import render

# Create your views here.
# Create your views here.
from album.models import Jar, JarIngredient, JarGoalKeyword
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
                if list(result.values('jar_number'))[0]['jar_number'] not in request.session['wishlist']['products']:
                    request.session['wishlist']['products'].append(list(result.values('jar_number'))[0]['jar_number'])
                    request.session.modified = True
                    print(request.session.get('wishlist'))

                else:
                    request.session['wishlist']['buy'] = list(result.values('jar_number'))[0]['jar_number']
                    request.session.modified = True
                    print(request.session.get('wishlist'))

                queryset = result.values()
                return JsonResponse({"models_to_return": list(queryset)})

    return JsonResponse("Type in a Jar name", safe=False)


def Checkout(request):
    result = ""
    if request.GET.get('purpose'):
        purpose = request.GET.get('purpose')
        if purpose == "General":
            result = JarIngredient.objects.all()
            print(result)
        elif purpose == "Personal":
            result = JarGoalKeyword.objects.all()
        queryset = result.values()
        return JsonResponse({"models_to_return": list(queryset)})

    if request.GET.get('keywords'):
        keywords = request.GET.get('keywords')
        if keywords is not "":
            result = JarIngredient.objects.all()

            queryset = result.values()
            return JsonResponse({"models_to_return": list(queryset)})

    return JsonResponse("Type in a Jar name", safe=False)
