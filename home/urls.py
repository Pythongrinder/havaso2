from django.urls import path
from . import views



urlpatterns = [

path('', views.index, name='havaso-home'),
path('contact/', views.contact, name='contact'),
path('contact2/', views.contact2, name='contact2'),
path('about/', views.about, name='about'),
path('services/', views.services, name='services'),
path('page/', views.page, name='about'),
]
