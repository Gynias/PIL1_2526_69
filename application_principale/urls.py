from django.urls import path
from . import views

urlpatterns = [
    path('parametres/profil/', views.account_settings, name='account_settings'),
    path('parametres/securite/', views.security_settings, name='security_settings'),
]
