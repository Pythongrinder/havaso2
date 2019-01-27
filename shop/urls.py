from django.urls import path
from . import views



urlpatterns = [
path('select/', views.Selectjar, name='selectjar'),
path('getcheckout/', views.Checkout, name='getcheckout'),
]
