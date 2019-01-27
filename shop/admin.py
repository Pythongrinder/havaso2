from django.contrib import admin
from .models import Product, CheckOut, ProductCategory

# Register your models here.
admin.site.register(Product)
admin.site.register(CheckOut)
admin.site.register(ProductCategory)
