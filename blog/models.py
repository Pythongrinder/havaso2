from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField


class Category(models.Model):
    name = models.CharField(max_length=100)
    positions = (
        ('General', 'General'),
        ('Jars', 'Jars'),
    )
    position = models.CharField(max_length=100,
                                choices=positions,
                                default='General')
    private = models.BooleanField(null=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    featured_image = models.FileField(upload_to='blog', default='')
    content = RichTextField()
    categories = models.ManyToManyField(Category, blank=True, default=None)

    permission = (
        ('Not set', 'Not set'),
        ('Yes, can be published', 'Yes, can be published'),
        ('No, needs more work and re-edited again before publishing',
         'No, needs more work and re-edited again before publishing'),
    )
    permission_to_publish = models.CharField(
        max_length=1000,
        choices=permission,
        null=True,
        blank=True,
    )

    date_created = models.DateTimeField(default=timezone.now)
    date_posted = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='user_editor')
    slug = AutoSlugField(populate_from='title')

    def __str__(self):
        title = self.title + " Category: "
        category = ",".join([str(p) for p in self.categories.all()])
        return title + category
