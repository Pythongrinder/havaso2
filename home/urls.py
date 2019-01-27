from django.urls import path
from . import views



urlpatterns = [

path('', views.index, name='havaso-home'),
path('album/', views.album, name='album'),
path('contact/', views.contact, name='contact'),
path('shop/', views.shop, name='shop'),
path('about/', views.about, name='about'),
path('payment/', views.payment, name='shop'),
path('thankyou/', views.thankyou, name='shop'),
path('page/', views.page, name='shop'),
]
