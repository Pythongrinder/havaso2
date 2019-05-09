from django.urls import path
from . import views



urlpatterns = [

path('', views.index, name='havaso-home'),
path('contact/', views.contact, name='contact'),
path('about/', views.about, name='about'),
path('cng/', views.cng, name='cng'),
path('page/', views.page, name='about'),
]
