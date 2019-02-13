from django.shortcuts import render
from .models import Legal

# Create your views here.

# Create your views here.
def legal(request):

    content = request.GET

    try:
        legal_content = Legal.objects.get(url__iexact=content['legal'])
        single = True
    except:

        legal_content = Legal.objects.all()
        single = False
    print(single)
    context = {
        'single' : single,
        'legals': legal_content,
    }

    return render(request, 'legal/legal.html', context)