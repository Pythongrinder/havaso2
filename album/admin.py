from django.contrib import admin
from .models import Jar, Decorator, JarGoalKeyword, JarIngredient
# Register your models here.

admin.site.register(Jar)
admin.site.register(Decorator)
admin.site.register(JarGoalKeyword)
admin.site.register(JarIngredient)