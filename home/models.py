from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField



class WebContent(models.Model):
    position = models.CharField(max_length=200)
    text = RichTextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.position


class Contact_Form(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    need = models.CharField(max_length=200,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    sent_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.sent_date)
