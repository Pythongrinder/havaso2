from django.db import models
from autoslug import AutoSlugField
from album.models import Jar
import string
import random

# Create your models here.

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class SentWishlist (models.Model):
    email = models.CharField(max_length=100, blank=True, default=None)
    wishlistedjars = models.ManyToManyField(Jar, blank=True, default=None)
    url_ref = AutoSlugField(default=rand_slug(), unique=True)
    def __str__(self):
        return self.email