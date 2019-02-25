from django.urls import path
from . import views

urlpatterns = [
    path('', views.album, name='album'),
    path('historic/', views.historic_album, name='historic_album'),
]
