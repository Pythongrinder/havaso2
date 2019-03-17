from django.shortcuts import render
from .models import Legal
from havasoweb.session import check_set_session


def legal(request):
    check_set_session(request)
    content = request.GET
    try:
        legal_content = Legal.objects.get(url__iexact=content['legal'])
        single = True
    except:
        legal_content = Legal.objects.all()
        single = False
    context = {
        'single': single,
        'legals': legal_content,
    }

    return render(request, 'legal/legal.html', context)
