from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Legal(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    content = RichTextField()


    def __str__(self):
        return self.url
