from django.urls import path
from . import views



urlpatterns = [
path('payment/', views.payment, name='shop'),
path('', views.shop, name='shop'),
path('select/', views.Selectjar, name='selectjar'),
path('getcheckout/', views.Checkout, name='getcheckout'),
path('thankyou/', views.thankyou, name='shop'),
path('tocheckout/', views.tocheckout, name='shop'),

]
