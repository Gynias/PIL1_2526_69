from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', views.connexion_view, name='login'),
    path('inscription/', views.inscription_view, name='signup'),
    path('deconnexion/', views.deconnexion_view, name='logout'),
    path('parametres/profil/', views.account_settings, name='account_settings'),
    path('parametres/securite/', views.security_settings, name='security_settings'),
]
