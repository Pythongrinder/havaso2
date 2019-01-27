from django.shortcuts import render

# Create your views here.
# Create your views here.
from album.models import Jar, JarIngredient, JarGoalKeyword
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Selectjar(request):
    status = 0
    if request.GET.get('jar'):
        status = request.GET.get('jar')
        if status:
            result = Jar.objects.filter(jar_name__contains=status)
            queryset = result.values()
            return JsonResponse({"models_to_return": list(queryset)})

    elif request.GET.get('jarnumber'):
        status = request.GET.get('jarnumber')
        if status:
            result = Jar.objects.filter(jar_number__iexact=status)
            if result.count() is 0:
                result = Jar.objects.filter(jar_name__iexact=status)

            request.session['wishlist']['products'] = list(result.values('jar_number'))[0]['jar_number']
            print(request.session.get('wishlist'))
            request.session.modified = True

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
