from django.db import models
from django.utils import timezone
from shop.models import Product, CheckOut


class Decorator(models.Model):
    decorator = models.CharField(max_length=100)

    def __str__(self):
        return self.decorator

#
# class JarIngredient(models.Model):
#     ingredient = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.ingredient


class JarPurpose(models.Model):
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword


class Jar(models.Model):
    jar_number = models.IntegerField(default=0)
    jar_name = models.CharField(max_length=50, default='')
    comment = models.CharField(max_length=50, blank=True)
    jar_image = models.FileField(upload_to='JarAlbum')
    decorator = models.ForeignKey(Decorator, on_delete=models.PROTECT, blank=True, null=True)
    production_date = models.DateTimeField(default=timezone.now)
    product_details = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True)
    sold_to = models.ForeignKey(CheckOut, on_delete=models.PROTECT, blank=True, null=True)
    status_options = (
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Historic Album', 'Historic Album'),
        ('Damaged', 'Damaged'),
    )
    jar_status = models.CharField(
        max_length=100,
        choices=status_options,
        default='Available'
    )

    def __str__(self):
        return self.jar_name
