from django.core.management.base import BaseCommand
from django.utils import timezone
from wishlist.models import SentWishlist
from datetime import datetime, timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from havasoweb.settings import website


class Command(BaseCommand):

    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        wish_list_object = SentWishlist.objects.all()
        for i in wish_list_object:
            time_between_insertion = datetime.now(timezone.utc) - i.date_created
            if time_between_insertion.days == 97:
                email = i.email
                subject, from_email = 'Reminder: Your Medicine Jar Wish List will expire in 7 days',\
                                      'support@havaso.com',
                link = website + '/wishlist/?wishlist=' + str(i.url_ref)
                html_content = render_to_string('wishlist/reminder_email.html', {'link': link})
                # render with dynamic value
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
