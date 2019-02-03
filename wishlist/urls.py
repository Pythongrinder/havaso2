from django.urls import path
from . import views



urlpatterns = [
path('add/', views.create, name='addwishlist'),
path('view/', views.viewwishlist, name='viewwishlist')
]
