# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def after_sale_email(purpose, email, first_name, last_name, address1, address2, jar_name):
    print(address1 + " " + address2)
    subject, from_email = 'Thank you for the purchase', 'support@havaso.com',
    html_content = render_to_string('shop/mail.html', {

        'purpose': purpose,
        'JarName': jar_name,
        'FullName': first_name + " " + last_name,
        'Address': address1 + " " + address2

    })  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return address1 + " " + address2

