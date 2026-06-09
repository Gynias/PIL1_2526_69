from django.urls import path
from . import views

urlpatterns = [
    path('annonces/creer/', views.create_offer_request, name='create_offer_request'),
    path('annonces/decouvrir/', views.discover_page, name='discover_page'),
    path('annonces/detail/', views.offer_request_detail, name='offer_request_detail'),
    path('annonces/fil/', views.offer_request_feed, name='offer_request_feed'),
    path('annonces/recherche/', views.search_results, name='search_results'),
    path('parametres/profil/', views.account_settings, name='account_settings'),
    path('parametres/securite/', views.security_settings, name='security_settings'),
]
