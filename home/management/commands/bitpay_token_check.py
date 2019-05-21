from django.core.management.base import BaseCommand
from shop.views import fetch_token

class Command(BaseCommand):
    help = 'Verify or activate Bitpay API key'

    def handle(self, *args, **kwargs):
        fetch_token("merchant")
