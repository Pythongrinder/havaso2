def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_set_session(request):
    current_session_state = request.session.get('session')
    if current_session_state is None:
        ip = get_client_ip(request)
        print("New Session Started!")
        request.session['session'] = {
            'ip': ip,
            'products': [],
            'buy': "",
            'purpose': "",
            'purposetext': '',
            'invoice': '',
        }
        current_session_state = request.session.get('session')
        return current_session_state
    else:
        return current_session_state