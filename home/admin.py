from django.contrib import admin

# Register your models here.
from .models import WebContent, Contact_Form

admin.site.register(WebContent)
admin.site.register(Contact_Form)
