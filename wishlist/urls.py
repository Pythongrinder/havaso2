from django.urls import path
from . import views



urlpatterns = [
path('', views.wishlist, name='wishlist'),
path('add/', views.add, name='addwishlist'),
path('view/', views.viewwishlist, name='viewwishlist'),
path('emailwishlist/', views.sendwishlistemail, name='sendemailwishlist')

]
