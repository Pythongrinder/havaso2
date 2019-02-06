from django.contrib import admin
from .models import Jar, Decorator, JarPurpose

admin.site.register(Jar)
admin.site.register(Decorator)
admin.site.register(JarPurpose)
# admin.site.register(JarIngredient)