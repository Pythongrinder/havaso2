from django.db import models
# Create your models here.

class ProductCategory(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    present_in_list = models.BooleanField(default=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)


class CheckOut(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=500)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    order_details = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

